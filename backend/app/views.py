from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers import RegisterSerializer
from app.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import bcrypt
import base64

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Hash password with bcrypt
        password_bytes = data['password'].encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Base64 encode hash and salt for storage
        password_hash = hashed.decode('utf-8')
        
        # Create user
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=password_hash  # Using create_user will also hash with Django's default
        )
        
        # Generate JWT token
        token = RefreshToken.for_user(user)
        
        return Response({
            'token': str(token.access_token),
            'user': {
                'id': str(user.pk),
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)
