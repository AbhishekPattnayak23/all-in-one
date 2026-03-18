import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
import json

# Create test users
sender = User.objects.create_user(username='test_sender', password='test123', email='sender@test.com')
recipient = User.objects.create_user(username='test_recipient', password='test123', email='recipient@test.com')

# Test API
client = Client()
response = client.post(
    '/api/send_notification/',
    data=json.dumps({
        'sender': sender.id,
        'recipient': recipient.id,
        'message': 'Test notification message'
    }),
    content_type='application/json'
)

print('Status:', response.status_code)
print('Response:', response.json())
