from rest_framework import serializers
from .models import Accommodation, Member, Reservation, Rating

class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = '__all__' # Include all fields from the model

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    # Optionally display related object details instead of just IDs
    # accommodation = AccommodationSerializer(read_only=True)
    # member = MemberSerializer(read_only=True)
    # accommodation_id = serializers.PrimaryKeyRelatedField(queryset=Accommodation.objects.all(), source='accommodation', write_only=True)
    # member_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), source='member', write_only=True)

    class Meta:
        model = Reservation
        fields = '__all__' # Or specify fields: ['id', 'accommodation', 'start_date', 'end_date', 'member', 'status']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__' # Or specify fields: ['id', 'accommodation', 'member', 'rating', 'comment']