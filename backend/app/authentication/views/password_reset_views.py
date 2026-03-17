from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import uuid

from app.authentication.models.password_reset_token import PasswordResetToken
from app.authentication.serializers.password_reset_serializers import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from app.authentication.tasks.send_reset_email import send_reset_email_task

User = get_user_model()

FRONTEND_BASE_URL = "http://localhost:5173"

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token_str = str(uuid.uuid4())
            PasswordResetToken.objects.create(
                user=user,
                token=token_str,
                expires_at=timezone.now() + timedelta(minutes=30)
            )
            reset_link = f"{FRONTEND_BASE_URL}/password-reset-confirm/{token_str}"
            send_reset_email_task.delay(email, reset_link)
            return Response({'message': 'Password reset link sent'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request, token):
        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                expires_at__gt=timezone.now()
            )
        except PasswordResetToken.DoesNotExist:
            return Response({'message': 'Invalid or expired token'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user = reset_token.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            reset_token.delete()
            return Response({'message': 'Password updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
