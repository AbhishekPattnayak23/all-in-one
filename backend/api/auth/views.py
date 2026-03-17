import uuid
from datetime import datetime, timedelta
import jwt
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models import User
from .serializers import UserSerializer


class RegisterView(viewsets.ViewSet):
    def create(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([username, email, password]):
            return Response({'detail': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'detail': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'detail': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            email=email,
            hashed_password=make_password(password)
        )

        payload = {
            'id': str(user.uuid),
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')

        user_serializer = UserSerializer(user)
        return Response({
            'token': token,
            'user': user_serializer.data
        }, status=status.HTTP_201_CREATED)
