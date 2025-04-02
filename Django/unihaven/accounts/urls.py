from django.urls import path
from . import views

urlpatterns = [
    path('users/<str:id>/', views.UserDetailView.as_view(), name='user_detail'),
    path('landlords/<str:id>/', views.LandlordDetailView.as_view(), name='landlord_detail'),
]