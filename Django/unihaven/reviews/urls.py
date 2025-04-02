from django.urls import path
from . import views

urlpatterns = [
    path('accommodations/<uuid:accommodation_id>/ratings/', views.RatingListCreateView.as_view(), name='rating-list-create'),
    path('ratings/<uuid:pk>/', views.RatingDetailView.as_view(), name='rating-detail'),
    path('users/<uuid:user_id>/ratings/', views.UserRatingListView.as_view(), name='user-rating-list'),
]