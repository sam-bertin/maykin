from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
from .views import ManagerView, HotelDeleteView, HotelUpdateView, HotelCreateView

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('hotels/', views.hotels_by_city, name='hotels_by_city'),
    path('hotels/create/', HotelCreateView.as_view(), name='hotel_create'),
    path('hotels/<int:pk>/update/', HotelUpdateView.as_view(), name='hotel_update'),
    path('hotels/<int:pk>/delete/', HotelDeleteView.as_view(), name='hotel_delete'),
    path('manager/', login_required(ManagerView.as_view()), name='manager_view'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]