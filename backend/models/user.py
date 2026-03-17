from datetime import datetime
from typing import Dict, Optional

class User:
    def __init__(self, id: str, email: str, password_hash: str, 
                 first_name: str = "", last_name: str = "", 
                 created_at: Optional[datetime] = None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'User':
        created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else None
        return User(
            id=data['id'],
            email=data['email'],
            password_hash=data['password_hash'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            created_at=created_at
        )
