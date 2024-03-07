from users.tests import TestUserSetUp
from django.urls import reverse
from .models import Booking
from .forms import BookingForm
from datetime import datetime, timedelta
from rest_framework.test import RequestsClient

# Create your tests here.
class TestBookingSetUp(TestUserSetUp):
    def setUp(self):
        super().setUp()
        tomorrow_date = datetime.now().date() + timedelta(days=1)
        self.reservation = {'date': tomorrow_date, 'time': '21:30:00', 'guests': 4, 'occasion': 'Anniversary', 'user': self.user}
        self.reservation_1 = Booking.objects.create(date= tomorrow_date, time= '21:30:00', guests= 4, occasion= 'Anniversary', user= self.user)
        
class TestBookingViews(TestBookingSetUp):
    def test_enter_booking_view_without_credentials(self):
        response = self.client.post('http://127.0.0.1:8000/booking/')
        self.assertEqual(response.status_code, 302)

    def test_enter_booking_view_with_credentials(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('booking'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking.html')
        self.assertIsInstance(response.context['form'], BookingForm)
        self.assertIsNone(response.context['errors'])
        self.assertEqual(response.context['bookings'].count(), 1)

    def test_successful_booking_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('booking'), self.reservation)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 2)
        self.assertEqual(Booking.objects.first().user, self.user)
        self.assertEqual(Booking.objects.first().date, self.reservation['date'])
        expected_time = datetime.strptime(self.reservation['time'], '%H:%M:%S').time()
        self.assertEqual(Booking.objects.first().time, expected_time)
        self.assertEqual(Booking.objects.first().guests, self.reservation['guests'])
        self.assertEqual(Booking.objects.first().occasion, self.reservation['occasion'])

    def test_successful_booking_confirmation_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('successful_booking', kwargs={'pk': self.reservation_1.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')

    def test_get_edit_booking_view_without_credentials(self):
        response = self.client.get(reverse('edit_booking', kwargs={'pk': self.reservation_1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_get_edit_booking_view_with_credentials(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_booking', kwargs={'pk': self.reservation_1.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')
        self.assertIsInstance(response.context['form'], BookingForm)
        self.assertEqual(response.context['bookings'], [self.reservation_1])
        self.assertIsNone(response.context['errors'])

    def test_successful_booking_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_booking', kwargs={'pk': self.reservation_1.pk}), self.reservation)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().user, self.user)
        self.assertEqual(Booking.objects.first().date, self.reservation['date'])
        expected_time = datetime.strptime(self.reservation['time'], '%H:%M:%S').time()
        self.assertEqual(Booking.objects.first().time, expected_time)
        self.assertEqual(Booking.objects.first().guests, self.reservation['guests'])
        self.assertEqual(Booking.objects.first().occasion, self.reservation['occasion'])

    def test_delete_booking_view_without_credentials(self):
        response = self.client.get(reverse('delete_booking', kwargs={'pk': self.reservation_1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_delete_booking_view_with_credentials(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete_booking', kwargs={'pk': self.reservation_1.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancelation.html')
        self.assertEqual(Booking.objects.count(), 1)

    def test_successful_delete_booking_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_booking', kwargs={'pk': self.reservation_1.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 0)


class BookingListCreateViewTest(TestBookingSetUp):
    client = RequestsClient()

    def test_get_all_reservations_without_credentials(self):
        response = self.client.get('http://127.0.0.1:8000/api/booking/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_get_all_reservations_with_credentials(self):
        response = self.client.get('http://127.0.0.1:8000/api/booking/', headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_a_reservation_without_credentials(self):
        response = self.client.post('http://127.0.0.1:8000/api/booking/', data=self.reservation)
        self.assertEqual(response.status_code, 403)

    def test_create_a_reservation_with_credentials(self):
        response = self.client.post('http://127.0.0.1:8000/api/booking/', headers={'Authorization': f'Token {self.token}'}, data=self.reservation)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 2)

    def test_edit_a_reservation(self):
        response = self.client.get(f'http://127.0.0.1:8000/api/booking/{self.reservation_1.pk}/', headers={'Authorization': f'Token {self.token}'}, data=self.reservation)
        self.assertEqual(response.status_code, 200)

    def delete_a_reservation(self):
        response = self.client.delete(f'http://127.0.0.1:8000/api/booking/{self.reservation_1.pk}/', headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, 204)
