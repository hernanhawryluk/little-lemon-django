from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    phone = models.CharField(max_length = 30, db_index = True)
    address = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255, db_index = True)

class OpeningHours(models.Model):
    days = models.CharField(max_length = 12)
    opening_hour = models.CharField(max_length = 6)
    closing_hour = models.CharField(max_length = 6)

    def __str__(self):
        return f'{self.days}: {self.opening_hour} - {self.closing_hour}'

