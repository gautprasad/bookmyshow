from django.urls import path
from .views import CreateEventView, EventListView

urlpatterns = [
    path('create-event/', CreateEventView.as_view(), name='create-event'),
    path('all-events/', EventListView.as_view(), name='event-list'),
]