from rest_framework import serializers
from .models import Accommodation, RatingReview

class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = '__all__'

class RatingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingReview
        fields = '__all__'