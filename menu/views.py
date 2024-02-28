from django.shortcuts import render
from . models import Menu

# Create your views here.

def menu(request):
    menus = Menu.objects.all()
    return render(request, 'menu.html', {'menus': menus })