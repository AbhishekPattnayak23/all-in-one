from rest_framework import serializers
from typing import Any
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=32,  # per spec
        allow_blank=False,
        allow_null=False,
        help_text="User name field"
    )
    password = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        min_length=1,
        help_text="Password"
    )

    def validate(self, attrs: Any) -> Any:
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(request=self.context.get("request"), username=username, password=password)
        if user is None:
            raise serializers.ValidationError({"detail": "Invalid credentials", "error_code": "invalid_credentials"})
        if not user.is_active:
            raise serializers.ValidationError({"detail": "Inactive account", "error_code": "inactive_account"})
        attrs["user"] = user
        return attrs
