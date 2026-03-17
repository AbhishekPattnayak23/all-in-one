from flask import Blueprint
from app.api.auth.password_reset import password_reset_bp

auth_bp = Blueprint('auth', __name__)
auth_bp.register_blueprint(password_reset_bp)

__all__ = ['auth_bp']
