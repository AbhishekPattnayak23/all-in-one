import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class TestAuthentication(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_register_success(self):
        """Test user registration happy path"""
        response = self.client.post('/api/auth/register', {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('token', data)
        self.assertEqual(data['user']['username'], 'testuser')
    
    def test_login_success(self):
        """Test user login happy path"""
        user = User.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password='login123'
        )
        
        response = self.client.post('/api/auth/login', {
            'username': 'loginuser',
            'password': 'login123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('token', data)
    
    def test_me_endpoint(self):
        """Test user profile endpoint"""
        user = User.objects.create_user(
            username='meuser',
            email='me@example.com',
            password='mypass123'
        )
        
        # Login to get token
        login_response = self.client.post('/api/auth/login', {
            'username': 'meuser',
            'password': 'mypass123'
        })
        token = login_response.json()['token']
        
        # Access me endpoint with token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get('/api/user/me')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['username'], 'meuser')
