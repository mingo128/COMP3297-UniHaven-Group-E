from rest_framework import serializers
from .models import RatingReview

class RatingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingReview
        fields = '__all__'  # or specify the fields you want to include explicitly