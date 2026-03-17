from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import LoginSerializer, UserSerializer
from backend.common.jwt_utils import generate_jwt_token


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """API endpoint for user login."""
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'detail': 'Invalid input.', 'error_code': 'INVALID_INPUT'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            {'detail': 'Invalid credentials.', 'error_code': 'INVALID_CREDENTIALS'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not user.check_password(password):
        return Response(
            {'detail': 'Invalid credentials.', 'error_code': 'INVALID_CREDENTIALS'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not user.is_active:
        return Response(
            {'detail': 'Account is disabled.', 'error_code': 'ACCOUNT_DISABLED'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Generate JWT token
    token = generate_jwt_token(user.uuid, user.username, user.email)
    
    # Prepare response
    response_data = {
        'token': token,
        'user': UserSerializer(user).data
    }
    
    return Response(response_data, status=status.HTTP_200_OK)
