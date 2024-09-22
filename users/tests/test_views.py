from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewsTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_register(self):
        url = reverse('register')
        data = {
            "email": "manager@gmail.com",
            "username": "manager",
            "name": "John Doe",
            "password": "password123",
            "is_event_manager": True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully.')

    def test_get_users(self):
        url = reverse('get_users')
        response = self.client.get(url)
        # response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIsInstance(response_data.data, list)

    def test_get_user_by_id(self):
        url = reverse('get_user_by_id', args=[self.user.id])
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['id'], self.user.id)

    def test_get_user_by_id_not_found(self):
        url = reverse('get_user_by_id', args=[999])
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data['error'], 'User not found.')

    def test_delete_user_without_token(self):
        url = reverse('delete_user')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_with_token(self):
        url = reverse('delete_user')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)