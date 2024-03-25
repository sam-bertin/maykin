from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('hotels/', views.hotels_by_city, name='hotels_by_city'),
]