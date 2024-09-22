from django.urls import path
from . import views
from .views import DeleteUserView


urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.get_users, name='get_users'),
    path('<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('delete/', DeleteUserView.as_view(), name='delete_user'),
]