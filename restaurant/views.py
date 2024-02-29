from django.shortcuts import render
from menu.models import Menu
from .models import OpeningHours


# Create your views here.
def home(request):
    opening_hours = OpeningHours.objects.all()
    menus = Menu.objects.filter(category__slug='food').order_by('?')[:4]
    return render(request, 'index.html', {'menus' : menus, 'opening_hours': opening_hours})

def about(request):
    return render(request, 'about.html', {})