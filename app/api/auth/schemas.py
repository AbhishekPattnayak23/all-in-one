from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.user import User

class PasswordResetRequestSchema(Schema):
    """Schema for password reset request."""
    email = fields.Email(required=True, validate=validate.Length(max=255))

class PasswordResetConfirmSchema(Schema):
    """Schema for password reset confirmation."""
    token = fields.String(required=True)
    password = fields.String(
        required=True, 
        validate=validate.Length(
            min=6, 
            max=128, 
            error="Password must be between 6 and 128 characters"
        )
    )
    password_confirm = fields.String(required=True)
    
    @validates('password_confirm')
    def validate_password_match(self, value, **kwargs):
        """Ensure password and confirmation match."""
        if value != self.context.get('password'):
            raise ValidationError('Passwords do not match')
