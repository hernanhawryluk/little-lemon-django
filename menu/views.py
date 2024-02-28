from django.shortcuts import render
from . models import Menu

# Create your views here.

def menu(request):
    items = Menu.objects.all()
    return render(request, 'menu.html', {'items': items })