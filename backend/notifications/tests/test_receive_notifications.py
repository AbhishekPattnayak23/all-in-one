from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from notifications.models import Notification

User = get_user_model()

class ReceiveNotificationsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', password='testpass123', email='test1@test.com')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123', email='test2@test.com')

        # Create test notifications for user1
        self.notification1 = Notification.objects.create(
            sender=self.user2,
            recipient=self.user1,
            message='Test message 1',
            is_read=False
        )
        self.notification2 = Notification.objects.create(
            sender=self.user2,
            recipient=self.user1,
            message='Test message 2',
            is_read=True
        )
        # Create notification for user2 (should not appear in user1's results)
        self.notification3 = Notification.objects.create(
            sender=self.user1,
            recipient=self.user2,
            message='Test message 3',
            is_read=False
        )

    def test_receive_notifications_requires_auth(self):
        """Test that endpoint requires authentication"""
        response = self.client.get('/api/receive_notifications/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_receive_notifications_returns_auth_user_notifications(self):
        """Test endpoint returns only notifications for authenticated user"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/receive_notifications/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notifications = response.json()

        # Should get 2 notifications
        self.assertEqual(len(notifications), 2)

        # Check correct notifications are present
        notification_ids = [n['id'] for n in notifications]
        self.assertIn(self.notification1.id, notification_ids)
        self.assertIn(self.notification2.id, notification_ids)
        self.assertNotIn(self.notification3.id, notification_ids)

        # Check they are in descending order
        self.assertGreater(notifications[0]['id'], notifications[1]['id'])

        # Check notification structure
        for notification in notifications:
            self.assertIn('id', notification)
            self.assertIn('sender', notification)
            self.assertIn('recipient', notification)
            self.assertIn('message', notification)
            self.assertIn('is_read', notification)
            self.assertIn('created_at', notification)
            # Ensure notification belongs to authenticated user
            self.assertEqual(notification['recipient'], self.user1.id)
