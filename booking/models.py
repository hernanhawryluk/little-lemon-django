from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.SmallIntegerField()
    guests = models.SmallIntegerField(default = 1)
    occasion = models.CharField(max_length = 12, default = 'Casual')

    def __str__(self) -> str:
        return f'{self.user} booked {self.guests} on {self.date} for {self.time}'