from django.test import TestCase
from django.urls import reverse
from .models import OpeningHours
from menu.tests import TestMenuSetUp
from rest_framework.test import RequestsClient

class TestRestaurantSetUp(TestMenuSetUp):
    def setUp(self):
        super().setUp()
        OpeningHours.objects.create(days='Mon - Fri', opening_hour='2pm', closing_hour='10pm')
        OpeningHours.objects.create(days='Sat', opening_hour='2pm', closing_hour='11pm')
        OpeningHours.objects.create(days='Sun', opening_hour='2pm', closing_hour='9pm')

class RenderViewTest(TestRestaurantSetUp):
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(len(response.context['opening_hours']), 3)
        self.assertEqual(len(response.context['menus']), 4)

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

class APIViewTest(TestRestaurantSetUp):
    client = RequestsClient()

    def test_opening_hours_view(self):
        response = self.client.get('http://127.0.0.1:8000/api/opening-hours/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)