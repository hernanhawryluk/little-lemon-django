from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

User = get_user_model()

# Create your models here.
class Booking(models.Model):
    def validate_date(value):
        today = datetime.now().date()
        six_months_from_now = today + timedelta(days=180)

        if value < today:
            raise ValidationError('Date must be in the future')
        elif value > six_months_from_now:
            raise ValidationError('Date must be within 6 months')

    def validate_time(value):
        if value < datetime.now().time():
            raise ValidationError('Time must be in the future')
        
    def validate_guests(value):
        if value < 1:
            raise ValidationError('Guests must be at least 1')
        elif value > 12:
            raise ValidationError('Guests must be at most 12')
    
    occasion_choices = [
        ('Casual', 'Casual'),
        ('Birthday', 'Birthday'),
        ('Anniversary', 'Anniversary'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(validators=[validate_date])
    time = models.TimeField(validators=[validate_time])
    guests = models.SmallIntegerField(validators=[validate_guests] , default = 1)
    occasion = models.CharField(max_length = 12, choices=occasion_choices , default = 'Casual')
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return f'{self.user.username} booked {self.guests} seats on {self.date} for {self.time}'