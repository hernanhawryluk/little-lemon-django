from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from .forms import BookingForm
from .serializers import BookingSerializer
from django.core.exceptions import ValidationError
from datetime import datetime
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

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


class BookingListCreateView(ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Booking.objects.filter(user = self.request.user)
        else:
            return Booking.objects.none()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user = self.request.user)
        else:
             raise PermissionDenied(detail='Not authorized', code=status.HTTP_401_UNAUTHORIZED)


class BookingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Booking, pk=pk, user=self.request.user)