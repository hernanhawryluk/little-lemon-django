from django.contrib import admin
from .models import Customer, OpeningHours

# Register your models here.
admin.site.register(Customer)
admin.site.register(OpeningHours)
