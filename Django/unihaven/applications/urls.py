from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApplicationListView.as_view(), name='application-list'),
    path('<uuid:id>/', views.ApplicationDetailView.as_view(), name='application-detail'),
    path('create/', views.ApplicationCreateView.as_view(), name='application-create'),
    path('<uuid:id>/update/', views.ApplicationUpdateView.as_view(), name='application-update'),
    path('<uuid:id>/cancel/', views.ApplicationCancelView.as_view(), name='application-cancel'),
]