from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import logging
from datetime import datetime
from uuid import uuid4

logger = logging.getLogger(__name__)

class NotificationService:
    """
    Service for handling email and WebSocket-based push notifications.

    This service provides methods to send notifications via email and
    WebSocket channels. Email delivery failures are logged but not raised
    (handled by Celery retry mechanism). WebSocket delivery failures are
    also logged gracefully to handle offline users.
    """

    def send_email_notification(self, recipient_id: int, message: str) -> dict:
        """
        Send email notification to user via Django's email backend.

        Uses Django's built-in send_mail function to deliver notifications.
        Creates a Notification record regardless of email delivery success.

        Args:
            recipient_id (int): ID of the recipient user
            message (str): The notification message content

        Returns:
            dict: {"notification_id": int, "created_at": iso8601 string}

        Raises:
            ValueError: If recipient_id is invalid
        """
        try:
            # Validate recipient exists
            recipient = User.objects.get(id=recipient_id)

            # Create notification record first (always succeeded)
            from ..models import Notification
            notification = Notification.objects.create(
                sender=None,  # System notification
                recipient=recipient,
                message=message,
                is_read=False
            )

            # Prepare email
            subject = "New Notification"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [recipient.email]

            try:
                # Attempt to send email
                send_mail(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                    fail_silently=False
                )
                logger.info(f"Email sent successfully to {recipient.email} (user_id: {recipient_id})")

            except Exception as e:
                # Log email failure but don't raise - Celery will handle retry
                logger.error(
                    f"Failed to send email to recipient {recipient_id} ({recipient.email}): {str(e)}"
                )

            return {
                "notification_id": notification.id,
                "created_at": notification.created_at.isoformat()
            }

        except User.DoesNotExist:
            logger.error(f"User with id {recipient_id} not found")
            raise ValueError(f"Invalid recipient_id: {recipient_id}")

    def push_notification(self, recipient_id: int, message: str) -> dict:
        """
        Send push notification via WebSocket using Django Channels.

        Sends the message to the user's notification channel group.
        Handles offline users gracefully by logging connection failures.

        Args:
            recipient_id (int): ID of the recipient user
            message (str): The notification message content

        Returns:
            dict: {"notification_id": int, "created_at": iso8601 string}

        Raises:
            ValueError: If recipient_id is invalid
        """
        try:
            # Validate recipient exists
            recipient = User.objects.get(id=recipient_id)

            # Create notification record
            from ..models import Notification
            notification = Notification.objects.create(
                sender=None,  # System notification
                recipient=recipient,
                message=message,
                is_read=False
            )

            # Prepare WebSocket message
            channel_layer = get_channel_layer()
            group_name = f"notifications_{recipient_id}"

            try:
                # Send via WebSocket channel layer
                async_to_sync(channel_layer.group_send)(
                    group_name,
                    {
                        "type": "send_notification",
                        "notification": {
                            "id": notification.id,
                            "message": message,
                            "created_at": notification.created_at.isoformat(),
                            "is_read": False
                        }
                    }
                )
                logger.info(f"Push notification sent successfully to user {recipient_id}")

            except Exception as e:
                # Log WebSocket failure but continue - user might be offline
                logger.error(
                    f"Failed to send push notification to user {recipient_id}: {str(e)}"
                )

            return {
                "notification_id": notification.id,
                "created_at": notification.created_at.isoformat()
            }

        except User.DoesNotExist:
            logger.error(f"User with id {recipient_id} not found")
            raise ValueError(f"Invalid recipient_id: {recipient_id}")
