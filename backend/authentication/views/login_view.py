from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers.login_serializer import LoginSerializer
from authentication.utils.token_handler import create_jwt_for_user


class LoginView(APIView):
    permission_classes = []  # authentication not required

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            # DRF serializer automatically returns {key: list_of_errors}
            # we extract first/primary
            field_errors = serializer.errors
            first_field = list(field_errors)[0]
            if first_field == "username":
                return Response(
                    {"detail": "username required", "error_code": "username_required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if first_field == "password":
                return Response(
                    {"detail": "password required", "error_code": "password_required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Catch-all
            return Response(
                {"detail": list(field_errors.values())[0][0], "error_code": "validation_error"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = serializer.validated_data["user"]
        data = create_jwt_for_user(user)
        return Response(data, status=status.HTTP_200_OK)
