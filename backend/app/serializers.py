from rest_framework import serializers
from app.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=32,
        required=True,
        error_messages={'required': 'username required'}
    )
    email = serializers.EmailField(
        required=True,
        error_messages={'required': 'email required'}
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={'required': 'password required'}
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value
