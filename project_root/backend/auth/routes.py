from flask import Blueprint, request, jsonify
from services.user_store import UserStore
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
user_store = UserStore()
auth_service = AuthService()

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login endpoint - validate credentials and return JWT token."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        user = user_store.validate_user_credentials(email, password)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        token = auth_service.generate_token(user)
        
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register endpoint - create new user."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('firstName', '')
        last_name = data.get('lastName', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        try:
            user = user_store.create_user(email, password, first_name=first_name, last_name=last_name)
            token = auth_service.generate_token(user)
            
            return jsonify({
                'token': token,
                'user': user.to_dict()
            }), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 409
            
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    """Verify JWT token validity."""
    from middleware.auth import require_auth
    
    @require_auth
    def verify():
        return jsonify({
            'valid': True,
            'user': request.current_user
        }), 200
    
    return verify()
