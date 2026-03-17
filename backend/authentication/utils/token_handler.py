from datetime import datetime, timedelta
from typing import Any, Dict

from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User


def create_jwt_for_user(user: User) -> Dict[str, str]:
    refresh = RefreshToken.for_user(user)
    return {
        "token": str(refresh.access_token),
        "user": {
            "id": str(user.uuid),
            "username": user.username,
            "email": user.email,
        }
    }
