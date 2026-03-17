from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from app import db
        db.create_all()
    
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', '1') == '1')
