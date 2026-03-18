from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models.notification import Notification

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Notification
        fields = ("id", "sender", "message", "created_at")
