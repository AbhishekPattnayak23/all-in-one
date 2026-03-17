from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=32)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='uuid', read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
