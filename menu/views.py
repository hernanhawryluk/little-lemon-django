from django.shortcuts import render
from . models import Menu

# Create your views here.

def menu(request):
    menus = Menu.objects.filter(category__slug = 'food')
    drinks = Menu.objects.filter(category__slug = 'drink')
    desserts = Menu.objects.filter(category__slug = 'dessert')
    return render(request, 'menu.html', {'menus': menus, 'drinks': drinks, 'desserts': desserts })

def menu_item(request, pk):
    item = Menu.objects.get(pk = pk)
    return render(request, 'menu-item.html', {'item': item })