from django.shortcuts import render, get_object_or_404
from django.views import View
from . models import Menu, Review

# Create your views here.

def menu(request):
    menus = Menu.objects.filter(category__slug = 'food')
    drinks = Menu.objects.filter(category__slug = 'drink')
    desserts = Menu.objects.filter(category__slug = 'dessert')
    return render(request, 'menu.html', {'menus': menus, 'drinks': drinks, 'desserts': desserts })

def menu_item(request, pk):
    item = get_object_or_404(Menu, pk = pk)
    average_rating = item.average_rating()
    total_reviews = item.total_reviews()
    reviews = Review.objects.filter(menu = pk).order_by('?')[:2]
    return render(request, 'menu-item.html', {'item': item, 'reviews': reviews, 'average_rating': average_rating, 'total_reviews': total_reviews})

class ReviewView(View):
    model = Review

    # def get(self, request):
    #     data = json.loads(request.body)
