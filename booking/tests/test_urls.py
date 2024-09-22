from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from events.models import Event, Location, Category

class BookingURLsTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        locations = ["Stadium", "Conference Hall", "Open Ground", "Auditorium"]
        for location_name in locations:
            Location.objects.get_or_create(name=location_name)

        categories = ["Movies", "Concerts", "Plays", "Sports", "Standup Comedy", "Live Events"]
        for category_name in categories:
            Category.objects.get_or_create(name=category_name)

        self.location = Location.objects.get(name="Stadium")
        self.category = Category.objects.get(name="Concerts")
        self.event = Event.objects.create(
            title='Test Event',
            description='This is a test event',
            location=self.location,
            category=self.category,
            date='2023-12-31',
            time='18:00:00',
            available_tickets=100,
            payment_options='Credit Card, PayPal',
            cost_per_ticket=50.00,
            created_by=self.user
        )

    def test_reserve_ticket_url(self):
        url = reverse('reserve_ticket')
        data = {
            'event': self.event.id,
            'number_of_tickets': 2,
            "status":  "reserved",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_bookings_user_url(self):
        url = reverse('view_bookings_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)

    def test_cancel_booking_url(self):
        reserve_url = reverse('reserve_ticket')
        reserve_data = {
            'event': self.event.id,
            'number_of_tickets': 2,
            "status":  "reserved",
        }
        reserve_response = self.client.post(reserve_url, reserve_data, format='json')
        self.assertEqual(reserve_response.status_code, status.HTTP_200_OK)
        booking_id = reserve_response.json().get('booking_id')
        cancel_url = reverse('cancel_booking', args=[booking_id])
        response = self.client.put(cancel_url, HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cancel_booking_not_found_url(self):
        cancel_url = reverse('cancel_booking', args=[999])
        response = self.client.put(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)