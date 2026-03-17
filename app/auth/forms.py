from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=4, max=20, message="Username must be between 4 and 20 characters"),
        Regexp('^[A-Za-z0-9_]+$', message="Username can only contain letters, numbers, and underscores")
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address"),
        Length(max=120, message="Email must be under 120 characters")
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, max=128, message="Password must be between 8 and 128 characters"),
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]', 
               message="Password must contain at least one uppercase, lowercase, number and special character")
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])
    
    submit = SubmitField('Create Account')
    
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already exists")
    
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered")
