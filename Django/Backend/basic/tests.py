import datetime
from django.test import TestCase
from .models import Accommodation, Member, Reservation, Rating

# filepath: /home/mio/Documents/django/unihaven/Backend/basic/test_serializers.py
from .serializers import (
    AccommodationSerializer,
    MemberSerializer,
    ReservationSerializer,
    RatingSerializer,
)

class AccommodationSerializerTest(TestCase):
    def setUp(self):
        self.accommodation_attributes = {
            'room_number': 101,
            'flat_number': 'A',
            'floor_number': 1,
            'building_name': 'Test Building',
            'availability_start': datetime.date(2024, 1, 1),
            'availability_end': datetime.date(2024, 12, 31),
            'managed_by': 'Test Manager'
        }
        self.accommodation = Accommodation.objects.create(**self.accommodation_attributes)
        self.serializer = AccommodationSerializer(instance=self.accommodation)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'room_number', 'flat_number', 'floor_number', 'building_name', 'availability_start', 'availability_end', 'managed_by'})

    def test_field_content(self):
        """Test the content of the serialized fields."""
        data = self.serializer.data
        self.assertEqual(data['room_number'], self.accommodation_attributes['room_number'])
        self.assertEqual(data['flat_number'], self.accommodation_attributes['flat_number'])
        self.assertEqual(data['floor_number'], self.accommodation_attributes['floor_number'])
        self.assertEqual(data['building_name'], self.accommodation_attributes['building_name'])
        self.assertEqual(data['availability_start'], str(self.accommodation_attributes['availability_start']))
        self.assertEqual(data['availability_end'], str(self.accommodation_attributes['availability_end']))
        self.assertEqual(data['managed_by'], self.accommodation_attributes['managed_by'])

    def test_accommodation_serializer_valid_data(self):
        """Test serializer with valid data for creation."""
        serializer = AccommodationSerializer(data=self.accommodation_attributes)
        self.assertTrue(serializer.is_valid())


class MemberSerializerTest(TestCase):
    def setUp(self):
        self.member_attributes = {
            'name': 'Test Member',
            'contact': '1234567890',
            'institute': 'Test Institute'
        }
        self.member = Member.objects.create(**self.member_attributes)
        self.serializer = MemberSerializer(instance=self.member)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'contact', 'institute'})

    def test_field_content(self):
        """Test the content of the serialized fields."""
        data = self.serializer.data
        self.assertEqual(data['name'], self.member_attributes['name'])
        self.assertEqual(data['contact'], self.member_attributes['contact'])
        self.assertEqual(data['institute'], self.member_attributes['institute'])

    def test_member_serializer_valid_data(self):
        """Test serializer with valid data for creation."""
        # Use different data than setUp to avoid potential unique constraint errors
        valid_data_for_creation = {
            'name': 'New Valid Member',
            'contact': '9876543210',
            'institute': 'New Valid Institute'
        }
        serializer = MemberSerializer(data=valid_data_for_creation)
        # Add raise_exception=True to get detailed validation errors on failure
        self.assertTrue(serializer.is_valid(raise_exception=True), msg=f"Serializer errors: {serializer.errors}")


class ReservationSerializerTest(TestCase):
    def setUp(self):
        self.accommodation = Accommodation.objects.create(
            flat_number='B',
            floor_number=2,
            building_name='Another Building',
            availability_start=datetime.date(2024, 1, 1),
            availability_end=datetime.date(2024, 12, 31),
            managed_by='Manager B'
        )
        self.member = Member.objects.create(
            name='Another Member',
            contact='0987654321',
            institute='Another Institute'
        )
        self.reservation_attributes = {
            'accommodation': self.accommodation.id,
            'start_date': datetime.date(2024, 6, 1),
            'end_date': datetime.date(2024, 8, 31),
            'member': self.member.id,
            'status': 'Not Signed'
        }
        self.reservation = Reservation.objects.create(
            accommodation=self.accommodation,
            start_date=datetime.date(2024, 6, 1),
            end_date=datetime.date(2024, 8, 31),
            member=self.member,
            status='Not Signed'
        )
        self.serializer = ReservationSerializer(instance=self.reservation)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'accommodation', 'start_date', 'end_date', 'member', 'status'})

    def test_field_content(self):
        """Test the content of the serialized fields."""
        data = self.serializer.data
        self.assertEqual(data['accommodation'], self.accommodation.id)
        self.assertEqual(data['start_date'], str(self.reservation_attributes['start_date']))
        self.assertEqual(data['end_date'], str(self.reservation_attributes['end_date']))
        self.assertEqual(data['member'], self.member.id)
        self.assertEqual(data['status'], self.reservation_attributes['status'])

    def test_reservation_serializer_valid_data(self):
        """Test serializer with valid data for creation."""
        # Use different data than setUp to avoid potential unique constraint errors
        # Ensure the combination of accommodation, start_date, end_date is unique
        valid_data_for_creation = {
            'accommodation': self.accommodation.id,
            'start_date': datetime.date(2024, 9, 1), # Different start date
            'end_date': datetime.date(2024, 9, 30),   # Different end date
            'member': self.member.id,
            'status': 'Signed' # Can also be different if needed
        }
        serializer = ReservationSerializer(data=valid_data_for_creation)
        self.assertTrue(serializer.is_valid(raise_exception=True), msg=f"Serializer errors: {serializer.errors}") # raise_exception provides more details on failure

class RatingSerializerTest(TestCase):
    def setUp(self):
        self.accommodation = Accommodation.objects.create(
            flat_number='C',
            floor_number=3,
            building_name='Rating Building',
            availability_start=datetime.date(2024, 1, 1),
            availability_end=datetime.date(2024, 12, 31),
            managed_by='Manager C'
        )
        self.member = Member.objects.create(
            name='Rating Member',
            contact='1122334455',
            institute='Rating Institute'
        )
        self.rating_attributes = {
            'accommodation': self.accommodation.id,
            'member': self.member.id,
            'rating': 5,
            'comment': 'Excellent!'
        }
        self.rating = Rating.objects.create(
            accommodation=self.accommodation,
            member=self.member,
            rating=5,
            comment='Excellent!'
        )
        self.serializer = RatingSerializer(instance=self.rating)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'accommodation', 'member', 'rating', 'comment'})

    def test_field_content(self):
        """Test the content of the serialized fields."""
        data = self.serializer.data
        self.assertEqual(data['accommodation'], self.accommodation.id)
        self.assertEqual(data['member'], self.member.id)
        self.assertEqual(data['rating'], self.rating_attributes['rating'])
        self.assertEqual(data['comment'], self.rating_attributes['comment'])
