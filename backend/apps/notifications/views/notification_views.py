"""
notification_views.py - receive_notifications endpoint

GET /api/receive_notifications/
Expects: Authorization: Bearer <jwt>
Returns: 200 OK
{
  "notifications": [
    {
      "id": int,
      "sender": { "username": str },
      "message": str,
      "created_at": iso8601
    },
    ...
  ]
}
401 if unauthenticated.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models.notification import Notification
from ..serializers.notification_serializer import NotificationSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def receive_notifications(request):
    """
    List all notifications for the authenticated user.
    """
    notifications = (
        Notification.objects.filter(recipient=request.user)
        .select_related("sender")
        .order_by("-created_at")
    )
    serializer = NotificationSerializer(notifications, many=True)
    return Response({"notifications": serializer.data}, status=status.HTTP_200_OK)
