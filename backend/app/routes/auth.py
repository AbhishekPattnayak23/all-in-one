from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from email_validator import validate_email, EmailNotValidError

auth_bp = Blueprint('auth', __name__)

def validate_registration_data(data):
    """Validate username and email format"""
    if not data.get('username') or len(data['username'].strip()) < 3:
        return False, "Username must be at least 3 characters long"
    
    if not data.get('email'):
        return False, "Email is required"
    
    try:
        validate_email(data['email'])
    except EmailNotValidError:
        return False, "Invalid email format"
    
    return True, None

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate input
        is_valid, validation_error = validate_registration_data(data)
        if not is_valid:
            return jsonify({'error': validation_error}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        
        # Check for existing username
        if User.username_exists(username):
            return jsonify({'error': 'Username already taken'}), 409
        
        # Check for existing email
        if User.email_exists(email):
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        user = User.create_user(username=username, email=email)
        
        return jsonify({
            'message': 'Registration successful',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500
