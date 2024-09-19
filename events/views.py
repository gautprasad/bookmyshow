from rest_framework import generics, permissions
from .models import Event
from .serializers import EventSerializerPost, EventSerializerGet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EventFilter

class IsEventManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_event_manager == True

class CreateEventView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializerPost
    permission_classes = [permissions.IsAuthenticated, IsEventManager]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# class EventListView(generics.ListAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializerGet

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializerGet
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter