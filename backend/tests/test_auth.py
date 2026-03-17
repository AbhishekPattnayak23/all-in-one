import pytest
from services.auth_service import AuthService
from services.user_store import UserStore

def test_password_hashing():
    auth_service = AuthService()
    password = "test123"
    hashed = auth_service.hash_password(password)
    
    assert hashed != password
    assert auth_service.verify_password(password, hashed)
    assert not auth_service.verify_password("wrong", hashed)

def test_user_validation():
    user_store = UserStore()
    
    # Test with demo user
    user = user_store.validate_user_credentials("demo@example.com", "password123")
    assert user is not None
    assert user.email == "demo@example.com"
    
    # Test wrong password
    user = user_store.validate_user_credentials("demo@example.com", "wrongpass")
    assert user is None
    
    # Test non-existent user
    user = user_store.validate_user_credentials("nonexistent@test.com", "pass")
    assert user is None

def test_jwt_generation():
    auth_service = AuthService()
    from models.user import User
    
    user = User(id="test-1", email="test@example.com", password_hash="hash")
    token = auth_service.generate_token(user)
    
    assert isinstance(token, str)
    assert len(token) > 0
    
    payload = auth_service.decode_token(token)
    assert payload is not None
    assert payload['user_id'] == user.id
    assert payload['email'] == user.email
