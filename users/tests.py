from django.test import TestCase
from django.urls import reverse
from rest_framework.test import RequestsClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class TestUserSetUp(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser', 
            email = 'testuser@gmail.com', 
            password =  'TestPassword@12345!'
        )

class AuthenticationViewRenderTest(TestUserSetUp):
    
    def test_signup_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser1',
            'email': 'testuser1@gmail.com',
            'password1': 'TestPassword@12345!',
            'password2': 'TestPassword@12345!'
        })
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(email = 'testuser1@gmail.com')
        self.assertTrue(new_user.is_active)

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'email': 'testuser@gmail.com',
            'password': 'TestPassword@12345!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['_auth_user_id'], str(User.objects.get(email = 'testuser@gmail.com').pk))

    def test_logout_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get('_auth_user_id'), None)


class AuthenticationViewAPITest(TestCase):
    client = RequestsClient()
    def setUp(self):
        User.objects.create_user(
            username = 'testuser', 
            email = 'testuser@gmail.com', 
            password =  'TestPassword@12345!'
        )
        self.token = Token.objects.create(user = User.objects.get(email = 'testuser@gmail.com')).key

    def test_register_without_data(self):
        response = self.client.post('http://127.0.0.1:8000/api/signup', {})
        self.assertEqual(response.status_code, 400)

    def test_create_a_user_that_already_exists(self):
        response = self.client.post('http://127.0.0.1:8000/api/signup', {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password': 'TestPassword@12345!',
        })
        self.assertEqual(response.status_code, 400)

    def test_register_with_data(self):
        response = self.client.post('http://127.0.0.1:8000/api/signup', {
            'username': 'testuser1',
            'email': 'testuser1@gmail.com',
            'password': 'TestPassword@12345!',
        })
        self.assertEqual(response.status_code, 201)

    def test_login_without_data(self):
        response = self.client.post('http://127.0.0.1:8000/api/login', {})
        self.assertEqual(response.status_code, 404)

    def test_login_with_data(self):
        response = self.client.post('http://127.0.0.1:8000/api/login', {
            'email': 'testuser@gmail.com',
            'password': 'TestPassword@12345!',
        })
        self.assertEqual(response.status_code, 200)

    def test_token_without_it(self):
        response = self.client.get('http://127.0.0.1:8000/api/test-token', headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, 200)

    