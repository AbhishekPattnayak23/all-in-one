import json
import uuid
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from backend.authentication.models import User


class LoginAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('auth-login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_successful_login(self):
        """Test successful login returns JWT token."""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('token', response_data)
        self.assertIn('user', response_data)
        self.assertEqual(response_data['user']['username'], 'testuser')
        self.assertEqual(response_data['user']['email'], 'test@example.com')
        self.assertIn('id', response_data['user'])
    
    def test_invalid_username(self):
        """Test login with invalid username."""
        data = {
            'username': 'nonexistent',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.json()
        self.assertEqual(response_data['detail'], 'Invalid credentials.')
        self.assertEqual(response_data['error_code'], 'INVALID_CREDENTIALS')
    
    def test_invalid_password(self):
        """Test login with invalid password."""
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.json()
        self.assertEqual(response_data['detail'], 'Invalid credentials.')
        self.assertEqual(response_data['error_code'], 'INVALID_CREDENTIALS')
    
    def test_inactive_user(self):
        """Test login with inactive user."""
        user = User.objects.create_user(
            username='inactiveuser',
            email='inactive@example.com',
            password='testpass123'
        )
        user.is_active = False
        user.save()
        
        data = {
            'username': 'inactiveuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.json()
        self.assertEqual(response_data['detail'], 'Account is disabled.')
        self.assertEqual(response_data['error_code'], 'ACCOUNT_DISABLED')
    
    def test_missing_fields(self):
        """Test login with missing fields."""
        # Missing username
        data = {'password': 'testpass123'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Missing password
        data = {'username': 'testuser'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
