from django.test import TestCase
from .models import Accommodation, RatingReview
import uuid

class AccommodationModelTest(TestCase):

    def setUp(self):
        self.accommodation = Accommodation.objects.create(
            type='Single_Room',
            period_of_availability='Yearly',
            number_of_rooms_available=5,
            Accommodation_invisible=False,
            price=1500.00,
            location='Swire Hall',
            latitude=22.3000000,
            longitude=114.2000000,
            amenities=['WiFi', 'Air Conditioning'],
            photos=['url1', 'url2'],
            landlord_id=uuid.uuid4(),
            availability_calendar=['2024-01-01', '2024-01-02'],
            description='A single room in Swire Hall.'
        )

    def test_accommodation_creation(self):
        accommodation = Accommodation.objects.get(location='Swire Hall')
        self.assertEqual(accommodation.type, 'Single_Room')
        self.assertEqual(accommodation.price, 1500.00)
        self.assertFalse(accommodation.Accommodation_invisible)

    def test_accommodation_str(self):
        accommodation = Accommodation.objects.get(location='Swire Hall')
        self.assertEqual(str(accommodation), 'Single_Room in Swire Hall')

    def test_accommodation_fields(self):
        accommodation = Accommodation.objects.get(location='Swire Hall')
        self.assertEqual(len(accommodation.amenities), 2)
        self.assertEqual(len(accommodation.photos), 2)
        self.assertIsNotNone(accommodation.landlord_id)
        self.assertEqual(len(accommodation.availability_calendar), 2)

class RatingReviewModelTest(TestCase):
    def setUp(self):
        self.accommodation = Accommodation.objects.create(
            type='Single_Room',
            period_of_availability='Yearly',
            number_of_rooms_available=1,
            price=1000.00,
            location='Test Location',
            latitude=22.0,
            longitude=114.0,
            amenities=[],
            photos=[],
            landlord_id=uuid.uuid4(),
            availability_calendar=[],
            description='Test description'
        )
        
        self.review = RatingReview.objects.create(
            accommodation=self.accommodation,
            user_id=uuid.uuid4(),
            overall_rating=4,
            value_for_money=4,
            location_convenience=5,
            property_condition=3,
            landlord_communication=5,
            review_text='Great place!',
            photos=['review_photo1.jpg']
        )

    def test_review_creation(self):
        review = RatingReview.objects.get(accommodation=self.accommodation)
        self.assertEqual(review.overall_rating, 4)
        self.assertEqual(review.review_text, 'Great place!')