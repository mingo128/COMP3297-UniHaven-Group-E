from rest_framework import viewsets
from .models import RatingReview
from .serializers import RatingReviewSerializer

class RatingReviewViewSet(viewsets.ModelViewSet):
    queryset = RatingReview.objects.all()
    serializer_class = RatingReviewSerializer

    def perform_create(self, serializer):
        serializer.save()