import os
from flask import current_app
from flask_mail import Message
from app.extensions import mail
from typing import List, Optional

class EmailService:
    """Service for sending emails."""
    
    @staticmethod
    def send_password_reset_email(user_email: str, reset_token: str, username: str) -> bool:
        """Send password reset email with token."""
        try:
            reset_url = f"{os.environ.get('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={reset_token}"
            
            subject = "Password Reset Request"
            sender = current_app.config.get('MAIL_USERNAME', 'noreply@example.com')
            
            # Create email body
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2c5aa0;">Password Reset Request</h2>
                        <p>Hello {username},</p>
                        <p>You have requested to reset your password. Please click the link below to set a new password:</p>
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{reset_url}" 
                               style="background-color: #2c5aa0; color: white; padding: 12px 24px; 
                                      text-decoration: none; border-radius: 4px;">
                                Reset Password
                            </a>
                        </div>
                        <p>If you didn't request this password reset, you can safely ignore this email.</p>
                        <p>This link will expire in 1 hour.</p>
                        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                        <p style="font-size: 12px; color: #666;">
                            If the button above doesn't work, copy and paste this URL into your browser:<br>
                            {reset_url}
                        </p>
                    </div>
                </body>
            </html>
            """
            
            text_body = f"""
Hello {username},

You have requested to reset your password. Please use the link below to set a new password:

{reset_url}

If you didn't request this password reset, you can safely ignore this email.

This link will expire in 1 hour.
            """
            
            msg = Message(
                subject=subject,
                sender=sender,
                recipients=[user_email],
                body=text_body,
                html=html_body
            )
            
            mail.send(msg)
            return True
            
        except Exception as e:
            current_app.logger.error(f"Failed to send password reset email: {str(e)}")
            return False
