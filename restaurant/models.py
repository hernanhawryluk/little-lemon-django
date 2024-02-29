from django.db import models

# Create your models here.

class OpeningHours(models.Model):
    days = models.CharField(max_length = 12)
    opening_hour = models.CharField(max_length = 6)
    closing_hour = models.CharField(max_length = 6)

    def __str__(self):
        return f'{self.days}: {self.opening_hour} - {self.closing_hour}'

