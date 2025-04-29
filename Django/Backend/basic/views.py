from rest_framework import viewsets
from .models import Accommodation, Member, Reservation, Rating
from .serializers import AccommodationSerializer, MemberSerializer, ReservationSerializer, RatingSerializer

class AccommodationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accommodations to be viewed or edited.
    """
    queryset = Accommodation.objects.all().order_by('building_name', 'floor_number', 'flat_number')
    serializer_class = AccommodationSerializer

class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows members to be viewed or edited.
    """
    queryset = Member.objects.all().order_by('name')
    serializer_class = MemberSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reservations to be viewed or edited.
    """
    queryset = Reservation.objects.all().order_by('start_date')
    serializer_class = ReservationSerializer
    # Add filtering capabilities if needed
    # filterset_fields = ['accommodation', 'member', 'status', 'start_date', 'end_date']

class RatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ratings to be viewed or edited.
    """
    queryset = Rating.objects.all().order_by('-rating')
    serializer_class = RatingSerializer
    # Add filtering capabilities if needed
    # filterset_fields = ['accommodation', 'member', 'rating']