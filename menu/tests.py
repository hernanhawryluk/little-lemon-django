from django.test import TestCase
from django.urls import reverse
from menu.models import Category, Menu, Review
from users.tests import TestUserSetUp
from django.forms.models import model_to_dict

from rest_framework.test import RequestsClient

class TestMenuSetUp(TestUserSetUp):
    def setUp(self):
        super().setUp()
        category_food = Category.objects.create(name='Food', slug='food')
        category_food_2 = Category.objects.create(name='Dessert', slug='dessert')
        category_food_3 = Category.objects.create(name='Drink', slug='drink')

        self.menu_1 = Menu.objects.create(name='Bruschetta', slug='bruschetta', description='Our Bruschetta is made from grilled bread that has been smeared with garlic, seasoned with salt, and drizzled with olive oil, creating a delightful appetizer.', image='http://127.0.0.1:8000/media/images/bruschetta.webp', price='5.99', stock=True, category=category_food)
        self.menu_2 = Menu.objects.create(name='Bruschetta', slug='bruschetta', description='Our Bruschetta is made from grilled bread that has been smeared with garlic, seasoned with salt, and drizzled with olive oil, creating a delightful appetizer.', image='http://127.0.0.1:8000/media/images/bruschetta.webp', price='5.99', stock=True, category=category_food)
        Menu.objects.create(name='Bruschetta', slug='bruschetta', description='Our Bruschetta is made from grilled bread that has been smeared with garlic, seasoned with salt, and drizzled with olive oil, creating a delightful appetizer.', image='http://127.0.0.1:8000/media/images/bruschetta.webp', price='5.99', stock=True, category=category_food)
        Menu.objects.create(name='Bruschetta', slug='bruschetta', description='Our Bruschetta is made from grilled bread that has been smeared with garlic, seasoned with salt, and drizzled with olive oil, creating a delightful appetizer.', image='http://127.0.0.1:8000/media/images/bruschetta.webp', price='5.99', stock=True, category=category_food)
        Menu.objects.create(name='Lemon Dessert', slug='lemon-dessert', description='This comes straight from grandma’s cherished recipe book, every last ingredient has been sourced and is as authentic and nostalgic as can be imagined.', image='http://127.0.0.1:8000/media/images/lemon-dessert.webp', price='2.00', stock=True, category=category_food_2)
        Menu.objects.create(name='"Mediterranean Wine"', slug='mediterranean-wine', description='Crafted from the sun-soaked vines of the Mediterranean, this wine embodies tradition and authenticity. Each grape tells a story, evoking the rich heritage of winemaking.', image='http://127.0.0.1:8000/media/images/wine.webp', price='2.00', stock=True, category=category_food_3)

        self.review_1 = Review.objects.create(menu=self.menu_1, user=self.user, rating=4, comment='Good item!')
        Review.objects.create(menu=self.menu_1, user=self.user, rating=5, comment='Excellent item!')

class RenderViewTest(TestMenuSetUp):
    def test_menu_view(self):
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
        self.assertEqual(len(response.context['menus']), 4)
        self.assertEqual(len(response.context['desserts']), 1)
        self.assertEqual(len(response.context['drinks']), 1)

    def test_item_view(self):
        response = self.client.get(reverse('item', args=[str(self.menu_1.pk)]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu-item.html')
        self.assertEqual(response.context['item'], self.menu_1)
        self.assertEqual(len(response.context['reviews']), 2)


class APIViewTest(TestMenuSetUp):
    client = RequestsClient()
    def test_menus_view(self):
        response = self.client.get('http://127.0.0.1:8000/api/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 6)

    def test_menu_view(self):
        response = self.client.get('http://127.0.0.1:8000/api/menu/' + str(self.menu_1.pk) + "/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.menu_1.name)
        self.assertEqual(response.data['description'], self.menu_1.description)

    def test_reviews_view_without_credentials(self):
        response = self.client.get('http://127.0.0.1:8000/api/review/?menu=' + str(self.menu_1.pk))
        self.assertEqual(response.status_code, 401)

    def test_reviews_view_with_credentials(self):
        response = self.client.get('http://127.0.0.1:8000/api/review/?menu=' + str(self.menu_1.pk), headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_write_a_review_without_credentials(self):
        response = self.client.post('http://127.0.0.1:8000/api/review/')
        self.assertEqual(response.status_code, 401)

    def test_write_a_review_with_credentials_but_no_data(self):
        response = self.client.post('http://127.0.0.1:8000/api/review/', headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, 400)

    def test_write_a_review_with_all_requiered_data(self):
        response = self.client.post('http://127.0.0.1:8000/api/review/', {
            'menu': self.menu_2.pk,
            'rating': 5,
            'comment': 'Excellent item!'
        }, headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Review.objects.filter(menu=self.menu_2, user=self.user, rating=5, comment='Excellent item!').count(), 1)

    def test_write_a_review_more_than_once(self):
        response = self.client.post('http://127.0.0.1:8000/api/review/', {
            'menu': self.menu_1.pk,
            'rating': 5,
            'comment': 'Excellent item!'
        }, headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, 400)

    def test_edit_a_review_without_credentials(self):
        response = self.client.post('http://127.0.0.1:8000/api/review/', {
            'menu': self.menu_2.pk,
            'rating': 5,
            'comment': 'Excellent item!'
        })
        self.assertEqual(response.status_code, 401)

    def test_edit_a_review_with_all_requiered_data(self):
        data = {
            'pk': self.review_1.pk,
            'menu': self.menu_1.pk,
            'rating': 2,
            'comment': 'Not so good'
        }
        response = self.client.put(
            f'http://127.0.0.1:8000/api/review/',
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Review.objects.filter(menu=self.menu_1, user=self.user, rating=2, comment='Not so good').count(), 1)

    def test_delete_a_review_with_all_requiered_data(self):
        response = self.client.delete(
            'http://127.0.0.1:8000/api/review/',
            data= {'pk': self.review_1.pk },
            content_type='application/json',
            headers={'Authorization': f'Token {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Review.objects.filter(pk=self.review_1.pk).count(), 0)
        
    


    

