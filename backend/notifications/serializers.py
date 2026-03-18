from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Notification

class SendNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'sender', 'recipient', 'message', 'timestamp']
        read_only_fields = ['id', 'timestamp']

    def validate_sender(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Sender user does not exist.")
        return value

    def validate_recipient(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Recipient user does not exist.")
        return value

    def validate_message(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        return value.strip()

    def validate(self, data):
        if data['sender'] == data['recipient']:
            raise serializers.ValidationError("Cannot send notification to yourself.")
        return data

class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.IntegerField(source='sender.id', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'sender', 'recipient', 'message', 'timestamp']
