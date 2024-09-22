from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from payments.models import Payment
from booking.models import Booking
from events.models import Event, Location, Category

class PaymentViewsTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.userManager = User.objects.create_user(username='manager@example.com', email='manager@example.com', password='password123', is_event_manager=True)
        self.tokenManager = str(RefreshToken.for_user(self.userManager).access_token)
        
        self.user = User.objects.create_user(username='testuser@example.com', email='testuser@example.com', password='password123')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.get_all_payments_url = reverse('get_all_payments')
        self.make_payment_url = reverse('make_payment')

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
            created_by=self.userManager
        )

        # Create a payment for the booking
        self.payment = Payment.objects.create(
            amount=100.0,
            mode_of_payment='credit_card',
            user=self.user,
            status='completed'
        )
        
        # Create a booking for the user
        self.booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            number_of_tickets=2,
            status='booked',
            payment=self.payment
        )

        self.bookingReserved = Booking.objects.create(
            user=self.user,
            event=self.event,
            number_of_tickets=2,
            status='reserved',
        )


    def test_get_all_payments(self):
        response = self.client.get(self.get_all_payments_url, HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 1)

    def test_make_payment_success(self):
        data = {
            'booking_id': self.bookingReserved.id,
            'mode_of_payment': 'credit_card',
            'amount': 100.0
        }
        response = self.client.post(self.make_payment_url, data, format='json', HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('payment id', response.data)

    def test_make_payment_invalid_booking(self):
        data = {
            'booking_id': 999,  # Non-existent booking ID
            'mode_of_payment': 'credit_card',
            'amount': 100.0
        }
        response = self.client.post(self.make_payment_url, data, format='json', HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Booking not found.')

    def test_make_payment_invalid_data(self):
        data = {
            'booking_id': self.booking.id,
            'mode_of_payment': 'aaaaa',  # Invalid mode of payment
            'amount': 100.0
        }
        response = self.client.post(self.make_payment_url, data, format='json', HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('mode_of_payment', response.data)

    def test_revert_payment_success(self):
        revert_payment_url = reverse('revert_payment', args=[self.payment.id])
        response = self.client.put(revert_payment_url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.token)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Payment reverted and booking updated successfully.')

    def test_revert_payment_not_found(self):
        revert_payment_url = reverse('revert_payment', args=[999])
        response = self.client.put(revert_payment_url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Payment not found.')
