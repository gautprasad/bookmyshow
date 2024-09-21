from django.urls import path
from .views import reserve_ticket, view_bookings_user, cancel_booking

urlpatterns = [
    path('reserve-ticket/', reserve_ticket, name='reserve-ticket'),
    path('view-bookings-user/', view_bookings_user, name='view-bookings-user'),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel-booking'),
]