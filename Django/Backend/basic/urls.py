from django.urls import path, include
from rest_framework.routers import DefaultRouter # <--- This is the key
from .views import AccommodationViewSet, MemberViewSet, ReservationViewSet, RatingViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter() # <--- You created an instance here
router.register(r'accommodations', AccommodationViewSet)
router.register(r'members', MemberViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'ratings', RatingViewSet) # Register the RatingViewSet
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)), # <--- You included the router's URLs here
]