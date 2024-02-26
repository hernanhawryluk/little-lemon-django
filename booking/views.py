from django.shortcuts import render
from django.http import JsonResponse
from .models import Booking
from .forms import BookingForm
from .serializers import BookingSerializer
from rest_framework import viewsets, permissions
from django.core.exceptions import ValidationError

# Create your views here.

def booking_view(request):
    errors = None
    form = BookingForm()
    bookings = Booking.objects.all()

    if request.method == 'POST':
        try:
            form = BookingForm(request.POST)
            new_booking = form.save(commit=False)
            new_booking.user = request.user
            new_booking.save()
        except ValidationError as e:
            errors = e.message_dict
        except ValueError:
            errors = 'Please provide valid data'
        except:
            errors = 'Something went wrong'

    return render(request, 'booking.html', {'form': BookingForm, 'errors': errors, 'bookings': bookings})
    
# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all()
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def perform_update(self, serializer):
#         if self.get_object().user == self.request.user:
#             serializer.save()
    
#     def perform_destroy(self, instance):
#         if instance.user == self.request.user:
#             instance.delete()