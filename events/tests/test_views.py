from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from events.models import Event, Location, Category
from payments.models import Payment
from booking.models import Booking
from rest_framework_simplejwt.tokens import RefreshToken

class EventViewsTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.event_manager = User.objects.create_user(username='eventmanager@example.com', email='eventmanager@example.com', password='password123', is_event_manager=True)
        self.regular_user = User.objects.create_user(username='regularuser@example.com', email='regularuser@example.com', password='password123')
        self.event_manager_token = str(RefreshToken.for_user(self.event_manager).access_token)
        self.regular_user_token = str(RefreshToken.for_user(self.regular_user).access_token)

        self.create_event_url = reverse('create_event')
        self.list_events_url = reverse('event_list')
        self.cancel_event_url = reverse('cancel_event', args=[1])  # Assuming the event ID is 1

        # Create a location and category for the event
        self.location = Location.objects.create(name='Test Location')
        self.category = Category.objects.create(name='Test Category')

    def test_create_event_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.event_manager_token)
        data = {
            'title': 'MUSIC SHOW',
            'description': 'Live music concert',
            'date': '2024-12-20',
            'time': '18:00',
            'location': self.location.id,
            'category': self.category.id,
            'payment_options': 'Credit Card, PayPal',
            'cost_per_ticket': 50.00
        }
        response = self.client.post(self.create_event_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'MUSIC SHOW')
        self.assertEqual(response.data['description'], 'Live music concert')

    def test_create_event_permission_denied(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.regular_user_token)
        data = {
            'title': 'MUSIC SHOW',
            'description': 'Live music concert',
            'date': '2024-12-20',
            'time': '18:00',
            'location': self.location.id,
            'category': self.category.id,
            'payment_options': 'Credit Card, PayPal',
            'cost_per_ticket': 50.00
        }
        response = self.client.post(self.create_event_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_events(self):
        Event.objects.create(
            title='Test Event 1',
            description='This is a test event 1',
            location=self.location,
            category=self.category,
            date='2024-12-20',
            time='18:00',
            payment_options='Credit Card, PayPal',
            cost_per_ticket=50.00,
            created_by=self.event_manager
        )
        Event.objects.create(
            title='Test Event 2',
            description='This is a test event 2',
            location=self.location,
            category=self.category,
            date='2024-12-20',
            time='18:00',
            payment_options='Credit Card, PayPal',
            cost_per_ticket=50.00,
            created_by=self.event_manager
        )
        response = self.client.get(self.list_events_url, HTTP_AUTHORIZATION='Bearer ' + self.regular_user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Test Event 1')
        self.assertEqual(response.data[1]['title'], 'Test Event 2')

    def test_cancel_event_success(self):
        event = Event.objects.create(
            title='Test Event',
            description='This is a test event',
            location=self.location,
            category=self.category,
            date='2024-12-20',
            time='18:00',
            payment_options='Credit Card, PayPal',
            cost_per_ticket=50.00,
            created_by=self.event_manager
        )
        booking = Booking.objects.create(
            user=self.regular_user,
            event=event,
            number_of_tickets=2,
            status='booked'
        )
        payment = Payment.objects.create(
            booking=booking,
            amount=100.0,
            mode_of_payment='credit_card',
            status='completed',
            user=self.regular_user
        )
        booking.payment = payment
        booking.save()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.event_manager_token)
        response = self.client.put(reverse('cancel_event', args=[event.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Event canceled and associated bookings updated successfully.')

        booking.refresh_from_db()
        self.assertEqual(booking.status, 'event_canceled')
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'refunded')

    def test_cancel_event_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.event_manager_token)
        response = self.client.put(reverse('cancel_event', args=[999]), format='json')  # Non-existent event ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Event not found.')