from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

User = get_user_model()

# Create your models here.
class Booking(models.Model):
    occasion_choices = [
        ('Casual', 'Casual'),
        ('Birthday', 'Birthday'),
        ('Anniversary', 'Anniversary'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.SmallIntegerField(default = 1)
    occasion = models.CharField(max_length = 12, choices=occasion_choices , default = 'Casual')
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return f'{self.user.username} booked {self.guests} seats on {self.date} for {self.time}'
    
    def clean(self):
        super().clean()

        today = datetime.now().date()
        if self.date == today and self.time < datetime.now().time():
            raise ValidationError({'time': 'Time must be in the future'})
        
        if self.date < today:
            raise ValidationError({'date': 'Date must be in the future'})
        elif self.date > today + timedelta(days=180):
            raise ValidationError({'date': 'Date must be within 6 months'})

        if self.guests < 1:
            raise ValidationError({'guests': 'Guests must be at least 1'})
        elif self.guests > 12:
            raise ValidationError({'guests': 'Guests must be at most 12'})