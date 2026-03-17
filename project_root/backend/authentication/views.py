from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .serializers import RegisterSerializer, LoginSerializer, MeSerializer
from .utils import jwt_encode

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """User registration endpoint"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = jwt_encode(user.id)
        return Response({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """User login endpoint"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token = jwt_encode(user.id)
        return Response({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    return Response({
        'detail': serializer.errors.get('non_field_errors', ['Invalid credentials'])[0],
        'error_code': 'LOGIN_FAIL'
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """Send password reset email"""
    email = request.data.get('email')
    
    if not email:
        return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Send email via console backend for dev
        reset_link = f"http://localhost:3000/reset-password/{uid}/{token}"
        send_mail(
            'Password Reset',
            f'Click the following link to reset your password: {reset_link}',
            'noreply@example.com',
            [email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        # Don't reveal if user exists for security
        pass
    
    return Response({'message': 'Password reset email sent'})

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request, token):
    """Confirm password reset with token"""
    new_password = request.data.get('new_password')
    
    if not new_password:
        return Response({'detail': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # TODO: Implement token validation
    return Response({'message': 'Password reset successful'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_me(request):
    """Get current user profile"""
    serializer = MeSerializer(request.user)
    return Response(serializer.data)
