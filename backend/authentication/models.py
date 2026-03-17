from uuid import uuid4
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    hashed_password = models.CharField(max_length=128)
    
    class Meta:
        db_table = 'authentication_user'
    
    def __str__(self):
        return self.username
