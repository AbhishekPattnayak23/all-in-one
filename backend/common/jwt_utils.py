import jwt
from datetime import datetime, timedelta
from django.conf import settings


def generate_jwt_token(user_id, username, email):
    """
    Generate a JWT token for successful login.
    
    Args:
        user_id: UUID string
        username: User's username
        email: User's email
    
    Returns:
        str: JWT token
    """
    payload = {
        'user_id': str(user_id),
        'username': username,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'nbf': datetime.utcnow(),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def decode_jwt_token(token):
    """
    Decode and validate JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        dict: Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
