from flask import Flask
from flask_cors import CORS
from auth.routes import auth_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'message': 'Server is running'}
    
    return app

if __name__ == '__main__':
    import os
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
