from django.urls import reverse, resolve
from django.test import TestCase
from booking.views import reserve_ticket, view_bookings_user, cancel_booking

class URLTests(TestCase):

    def test_reserve_ticket_url(self):
        url = reverse('reserve_ticket')
        self.assertEqual(resolve(url).func, reserve_ticket)

    def test_view_bookings_user_url(self):
        url = reverse('view_bookings_user')
        self.assertEqual(resolve(url).func, view_bookings_user)

    def test_cancel_booking_url(self):
        url = reverse('cancel_booking', args=[1])
        self.assertEqual(resolve(url).func, cancel_booking)