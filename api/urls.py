from django.urls import path
from .views import BookingListCreateView, BookingRetrieveUpdateDestroyView
from . import views 

urlpatterns = [
    path('login', views.login),
    path('signup', views.signup),
    path('test-token', views.test_token),

    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking-retrieve-update-destroy'),
]