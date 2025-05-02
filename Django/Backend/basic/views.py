from rest_framework import viewsets, filters
from .models import Accommodation, Member, Reservation, Rating
from .serializers import AccommodationSerializer, MemberSerializer, ReservationSerializer, RatingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class AccommodationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accommodations to be viewed or edited.
    """
    queryset = Accommodation.objects.all().order_by('building_name', 'floor_number', 'flat_number')
    serializer_class = AccommodationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['building_name', 'managed_by']

    @action(detail=False, methods=['get'])
    def ranked_by_distance(self, request):
        """
        Custom action to get accommodations ranked by distance to campus.
        """
        reversed = request.query_params.get('reverse', 'false').lower() == 'true'
        order = '-distance_to_campus' if reversed else 'distance_to_campus'
        queryset = self.queryset.order_by(order)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows members to be viewed or edited.
    """
    queryset = Member.objects.all().order_by('name')
    serializer_class = MemberSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'contact', 'institute']

class ReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reservations to be viewed or edited.
    """
    queryset = Reservation.objects.all().order_by('start_date')
    serializer_class = ReservationSerializer
    # Add filtering capabilities if needed
    # filterset_fields = ['accommodation', 'member', 'status', 'start_date', 'end_date']
    filter_backends = [filters.SearchFilter]
    search_fields = ['accommodation__building_name', 'member__name', 'status']
    @action(detail=False, methods=['get'])
    def get_Unsigned_reservations(self, request):
        """
        Custom action to get reservations that are signed.
        """
        unsigned = request.query_params.get('unsigned', 'false').lower() == 'true'
        whether_signed = 'Signed' if unsigned else 'Not Signed'
        queryset = self.queryset.filter(status=whether_signed).order_by('start_date')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class RatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ratings to be viewed or edited.
    """
    queryset = Rating.objects.all().order_by('-rating')
    serializer_class = RatingSerializer
    # Add filtering capabilities if needed
    # filterset_fields = ['accommodation', 'member', 'rating']
    filter_backends = [filters.SearchFilter]
    search_fields = ['accommodation__building_name', 'member__name', 'rating']

    # ranked_by_rating
    @action(detail=False, methods=['get'])
    def ranked_by_rating(self, request):
        """
        Custom action to get ratings ranked by rating value.
        """
        reverse = request.query_params.get('reverse', 'false').lower() == 'true'
        order = 'rating' if reverse else '-rating'
        queryset = self.queryset.order_by(order)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)