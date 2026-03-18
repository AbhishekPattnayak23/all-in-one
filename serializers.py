from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.Serializer):
    sender = serializers.IntegerField()
    recipient = serializers.IntegerField()
    message = serializers.CharField(max_length=1000)

    def validate_sender(self, value):
        from django.contrib.auth.models import User
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Sender user not found")
        return value

    def validate_recipient(self, value):
        from django.contrib.auth.models import User
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Recipient user not found")
        return value

    def create(self, validated_data):
        from django.contrib.auth.models import User
        notification = Notification.objects.create(
            sender_id=validated_data['sender'],
            recipient_id=validated_data['recipient'],
            message=validated_data['message']
        )
        return notification
