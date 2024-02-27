from django.forms import ModelForm
from .models import Booking
from django import forms

class BookingForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    guests = forms.IntegerField(initial=1, min_value=1, max_value=12)

    class Meta:
        model = Booking
        fields = ['date', 'time', 'guests', 'occasion']