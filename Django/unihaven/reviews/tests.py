import pytest
from django.db import IntegrityError
from .models import RatingReview
from accommodations.models import Accommodation
from accounts.models import User

@pytest.mark.django_db
def test_rating_review_creation_and_str():
    # Create a dummy Accommodation.
    # Adjust the creation parameters according to your Accommodation model's requirements.
    accommodation = Accommodation.objects.create(
        type='Apartment'
    )

    # Create a dummy User.
    # Adjust the creation parameters according to your User model's requirements.
    user = User.objects.create(
        username='testuser',
        name='Test User'
    )

    # Create a RatingReview instance.
    review = RatingReview.objects.create(
        accommodation=accommodation,
        user=user,
        overall_rating=4,
        value_for_money=4,
        location_convenience=5,
        property_condition=4,
        landlord_communication=5,
        review_text='Great place to stay!',
        photos=['url1', 'url2']
    )

    # Check that the fields are set correctly.
    assert review.overall_rating == 4
    assert review.review_text == 'Great place to stay!'

    # Check the string representation.
    expected_str = f"Review by {user.name} for {accommodation.type}"
    assert str(review) == expected_str

@pytest.mark.django_db
def test_rating_review_invalid_data():
    # Create dummy Accommodation and User.
    accommodation = Accommodation.objects.create(
        type='Apartment'
    )
    user = User.objects.create(
        username='testuser2',
        name='Another User'
    )

    # Attempt to create a RatingReview with an invalid overall_rating value.
    with pytest.raises(IntegrityError):
        RatingReview.objects.create(
            accommodation=accommodation,
            user=user,
            overall_rating=6,  # outside the valid range 0-5
            value_for_money=4,
            location_convenience=5,
            property_condition=4,
            landlord_communication=5,
            review_text='Invalid rating test',
            photos=['url3']
        )