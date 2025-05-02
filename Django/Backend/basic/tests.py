import datetime
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Accommodation, Member, Reservation, Rating

class AccommodationAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.accommodation_attributes = {
            'room_number': 101,
            'flat_number': 'A',
            'floor_number': 1,
            'building_name': 'Sha Tin Hall',
            'availability_start': '2024-01-01',
            'availability_end': '2024-12-31',
            'managed_by': 'Test Manager'
        }
        self.accommodation = Accommodation.objects.create(**{
            **self.accommodation_attributes,
            'availability_start': datetime.date(2024, 1, 1),
            'availability_end': datetime.date(2024, 12, 31),
        })

    def test_accommodation_list(self):
        url = reverse('accommodation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(acc['id'] == self.accommodation.id for acc in response.data))

    def test_accommodation_detail(self):
        url = reverse('accommodation-detail', args=[self.accommodation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['room_number'], self.accommodation_attributes['room_number'])

    def test_accommodation_create(self):
        url = reverse('accommodation-list')
        data = {
            'room_number': 102,
            'flat_number': 'B',
            'floor_number': 2,
            'building_name': 'University Hall The University of Hong Kong',
            'availability_start': '2024-02-01',
            'availability_end': '2024-11-30',
            'managed_by': 'Manager B',
            'latitude': 22.3964,
            'longitude': 114.1095,
            'distance_to_campus': 1.5
        }
        response = self.client.post(url, data, format='json')
        print(response.data)  # Print the response for debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['room_number'], 102)
        

class MemberAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.member_attributes = {
            'name': 'Test Member',
            'contact': '1234567890',
            'institute': 'Test Institute'
        }
        self.member = Member.objects.create(**self.member_attributes)

    def test_member_list(self):
        url = reverse('member-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(m['id'] == self.member.id for m in response.data))

    def test_member_detail(self):
        url = reverse('member-detail', args=[self.member.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.member_attributes['name'])

    def test_member_create(self):
        url = reverse('member-list')
        data = {
            'name': 'New Member',
            'contact': '9876543210',
            'institute': 'New Institute'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Member')

class ReservationAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.accommodation = Accommodation.objects.create(
            room_number=201,
            flat_number='C',
            floor_number=3,
            building_name='Swire Hall The University of Hong Kong',
            availability_start=datetime.date(2024, 1, 1),
            availability_end=datetime.date(2024, 12, 31),
            managed_by='Manager C'
        )
        self.member = Member.objects.create(
            name='Res Member',
            contact='1112223333',
            institute='Res Institute'
        )
        self.reservation_attributes = {
            'accommodation': self.accommodation.id,
            'start_date': '2024-06-01',
            'end_date': '2024-08-31',
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

    def test_reservation_list(self):
        url = reverse('reservation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(r['id'] == self.reservation.id for r in response.data))

    def test_reservation_detail(self):
        url = reverse('reservation-detail', args=[self.reservation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], self.reservation_attributes['status'])

    def test_reservation_create(self):
        url = reverse('reservation-list')
        data = {
            'accommodation': self.accommodation.id,
            'start_date': '2024-09-01',
            'end_date': '2024-09-30',
            'member': self.member.id,
            'status': 'Signed'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'Signed')

class RatingAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.accommodation = Accommodation.objects.create(
            room_number=301,
            flat_number='D',
            floor_number=4,
            building_name='Lungga Mansion Kennedy Town',
            availability_start=datetime.date(2024, 1, 1),
            availability_end=datetime.date(2024, 12, 31),
            managed_by='Manager D'
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

    def test_rating_list(self):
        url = reverse('rating-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(r['id'] == self.rating.id for r in response.data))

    def test_rating_detail(self):
        url = reverse('rating-detail', args=[self.rating.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment'], self.rating_attributes['comment'])

    def test_rating_create(self):
        url = reverse('rating-list')
        new_member = Member.objects.create(
            name='New Rating Member',
            contact='9988776655',
            institute='New Rating Institute'
        )
        data = {
            'accommodation': self.accommodation.id,
            'member': new_member.id,
            'rating': 4,
            'comment': 'Very good!'
        }
        response = self.client.post(url, data, format='json')
        #print the response for debugging
        print(data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 4)