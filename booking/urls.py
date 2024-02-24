from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet

router = DefaultRouter()
router.register('booking', BookingViewSet, basename='booking')

urlpatterns = [
    path('booking/', include(router.urls)),
]