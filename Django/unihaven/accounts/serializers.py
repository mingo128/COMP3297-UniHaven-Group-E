from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Specify the fields you want to include in the API for regular users
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined'] # Example fields

class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Specify the fields you want to include for landlords
        # This might be the same as UserSerializer or include additional fields
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined'] # Example fields
        # Add any landlord-specific fields if they exist on the User model