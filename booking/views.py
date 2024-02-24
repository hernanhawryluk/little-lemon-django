from django.http import JsonResponse
from .models import Booking
from .serializers import BookingSerializer
from rest_framework import viewsets, permissions

# Create your views here.
    
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().user == self.request.user:
            serializer.save()
    
    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()