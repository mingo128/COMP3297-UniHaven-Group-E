from django.db import models
import uuid

class Accommodation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Accommodation_invisible = models.BooleanField(default=False)
    TYPE_CHOICES = [
        ('Single_Room', 'Single Room'),
        ('Shared_Room', 'Shared Room'),
        ('Apartment', 'Apartment'),
    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    period_of_availability = models.CharField(max_length=50)
    number_of_rooms_available = models.IntegerField()
    price = models.FloatField()
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    amenities = models.JSONField()  # List of amenities
    photos = models.JSONField()  # List of URLs to images
    landlord_id = models.UUIDField()
    availability_calendar = models.JSONField()  # List of dates
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} in {self.location}"


class RatingReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    user_id = models.UUIDField()
    overall_rating = models.IntegerField(choices=[(i, i) for i in range(6)])  # 0-5
    value_for_money = models.IntegerField(choices=[(i, i) for i in range(6)])  # 0-5
    location_convenience = models.IntegerField(choices=[(i, i) for i in range(6)])  # 0-5
    property_condition = models.IntegerField(choices=[(i, i) for i in range(6)])  # 0-5
    landlord_communication = models.IntegerField(choices=[(i, i) for i in range(6)])  # 0-5
    review_text = models.TextField(blank=True, null=True)
    photos = models.JSONField(blank=True, null=True)  # List of URLs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.accommodation} by {self.user_id}"