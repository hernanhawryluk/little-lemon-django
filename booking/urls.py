from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required
# from .views import BookingViewSet
from . import views

# router = DefaultRouter()
# router.register('booking', BookingViewSet, basename='booking')

urlpatterns = [
    path('booking/', login_required(views.booking_view), name='booking'),
    # path('booking/', include(router.urls)),
]