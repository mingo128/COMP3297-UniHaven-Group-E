from django.urls import path
from . import views

urlpatterns = [
    path('', views.AccommodationListView.as_view(), name='accommodation-list'),
    path('<uuid:id>/', views.AccommodationDetailView.as_view(), name='accommodation-detail'),
    path('create/', views.AccommodationCreateView.as_view(), name='accommodation-create'),
    path('<uuid:id>/update/', views.AccommodationUpdateView.as_view(), name='accommodation-update'),
    path('<uuid:id>/delete/', views.AccommodationDeleteView.as_view(), name='accommodation-delete'),
]