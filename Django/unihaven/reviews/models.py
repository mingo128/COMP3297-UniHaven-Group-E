from django.db import models
from accommodations.models import Accommodation
from accounts.models import User

class RatingReview(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    overall_rating = models.IntegerField(choices=[(i, str(i)) for i in range(6)])  # 0-5 rating
    value_for_money = models.IntegerField(choices=[(i, str(i)) for i in range(6)])  # 0-5 rating
    location_convenience = models.IntegerField(choices=[(i, str(i)) for i in range(6)])  # 0-5 rating
    property_condition = models.IntegerField(choices=[(i, str(i)) for i in range(6)])  # 0-5 rating
    landlord_communication = models.IntegerField(choices=[(i, str(i)) for i in range(6)])  # 0-5 rating
    review_text = models.TextField(blank=True, null=True)
    photos = models.JSONField(blank=True, null=True)  # Store URLs as a JSON array
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review by {self.user.name} for {self.accommodation.type}'