from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Booking
from .forms import BookingForm
from .serializers import BookingSerializer
from rest_framework import viewsets, permissions
from django.core.exceptions import ValidationError
from datetime import datetime

# Create your views here.

def booking_view(request):
    if request.method == 'POST':
        try:
            form = BookingForm(request.POST)
            new_booking = form.save(commit=False)
            new_booking.user = request.user
            new_booking.save()
            return redirect('successful_booking', pk=new_booking.pk)
        except ValidationError as e:
            errors = e.message_dict
        except ValueError:
            errors = 'Please provide valid data'
        except:
            errors = 'Something went wrong'
        return redirect('booking')

    if request.method == 'GET':
        errors = None
        form = BookingForm()
        bookings = Booking.objects.filter(user=request.user, date__gte=datetime.now().date()).order_by('date', 'time')
        return render(request, 'booking.html', {'form': BookingForm, 'errors': errors, 'bookings': bookings})
    
def successful_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'success.html', {'booking': booking})

def edit_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if request.method == 'GET':
        errors = None
        form = BookingForm(instance=booking)
        bookings = Booking.objects.filter(user=request.user, date__gte=datetime.now().date()).exclude(pk=pk).order_by('date', 'time')
        ordered_bookings = [booking] + list(bookings)
        return render(request, 'edit.html', {'form': form, 'errors': errors, 'bookings': ordered_bookings, 'editing': pk})
    
    if request.method == 'POST':
        if booking.user == request.user:
            try:
                form = BookingForm(request.POST, instance=booking)
                form.save()
                return redirect('booking')
            except ValidationError as e:
                errors = e.message_dict
            except ValueError:
                errors = 'Please provide valid data'
            except:
                errors = 'Something went wrong'
            return render(request, 'edit.html', {'form': form, 'errors': errors, 'bookings': bookings, 'editing': pk})
        
def delete_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        if(booking.user == request.user):
            booking.delete()
            return redirect('booking')
    
    return render(request, 'cancelation.html', {'booking': booking})

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