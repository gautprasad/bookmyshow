from django.urls import path
from .views import book_ticket, view_bookings, cancel_booking

urlpatterns = [
    path('book-ticket/', book_ticket, name='book-ticket'),
    path('view-bookings/', view_bookings, name='view-bookings'),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel-booking'),
]