from django.test import TestCase
from django.contrib.auth.models import User
from models.notification_model import Notification

class NotificationModelTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username='sender',
            password='testpass123'
        )
        self.recipient = User.objects.create_user(
            username='recipient',
            password='testpass123'
        )

    def test_notification_creation(self):
        notification = Notification.create_notification(
            sender=self.sender,
            recipient=self.recipient,
            message='Hello World!'
        )
        self.assertEqual(notification.sender.username, 'sender')
        self.assertEqual(notification.recipient.username, 'recipient')
        self.assertEqual(notification.message, 'Hello World!')
        self.assertFalse(notification.is_read)

    def test_unread_count(self):
        Notification.create_notification(
            sender=self.sender,
            recipient=self.recipient,
            message='Test 1'
        )
        Notification.create_notification(
            sender=self.sender,
            recipient=self.recipient,
            message='Test 2'
        )
        self.assertEqual(
            Notification.get_unread_count(self.recipient),
            2
        )
