from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.get_users, name='get-users'),
    path('<uuid:user_id>/', views.get_user_by_id, name='get-user-by-id'),
    path('<uuid:user_id>/delete/', views.delete_user, name='delete-user'),
]