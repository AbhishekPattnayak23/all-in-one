from typing import Dict, Optional
from models.user import User
from services.auth_service import AuthService

class UserStore:
    """In-memory user store for demo. Replace with actual database."""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.auth_service = AuthService()
        
        # Demo user - password: "password123"
        demo_user = User(
            id="user-1",
            email="demo@example.com",
            password_hash="$2b$12$KtKP2.ybrTcEJsV8oGXUg.6mmFQdlLN3KZA2xYdZ.bzx1MtiQPr2i",
            first_name="Demo",
            last_name="User"
        )
        self.users[demo_user.email] = demo_user
    
    def create_user(self, email: str, password: str, **kwargs) -> User:
        """Create a new user."""
        if email in self.users:
            raise ValueError("User already exists")
        
        password_hash = self.auth_service.hash_password(password)
        user_id = f"user-{len(self.users) + 1}"
        user = User(id=user_id, email=email, password_hash=password_hash, **kwargs)
        self.users[email] = user
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.users.get(email)
    
    def validate_user_credentials(self, email: str, password: str) -> Optional[User]:
        """Validate user credentials."""
        user = self.get_user_by_email(email)
        if user and self.auth_service.verify_password(password, user.password_hash):
            return user
        return None
