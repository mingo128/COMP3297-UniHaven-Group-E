from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApplicationViewSet.as_view({'get': 'list'}), name='application-list'),
    path('<uuid:id>/', views.ApplicationViewSet.as_view({'get': 'retrieve'}), name='application-detail'),
    path('create/', views.ApplicationViewSet.as_view({'post': 'create'}), name='application-create'),
    path('<uuid:id>/update/', views.ApplicationViewSet.as_view({'put': 'update'}), name='application-update'),
    path('<uuid:id>/cancel/', views.ApplicationViewSet.as_view({'post': 'cancel'}), name='application-cancel'),
]