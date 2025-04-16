from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'ratings', views.RatingReviewViewSet, basename='rating')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    # The following paths are commented out because RatingReviewViewSet
    # provides standard CRUD endpoints at /ratings/ and /ratings/{pk}/.
    # If you need custom paths like below, you'll need to create
    # different views (e.g., APIView or custom ViewSet actions)
    # path('accommodations/<uuid:accommodation_id>/ratings/', views.RatingListCreateView.as_view(), name='rating-list-create'),
    # path('users/<uuid:user_id>/ratings/', views.UserRatingListView.as_view(), name='user-rating-list'),
]