from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_notifications'
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_notifications'
    )
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Notification from {self.sender.username} to {self.recipient.username}"
