from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from authentication.models import User

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        if not all([username, email, password]):
            return Response(
                {"detail": "Missing fields.", "error_code": "MISSING_FIELDS"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Username already taken.", "error_code": "USERNAME_TAKEN"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        if User.objects.filter(email=email).exists():
            return Response(
                {"detail": "Email already in use.", "error_code": "EMAIL_TAKEN"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        user = User.objects.create(
            username=username,
            email=email,
            hashed_password=make_password(password),
        )
        
        token = str(RefreshToken.for_user(user).access_token)
        
        return Response({
            "token": token,
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
            }
        }, status=status.HTTP_200_OK)
