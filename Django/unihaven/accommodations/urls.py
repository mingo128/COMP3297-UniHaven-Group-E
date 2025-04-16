from django.urls import path
from . import views

urlpatterns = [
    path('', views.AccommodationViewSet.as_view({'get': 'list', 'post': 'create'}), name='accommodation-list-create'),
    path('<uuid:id>/', views.AccommodationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='accommodation-detail'),
]