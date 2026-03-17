from flask import request, Blueprint, jsonify
from app.extensions import db
from app.models.user import User
from app.services.email_service import EmailService
from app.api.auth.schemas import PasswordResetRequestSchema, PasswordResetConfirmSchema
from marshmallow import ValidationError

password_reset_bp = Blueprint('password_reset', __name__, url_prefix='/api/auth')

@password_reset_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset link via email."""
    schema = PasswordResetRequestSchema()
    
    try:
        data = schema.load(request.json)
        email = data['email']
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user and user.is_active:
            # Generate reset token
            reset_token = user.generate_reset_token()
            
            # Send email
            email_sent = EmailService.send_password_reset_email(
                email, 
                reset_token, 
                user.username
            )
            
            if email_sent:
                current_app.logger.info(f"Password reset email sent to {email}")
            else:
                current_app.logger.error(f"Failed to send password reset email to {email}")
        
        # Always return success to prevent email enumeration
        return jsonify({
            'message': 'If your email exists in our system, you will receive a password reset link.'
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Invalid email format', 'details': e.messages}), 400
    except Exception as e:
        current_app.logger.error(f"Error in forgot_password: {str(e)}")
        return jsonify({'error': 'An error occurred processing your request'}), 500


@password_reset_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Confirm password reset with token."""
    schema = PasswordResetConfirmSchema()
    
    try:
        request_data = request.json
        schema.context = {'password': request_data.get('password')}
        data = schema.load(request_data)
        
        token = data['token']
        new_password = data['password']
        
        # Find user by reset token
        user = User.query.filter_by(reset_token=token).first()
        
        if not user:
            return jsonify({'error': 'Invalid or expired reset token'}), 400
        
        if not user.validate_reset_token(token):
            user.clear_reset_token()
            return jsonify({'error': 'Invalid or expired reset token'}), 400
        
        # Update password
        user.set_password(new_password)
        user.clear_reset_token()
        db.session.commit()
        
        current_app.logger.info(f"Password reset successful for user {user.email}")
        
        return jsonify({
            'message': 'Password reset successful. You can now login with your new password.'
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Invalid input', 'details': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in reset_password: {str(e)}")
        return jsonify({'error': 'An error occurred processing your request'}), 500


# Export blueprint
__all__ = ['password_reset_bp']
