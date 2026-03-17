from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterRequestSerializer
from .models import User

class RegisterUser(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterRequestSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            detail = ', '.join([f"{k}: {v[0]}" for k, v in errors.items()])
            return Response(
                {"detail": detail, "error_code": "INVALID_INPUT"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        
        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Username already taken", "error_code": "USERNAME_EXISTS"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {"detail": "Email already exists", "error_code": "EMAIL_EXISTS"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = serializer.save()
        token = RefreshToken.for_user(user)
        return Response(
            {
                "token": str(token.access_token),
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email
                }
            },
            status=status.HTTP_201_CREATED
        )
