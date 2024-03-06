from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required
from .views import BookingListCreateView, BookingRetrieveUpdateDestroyView
from . import views

urlpatterns = [
    path('booking/', login_required(views.booking_view), name='booking'),
    path('booking/success/<int:pk>', login_required(views.successful_booking_view), name='successful_booking'),
    path('booking/edit/<int:pk>', login_required(views.edit_booking_view), name='edit_booking'),
    path('booking/delete/<int:pk>', login_required(views.delete_booking_view), name='delete_booking'),
    
    path('api/booking/', BookingListCreateView.as_view()),
    path('api/booking/<int:pk>/', BookingRetrieveUpdateDestroyView.as_view()),
]