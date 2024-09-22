from django.test import TestCase
from django.urls import reverse, resolve
from users.views import register, get_users, get_user_by_id, DeleteUserView
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UsersURLsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)

    def test_get_users_url_resolves(self):
        url = reverse('get_users')
        self.assertEqual(resolve(url).func, get_users)

    def test_get_user_by_id_url_resolves(self):
        url = reverse(get_user_by_id, args=[1])
        self.assertEqual(resolve(url).func, get_user_by_id)

    def test_delete_user_url_resolves(self):
        url = reverse('delete_user')
        self.assertEqual(resolve(url).func.view_class, DeleteUserView)

    def test_register_url_response(self):
        response = self.client.post(reverse('register'))
        self.assertEqual(response.status_code, 400)

    def test_get_users_url_response(self):
        response = self.client.get(reverse('get_users'))
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id_url_response(self):
        response = self.client.get(reverse('get_user_by_id', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_delete_user_url_response(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(reverse('delete_user'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)