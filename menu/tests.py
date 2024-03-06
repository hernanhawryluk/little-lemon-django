from django.test import TestCase, RequestFactory
from django.urls import reverse
from menu.models import Category, Menu, Review
from users.tests import TestUserSetUp

from rest_framework.test import RequestsClient

class TestMenuSetUp(TestUserSetUp):
    def setUp(self):
        super().setUp()
        category_food = Category.objects.create(name='Food', slug='food')
        category_food_2 = Category.objects.create(name='Dessert', slug='dessert')
        category_food_3 = Category.objects.create(name='Drink', slug='drink')

        self.menu_1 = Menu.objects.create(name='Bruschetta', slug='bruschetta', description='Our Bruschetta is made from grilled bread that has been smeared with garlic, seasoned with salt, and drizzled with olive oil, creating a delightful appetizer.', image='http://127.0.0.1:8000/media/images/bruschetta.webp', price='5.99', stock=True, category=category_food)
        Menu.objects.create(name='Bruschetta', slug='bruschetta', description='Our Bruschetta is made from grilled bread that has been smeared with garlic, seasoned with salt, and drizzled with olive oil, creating a delightful appetizer.', image='http://127.0.0.1:8000/media/images/bruschetta.webp', price='5.99', stock=True, category=category_food)
        Menu.objects.create(name='Bruschetta', slug='bruschetta', description='Our Bruschetta is made from grilled bread that has been smeared with garlic, seasoned with salt, and drizzled with olive oil, creating a delightful appetizer.', image='http://127.0.0.1:8000/media/images/bruschetta.webp', price='5.99', stock=True, category=category_food)
        Menu.objects.create(name='Bruschetta', slug='bruschetta', description='Our Bruschetta is made from grilled bread that has been smeared with garlic, seasoned with salt, and drizzled with olive oil, creating a delightful appetizer.', image='http://127.0.0.1:8000/media/images/bruschetta.webp', price='5.99', stock=True, category=category_food)
        Menu.objects.create(name='Lemon Dessert', slug='lemon-dessert', description='This comes straight from grandma’s cherished recipe book, every last ingredient has been sourced and is as authentic and nostalgic as can be imagined.', image='http://127.0.0.1:8000/media/images/lemon-dessert.webp', price='2.00', stock=True, category=category_food_2)
        Menu.objects.create(name='"Mediterranean Wine"', slug='mediterranean-wine', description='Crafted from the sun-soaked vines of the Mediterranean, this wine embodies tradition and authenticity. Each grape tells a story, evoking the rich heritage of winemaking.', image='http://127.0.0.1:8000/media/images/wine.webp', price='2.00', stock=True, category=category_food_3)

class RenderViewTest(TestMenuSetUp):
    def test_menu_view(self):
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
        self.assertEqual(len(response.context['menus']), 4)
        self.assertEqual(len(response.context['desserts']), 1)
        self.assertEqual(len(response.context['drinks']), 1)

    def test_item_view(self):
        Review.objects.create(menu=self.menu_1, user=self.user, rating=4, comment='Good item!')
        Review.objects.create(menu=self.menu_1, user=self.user, rating=5, comment='Excellent item!')

        factory = RequestFactory()
        response = self.client.get(reverse('item', args=[str(self.menu_1.pk)]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu-item.html')




