import pytest
from datetime import datetime, timedelta
from app.models.user import User
from app.services.email_service import EmailService
from unittest.mock import patch, MagicMock

class TestPasswordReset:
    
    def test_generate_reset_token(self, db_session, user_data):
        """Test reset token generation."""
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        
        token = user.generate_reset_token()
        
        assert token is not None
        assert len(token) > 20
        assert user.reset_token == token
        assert user.reset_token_expires_at > datetime.utcnow()
    
    def test_validate_reset_token_valid(self, db_session, user_data):
        """Test valid reset token validation."""
        user = User(**user_data)
        user.generate_reset_token()
        db_session.add(user)
        db_session.commit()
        
        assert user.validate_reset_token(user.reset_token) is True
    
    def test_validate_reset_token_expired(self, db_session, user_data):
        """Test expired reset token validation."""
        user = User(**user_data)
        user.generate_reset_token()
        user.reset_token_expires_at = datetime.utcnow() - timedelta(hours=2)
        db_session.add(user)
        db_session.commit()
        
        assert user.validate_reset_token(user.reset_token) is False
    
    def test_validate_reset_token_invalid(self, db_session, user_data):
        """Test invalid reset token validation."""
        user = User(**user_data)
        user.generate_reset_token()
        db_session.add(user)
        db_session.commit()
        
        assert user.validate_reset_token("invalid_token") is False
    
    def test_clear_reset_token(self, db_session, user_data):
        """Test reset token clearing."""
        user = User(**user_data)
        user.generate_reset_token()
        db_session.add(user)
        db_session.commit()
        
        user.clear_reset_token()
        
        assert user.reset_token is None
        assert user.reset_token_expires_at is None
    
    @patch('app.extensions.mail.send')
    def test_send_password_reset_email_success(self, mock_send, app):
        """Test successful password reset email sending."""
        with app.app_context():
            mock_send.return_value = None
            result = EmailService.send_password_reset_email(
                "test@example.com",
                "reset_token_123",
                "testuser"
            )
            
            assert result is True
            mock_send.assert_called_once()
    
    @patch('app.extensions.mail.send')
    def test_send_password_reset_email_failure(self, mock_send, app):
        """Test failed password reset email sending."""
        with app.app_context():
            mock_send.side_effect = Exception("SMTP Error")
            result = EmailService.send_password_reset_email(
                "test@example.com",
                "reset_token_123",
                "testuser"
            )
            
            assert result is False
    
    def test_forgot_password_endpoint_user_exists(self, client, db_session, user_data):
        """Test forgot password endpoint with existing user."""
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        
        with patch.object(EmailService, 'send_password_reset_email') as mock_send:
            mock_send.return_value = True
            response = client.post('/api/auth/forgot-password', json={
                'email': user.email
            })
        
        assert response.status_code == 200
        assert 'will receive a password reset link' in response.json['message']
        mock_send.assert_called_once()
    
    def test_forgot_password_endpoint_user_not_exists(self, client):
        """Test forgot password endpoint with non-existent user."""
        with patch.object(EmailService, 'send_password_reset_email') as mock_send:
            response = client.post('/api/auth/forgot-password', json={
                'email': 'nonexistent@example.com'
            })
        
        assert response.status_code == 200
        assert 'will receive a password reset link' in response.json['message']
        mock_send.assert_not_called()
    
    def test_reset_password_endpoint_success(self, client, db_session, user_data):
        """Test successful password reset."""
        user = User(**user_data)
        user.set_password("oldpassword")
        reset_token = user.generate_reset_token()
        db_session.add(user)
        db_session.commit()
        
        response = client.post('/api/auth/reset-password', json={
            'token': reset_token,
            'password': 'newsecurepassword123',
            'password_confirm': 'newsecurepassword123'
        })
        
        assert response.status_code == 200
        assert 'Password reset successful' in response.json['message']
        
        db_session.refresh(user)
        assert user.check_password('newsecurepassword123') is True
        assert user.reset_token is None
    
    def test_reset_password_endpoint_invalid_token(self, client):
        """Test password reset with invalid token."""
        response = client.post('/api/auth/reset-password', json={
            'token': 'invalid_token',
            'password': 'newpassword123',
            'password_confirm': 'newpassword123'
        })
        
        assert response.status_code == 400
        assert 'Invalid or expired reset token' in response.json['error']
    
    def test_reset_password_endpoint_expired_token(self, client, db_session, user_data):
        """Test password reset with expired token."""
        user = User(**user_data)
        user.generate_reset_token()
        user.reset_token_expires_at = datetime.utcnow() - timedelta(hours=2)
        db_session.add(user)
        db_session.commit()
        
        response = client.post('/api/auth/reset-password', json={
            'token': user.reset_token,
            'password': 'newpassword123',
            'password_confirm': 'newpassword123'
        })
        
        assert response.status_code == 400
        assert 'Invalid or expired reset token' in response.json['error']
    
    def test_reset_password_endpoint_password_mismatch(self, client, db_session, user_data):
        """Test password reset with password mismatch."""
        user = User(**user_data)
        reset_token = user.generate_reset_token()
        db_session.add(user)
        db_session.commit()
        
        response = client.post('/api/auth/reset-password', json={
            'token': reset_token,
            'password': 'password1',
            'password_confirm': 'password2'
        })
        
        assert response.status_code == 400
        assert 'Passwords do not match' in response.json['details']['password_confirm']
