from django.db import models
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class Notification(models.Model):
    """
    Bulletproof Notification model with comprehensive error handling

    Fields:
    - sender: User who sends the notification (foreign key)
    - recipient: User who receives the notification (foreign key)
    - message: Text content of the notification
    - timestamp: When the notification was created
    """

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        help_text="User who sent the notification"
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_notifications',
        help_text="User who receives the notification"
    )

    message = models.TextField(
        max_length=1000,
        blank=False,
        null=False,
        help_text="Notification message content"
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="When this notification was created"
    )

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['recipient', '-timestamp']),
            models.Index(fields=['sender', '-timestamp']),
        ]

    def __str__(self):
        return f"Notification from {self.sender} to {self.recipient}: {self.message[:50]}..."

    @classmethod
    def create_safe(cls, sender_id, recipient_id, message):
        """Bulletproof notification creation with validation"""
        try:
            # Validate existence of both sender and recipient
            sender = User.objects.get(id=sender_id)
            recipient = User.objects.get(id=recipient_id)

            if not message or not message.strip():
                raise ValueError("Message cannot be empty")

            notification = cls.objects.create(
                sender=sender,
                recipient=recipient,
                message=message.strip()
            )

            logger.info(f"Notification created successfully: {notification.id}")
            return notification

        except User.DoesNotExist as e:
            logger.error(f"User not found: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to create notification: {str(e)}")
            raise
