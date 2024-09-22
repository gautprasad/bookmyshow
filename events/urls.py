from django.urls import path
from .views import CreateEventView, EventListView, cancel_event

urlpatterns = [
    path('create-event/', CreateEventView.as_view(), name='create_event'),
    path('get-events/', EventListView.as_view(), name='event_list'),
    path('cancel-event/<int:event_id>/', cancel_event, name='cancel_event'),
]