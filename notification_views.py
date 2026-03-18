from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import NotificationSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def send_notification(request):
    try:
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            notification = serializer.save()
            logger.info(f"Notification created: {notification.id}")
            return Response({
                'success': True,
                'message': 'Notification sent successfully',
                'notification_id': notification.id
            }, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"Invalid notification data: {serializer.errors}")
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Failed to process notification: {str(e)}")
        return Response({
            'success': False,
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
