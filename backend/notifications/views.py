from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Notification
from .serializers import SendNotificationSerializer, NotificationSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_notification(request):
    """
    Send notification to another user
    Endpoint: POST /api/send_notification/

    Request Body:
    {
        "sender": int,
        "recipient": int,
        "message": str
    }

    Response:
    {
        "id": int,
        "sender": int,
        "recipient": int,
        "message": str,
        "timestamp": "2023-10-20T14:30:00Z"
    }
    """
    # Enforce sender matches authenticated user
    data = request.data.copy()
    data['sender'] = request.user.id

    serializer = SendNotificationSerializer(data=data)

    if serializer.is_valid():
        notification = serializer.save()
        response_data = {
            'id': notification.id,
            'sender': notification.sender.id,
            'recipient': notification.recipient.id,
            'message': notification.message,
            'timestamp': notification.timestamp.isoformat()
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def receive_notifications(request):
    """
    Get all notifications for the authenticated user
    Endpoint: GET /api/notifications/receive/

    Response:
    [
        {
            "id": int,
            "sender": int,
            "message": str,
            "timestamp": "2023-10-20T14:30:00Z"
        }
    ]
    """
    notifications = Notification.objects.filter(recipient=request.user)

    response_data = []
    for notification in notifications:
        response_data.append({
            'id': notification.id,
            'sender': notification.sender.id,
            'message': notification.message,
            'timestamp': notification.timestamp.isoformat()
        })

    return Response(response_data, status=status.HTTP_200_OK)
