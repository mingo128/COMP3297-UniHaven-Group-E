from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from .models import Accommodation, Member

@pytest.mark.django_db
def test_accommodation_list():
    client = APIClient()
    url = reverse('accommodation-list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_ranked_by_distance():
    client = APIClient()
    url = reverse('accommodation-ranked-by-distance')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_member():
    client = APIClient()
    url = reverse('member-list')
    data = {
        "name": "Test User",
        "contact": "1234567890",
        "institute": "HKU"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['name'] == "Test User"