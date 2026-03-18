from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Notification
from authentication.permissions import IsAuthenticated

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'sender', 'recipient', 'message', 'is_read', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Ensure sender and recipient are serialized as user IDs
        data['sender'] = instance.sender.id
        data['recipient'] = instance.recipient.id
        return data

class ReceiveNotificationsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for receiving user notifications
    Returns only notifications for the authenticated user
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
