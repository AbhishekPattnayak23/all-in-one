from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

class PasswordResetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.password_reset_url = '/api/auth/password-reset/request/'
    
    def test_password_reset_request(self):
        response = self.client.post(
            self.password_reset_url,
            {'email': 'test@example.com'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
