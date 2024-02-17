from django.db import models

# Create your models here.
class Booking(models.Model):
    name = models.CharField(max_length = 255)
    no_of_guests = models.IntegerField()
    booking_date = models.DateField()

    def __str__(self) -> str:
        return f'{self.name} booked {self.no_of_guests} on {self.booking_date}'

class Menu(models.Model):
    title = models.CharField(max_length = 255, db_index = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, db_index = True)
    inventory = models.IntegerField()

    def __str__(self):
        return f'{self.title} : {str(self.price)}'
