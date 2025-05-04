import datetime
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Accommodation, Member, Reservation, Rating

# filepath: Django/Backend/basic/test_models.py
from django.core.mail import send_mail # Import send_mail for mocking check

# Use relative import based on the project structure

class MemberModelTests(TestCase):
    """Tests for the Member model."""

    def test_member_creation(self):
        """Test creating a Member instance."""
        member = Member.objects.create(
            name='Test Member',
            contact='98765432',
            institute='HKU',
            email='member@test.com'
        )
        self.assertEqual(member.name, 'Test Member')
        self.assertEqual(member.contact, '98765432')
        self.assertEqual(member.institute, 'HKU')
        self.assertEqual(member.email, 'member@test.com')
        self.assertTrue(member.active)
        self.assertEqual(str(member), 'Test Member (HKU)')

    def test_member_update(self):
        """Test updating a Member instance."""
        member = Member.objects.create(name='Initial Name', contact='111', institute='CUHK', email='initial@test.com')
        member.name = 'Updated Name'
        member.active = False
        member.save()
        updated_member = Member.objects.get(pk=member.pk)
        self.assertEqual(updated_member.name, 'Updated Name')
        self.assertFalse(updated_member.active)

    def test_member_deletion(self):
        """Test deleting a Member instance."""
        member = Member.objects.create(name='To Delete', contact='222', institute='HKUST', email='delete@test.com')
        member_id = member.pk
        member.delete()
        with self.assertRaises(Member.DoesNotExist):
            Member.objects.get(pk=member_id)

# Mock external dependencies for Accommodation tests
@patch('basic.models.googlemaps.Client') # Mock the googlemaps client
@patch('basic.models.requests.get') # Mock requests.get used in get_lat_long
@patch('basic.models.pyproj.Transformer') # Mock pyproj Transformer
class AccommodationModelTests(TestCase):
    """Tests for the Accommodation model."""

    def setUp(self):
        """Set up common data for tests."""
        self.accommodation_data = {
            'flat_number': '2B',
            'floor_number': 2,
            'building_name': 'Test Building',
            'availability_start': datetime.date.today(),
            'availability_end': datetime.date.today() + datetime.timedelta(days=100),
            'number_of_beds': 1,
            'no_of_bedrooms': 1,
            'type_of_accommodation': 'Single',
            'price_per_month': 6000.00,
            'managed_by': 'UniHaven Test',
        }

    def test_accommodation_creation(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test creating an Accommodation instance with mocked external calls."""
        # Configure mocks
        mock_gmaps_instance = mock_gmaps_client.return_value
        mock_gmaps_instance.geocode.return_value = [{'geometry': {'location': {'lat': 22.2830, 'lng': 114.1365}}}] # Mock geocode if used

        # Mock the response from geodata.gov.hk API
        mock_response = MagicMock()
        mock_response.status_code = 200
        # Simulate the structure returned by the API (HK1980 Grid Coordinates)
        mock_response.json.return_value = [{'x': 833500, 'y': 816500}] # Example HK1980 coordinates
        mock_requests_get.return_value = mock_response

        # Mock the coordinate transformation result (WGS84 lat/lon)
        mock_transformer_instance = mock_transformer.from_crs.return_value
        mock_transformer_instance.transform.return_value = (114.1365621, 22.2830891) # lon, lat

        # Create accommodation - this will trigger the save method and mocked calls
        accommodation = Accommodation.objects.create(**self.accommodation_data)

        # Assertions
        self.assertEqual(accommodation.building_name, 'Test Building')
        self.assertEqual(accommodation.floor_number, 2)
        self.assertTrue(accommodation.active)
        # Check if lat/lon and distances were calculated (using mocked values)
        self.assertIsNotNone(accommodation.latitude)
        self.assertIsNotNone(accommodation.longitude)
        self.assertIsNotNone(accommodation.distance_to_HKUcampus)
        # Check __str__ method
        self.assertEqual(str(accommodation), 'Test Building - Floor 2, Flat 2B')

        # Verify mocks were called (optional but good practice)
        mock_requests_get.assert_called_once()
        mock_transformer_instance.transform.assert_called_once()


    def test_accommodation_update(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test updating an Accommodation instance."""
        # Configure mocks as in creation test
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'x': 833500, 'y': 816500}]
        mock_requests_get.return_value = mock_response
        mock_transformer_instance = mock_transformer.from_crs.return_value
        mock_transformer_instance.transform.return_value = (114.1365621, 22.2830891)

        accommodation = Accommodation.objects.create(**self.accommodation_data)
        accommodation.price_per_month = 6500.00
        accommodation.active = False
        accommodation.save() # Save triggers mocks again

        updated_accommodation = Accommodation.objects.get(pk=accommodation.pk)
        self.assertEqual(updated_accommodation.price_per_month, 6500.00)
        self.assertFalse(updated_accommodation.active)
        # Ensure mocks were called multiple times (creation + update)
        self.assertEqual(mock_requests_get.call_count, 2)
        self.assertEqual(mock_transformer_instance.transform.call_count, 2)


    def test_accommodation_deletion(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test deleting an Accommodation instance."""
        # Configure mocks
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'x': 833500, 'y': 816500}]
        mock_requests_get.return_value = mock_response
        mock_transformer_instance = mock_transformer.from_crs.return_value
        mock_transformer_instance.transform.return_value = (114.1365621, 22.2830891)

        accommodation = Accommodation.objects.create(**self.accommodation_data)
        accommodation_id = accommodation.pk
        accommodation.delete()
        with self.assertRaises(Accommodation.DoesNotExist):
            Accommodation.objects.get(pk=accommodation_id)

# Need to mock external calls for Accommodation save within Reservation tests too
@patch('basic.models.googlemaps.Client')
@patch('basic.models.requests.get')
@patch('basic.models.pyproj.Transformer')
class ReservationModelTests(TestCase):
    """Tests for the Reservation model."""

    def setUp(self):
        """Set up Accommodation and Member for Reservation tests."""
        # Mock external calls for setUp Accommodation creation
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'x': 833500, 'y': 816500}]
        requests_get_patcher = patch('basic.models.requests.get', return_value=mock_response)
        transformer_patcher = patch('basic.models.pyproj.Transformer')
        self.mock_requests_get = requests_get_patcher.start()
        self.mock_transformer = transformer_patcher.start()
        self.mock_transformer_instance = self.mock_transformer.from_crs.return_value
        self.mock_transformer_instance.transform.return_value = (114.1365621, 22.2830891)

        self.member = Member.objects.create(name='Res Member', contact='333', institute='HKU', email='res@test.com')
        self.accommodation = Accommodation.objects.create(
            flat_number='3C', floor_number=3, building_name='Res Building',
            availability_start=datetime.date.today(),
            availability_end=datetime.date.today() + datetime.timedelta(days=365),
            price_per_month=7000.00, managed_by='Res Manager'
        )
        self.start_date = datetime.date.today() + datetime.timedelta(days=10)
        self.end_date = datetime.date.today() + datetime.timedelta(days=40)

        # Stop setUp specific patches
        requests_get_patcher.stop()
        transformer_patcher.stop()


    def test_reservation_creation(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test creating a Reservation instance."""
        reservation = Reservation.objects.create(
            accommodation=self.accommodation,
            member=self.member,
            start_date=self.start_date,
            end_date=self.end_date,
            status='Not Signed'
        )
        self.assertEqual(reservation.accommodation, self.accommodation)
        self.assertEqual(reservation.member, self.member)
        self.assertEqual(reservation.status, 'Not Signed')
        self.assertTrue(reservation.active)
        self.assertEqual(
            str(reservation),
            f"Reservation for {self.accommodation} by {self.member} ({self.start_date} to {self.end_date})"
        )

    def test_reservation_update(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test updating a Reservation instance."""
        reservation = Reservation.objects.create(
            accommodation=self.accommodation, member=self.member,
            start_date=self.start_date, end_date=self.end_date, status='Not Signed'
        )
        reservation.status = 'Signed'
        reservation.save()
        updated_reservation = Reservation.objects.get(pk=reservation.pk)
        self.assertEqual(updated_reservation.status, 'Signed')

    def test_reservation_deletion(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test deleting a Reservation instance."""
        reservation = Reservation.objects.create(
            accommodation=self.accommodation, member=self.member,
            start_date=self.start_date, end_date=self.end_date, status='Not Signed'
        )
        reservation_id = reservation.pk
        reservation.delete()
        with self.assertRaises(Reservation.DoesNotExist):
            Reservation.objects.get(pk=reservation_id)

    def test_reservation_clean_dates(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test validation preventing end_date before start_date."""
        with self.assertRaisesRegex(ValidationError, "End date cannot be before start date."):
            Reservation(
                accommodation=self.accommodation, member=self.member,
                start_date=self.end_date, end_date=self.start_date, status='Not Signed'
            ).full_clean()

    def test_reservation_clean_overlap(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test validation preventing overlapping reservations."""
        Reservation.objects.create(
            accommodation=self.accommodation, member=self.member,
            start_date=self.start_date, end_date=self.end_date, status='Signed'
        )
        # Attempt to create an overlapping reservation
        with self.assertRaises(ValidationError) as cm:
            Reservation(
                accommodation=self.accommodation, member=self.member,
                start_date=self.start_date + datetime.timedelta(days=5), # Overlaps
                end_date=self.end_date + datetime.timedelta(days=5),
                status='Not Signed'
            ).full_clean()
        self.assertIn("already reserved during the period", str(cm.exception))

        # Test non-overlapping reservation is allowed
        try:
             Reservation(
                accommodation=self.accommodation, member=self.member,
                start_date=self.end_date + datetime.timedelta(days=1), # Starts after previous ends
                end_date=self.end_date + datetime.timedelta(days=10),
                status='Not Signed'
            ).full_clean() # Should not raise ValidationError
        except ValidationError as e:
            self.fail(f"Non-overlapping reservation raised ValidationError: {e}")


    def test_reservation_clean_inactive_signed(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test validation preventing inactive status for signed contracts."""
        with self.assertRaisesRegex(ValidationError, "cannot be set to inactive"):
            Reservation(
                accommodation=self.accommodation, member=self.member,
                start_date=self.start_date, end_date=self.end_date,
                status='Signed', active=False # Invalid combination
            ).full_clean()

        # Test that active=True with status='Signed' is valid
        try:
            Reservation(
                accommodation=self.accommodation, member=self.member,
                start_date=self.start_date, end_date=self.end_date,
                status='Signed', active=True
            ).full_clean() # Should not raise
        except ValidationError as e:
            self.fail(f"Valid active signed reservation raised ValidationError: {e}")

    @patch('basic.models.send_mail') # Mock send_mail specifically for this test
    def test_reservation_save_email_notification(self, mock_send_mail, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test email notification is sent when active status changes."""
        # Create initial reservation
        reservation = Reservation.objects.create(
            accommodation=self.accommodation, member=self.member,
            start_date=self.start_date, end_date=self.end_date,
            status='Not Signed', active=True
        )
        mock_send_mail.assert_not_called() # No email on creation

        # Update active status to False
        reservation.active = False
        reservation.save()
        mock_send_mail.assert_called_once() # Email should be sent
        args, kwargs = mock_send_mail.call_args
        self.assertEqual(args[0], 'Your Reservation Status Has Changed') # Subject
        self.assertIn('updated to: Inactive', args[1]) # Message content
        self.assertEqual(args[3], [self.member.email]) # Recipient list

        # Reset mock and update active status back to True
        mock_send_mail.reset_mock()
        reservation.active = True
        reservation.save()
        mock_send_mail.assert_called_once() # Email should be sent again
        args, kwargs = mock_send_mail.call_args
        self.assertIn('updated to: Active', args[1]) # Message content

        # Reset mock and save without changing active status
        mock_send_mail.reset_mock()
        reservation.status = 'Signed' # Change something else
        reservation.save()
        mock_send_mail.assert_not_called() # No email if active status didn't change


# Need to mock external calls for Accommodation save within Rating tests too
@patch('basic.models.googlemaps.Client')
@patch('basic.models.requests.get')
@patch('basic.models.pyproj.Transformer')
class RatingModelTests(TestCase):
    """Tests for the Rating model."""

    def setUp(self):
        """Set up data for Rating tests."""
        # Mock external calls for setUp Accommodation creation
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'x': 833500, 'y': 816500}]
        requests_get_patcher = patch('basic.models.requests.get', return_value=mock_response)
        transformer_patcher = patch('basic.models.pyproj.Transformer')
        self.mock_requests_get = requests_get_patcher.start()
        self.mock_transformer = transformer_patcher.start()
        self.mock_transformer_instance = self.mock_transformer.from_crs.return_value
        self.mock_transformer_instance.transform.return_value = (114.1365621, 22.2830891)

        self.member = Member.objects.create(name='Rating Member', contact='444', institute='CUHK', email='rating@test.com')
        self.accommodation = Accommodation.objects.create(
            flat_number='4D', floor_number=4, building_name='Rating Building',
            availability_start=datetime.date.today(),
            availability_end=datetime.date.today() + datetime.timedelta(days=365),
            price_per_month=8000.00, managed_by='Rating Manager'
        )
        # Create a completed reservation in the past
        self.completed_reservation = Reservation.objects.create(
            accommodation=self.accommodation,
            member=self.member,
            start_date=timezone.now().date() - datetime.timedelta(days=60),
            end_date=timezone.now().date() - datetime.timedelta(days=30),
            status='Signed',
            active=True
        )
        # Create an ongoing reservation
        self.ongoing_reservation = Reservation.objects.create(
            accommodation=self.accommodation,
            member=self.member,
            start_date=timezone.now().date() - datetime.timedelta(days=10),
            end_date=timezone.now().date() + datetime.timedelta(days=20),
            status='Signed',
            active=True
        )

        # Stop setUp specific patches
        requests_get_patcher.stop()
        transformer_patcher.stop()

    def test_rating_creation_valid(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test creating a valid Rating instance after reservation ended."""
        rating = Rating(
            accommodation=self.accommodation,
            member=self.member,
            rating=5,
            comment="Excellent stay!"
        )
        rating.full_clean() # Should not raise ValidationError
        rating.save()
        self.assertEqual(rating.rating, 5)
        self.assertEqual(rating.comment, "Excellent stay!")
        self.assertTrue(rating.active)
        self.assertEqual(
            str(rating),
            f"Rating for {self.accommodation} by {self.member}: 5"
        )

    def test_rating_update(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test updating a Rating instance."""
        rating = Rating.objects.create(
            accommodation=self.accommodation, member=self.member, rating=4
        )
        rating.rating = 3
        rating.comment = "Updated comment"
        rating.active = False
        rating.full_clean() # Ensure update is still valid
        rating.save()
        updated_rating = Rating.objects.get(pk=rating.pk)
        self.assertEqual(updated_rating.rating, 3)
        self.assertEqual(updated_rating.comment, "Updated comment")
        self.assertFalse(updated_rating.active)

    def test_rating_deletion(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test deleting a Rating instance."""
        rating = Rating.objects.create(
            accommodation=self.accommodation, member=self.member, rating=5
        )
        rating_id = rating.pk
        rating.delete()
        with self.assertRaises(Rating.DoesNotExist):
            Rating.objects.get(pk=rating_id)

    def test_rating_clean_invalid_period(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test validation preventing rating before reservation ends."""
        # Create a member and accommodation without a *completed* reservation
        new_member = Member.objects.create(name='New Member', contact='555', email='new@test.com', institute='HKUST')
        # Use existing accommodation, but this member only has an ongoing reservation
        with self.assertRaisesRegex(ValidationError, "only rate an accommodation after your reservation period has ended"):
             # Try to rate based on the ongoing reservation
            Rating(
                accommodation=self.accommodation,
                member=self.member, # This member has completed and ongoing
                rating=4
            ).full_clean() # This should pass because *a* completed reservation exists

        # Try to rate when NO completed reservation exists for the member/acco pair
        another_acco = Accommodation.objects.create(
             flat_number='5E', floor_number=5, building_name='Another Building',
             availability_start=datetime.date.today(),
             availability_end=datetime.date.today() + datetime.timedelta(days=365),
             price_per_month=9000.00, managed_by='Another Manager'
        )
        with self.assertRaisesRegex(ValidationError, "only rate an accommodation after your reservation period has ended"):
            Rating(
                accommodation=another_acco, # Different accommodation
                member=self.member,
                rating=4
            ).full_clean()


    def test_rating_clean_invalid_value(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test validation for rating value (1-5)."""
        with self.assertRaisesRegex(ValidationError, "Rating must be between 1 and 5."):
            Rating(
                accommodation=self.accommodation, member=self.member, rating=0
            ).full_clean()
        with self.assertRaisesRegex(ValidationError, "Rating must be between 1 and 5."):
            Rating(
                accommodation=self.accommodation, member=self.member, rating=6
            ).full_clean()

        # Test valid values don't raise error
        try:
            Rating(accommodation=self.accommodation, member=self.member, rating=1).full_clean()
            Rating(accommodation=self.accommodation, member=self.member, rating=5).full_clean()
        except ValidationError as e:
            self.fail(f"Valid rating raised ValidationError: {e}")

    def test_rating_unique_together(self, mock_transformer, mock_requests_get, mock_gmaps_client):
        """Test unique constraint for (accommodation, member)."""
        # Create the first rating
        Rating.objects.create(
            accommodation=self.accommodation, member=self.member, rating=5
        )
        # Attempt to create a second rating for the same pair
        with self.assertRaises(ValidationError) as cm:
             # Note: unique_together is checked during save/full_clean, not __init__
             duplicate_rating = Rating(
                 accommodation=self.accommodation, member=self.member, rating=4
             )
             duplicate_rating.full_clean() # This should raise the validation error
        # Check if the error message relates to the unique constraint
        # Django's default message might vary slightly, check for key fields
        self.assertIn('Rating with this Accommodation and Member already exists.', str(cm.exception))

        # Test that a different member can rate the same accommodation
        other_member = Member.objects.create(name='Other Member', contact='666', email='other@test.com', institute='PolyU')
        # Need a completed reservation for this other member too
        Reservation.objects.create(
            accommodation=self.accommodation,
            member=other_member,
            start_date=timezone.now().date() - datetime.timedelta(days=60),
            end_date=timezone.now().date() - datetime.timedelta(days=30),
            status='Signed', active=True
        )
        try:
            Rating(
                accommodation=self.accommodation, member=other_member, rating=3
            ).full_clean() # Should not raise unique constraint error
        except ValidationError as e:
             self.fail(f"Rating by different member raised ValidationError: {e}")
