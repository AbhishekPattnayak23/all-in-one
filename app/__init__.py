from flask import Flask
from flask_cors import CORS
from app.extensions import db, migrate, jwt, mail
from app.config import Config
from app.api.users import users_bp
from app.api.auth import auth_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    
    return app

app = create_app()
