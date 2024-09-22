from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserManagerTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(email='testuser@example.com', username='testuser', password='password123')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(email='', username='testuser', password='password123')
        self.assertEqual(str(context.exception), 'The Email field must be set')

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email='superuser@example.com', username='superuser', password='password123')
        self.assertEqual(superuser.email, 'superuser@example.com')
        self.assertEqual(superuser.username, 'superuser')
        self.assertTrue(superuser.check_password('password123'))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_without_is_staff(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(email='superuser@example.com', username='superuser', password='password123', is_staff=False)
        self.assertEqual(str(context.exception), 'Superuser must have is_staff=True.')

    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(email='superuser@example.com', username='superuser', password='password123', is_superuser=False)
        self.assertEqual(str(context.exception), 'Superuser must have is_superuser=True.')

class UserModelTests(TestCase):

    def test_user_fields(self):
        user = User.objects.create_user(email='testuser@example.com', username='testuser', password='password123')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))