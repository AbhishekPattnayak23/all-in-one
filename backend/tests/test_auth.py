import unittest
import json
from app import create_app, db
from app.models.user import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_successful_registration(self):
        """Test successful user registration"""
        response = self.client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Registration successful')
        self.assertEqual(data['user']['username'], 'testuser')
    
    def test_duplicate_username(self):
        """Test registration with existing username"""
        with self.app.app_context():
            User.create_user('testuser', 'test1@example.com')
        
        response = self.client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test2@example.com'
        })
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Username already taken')
    
    def test_duplicate_email(self):
        """Test registration with existing email"""
        with self.app.app_context():
            User.create_user('testuser1', 'test@example.com')
        
        response = self.client.post('/api/auth/register', json={
            'username': 'testuser2',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Email already registered')
    
    def test_invalid_email(self):
        """Test registration with invalid email"""
        response = self.client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'invalid-email'
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid email format')
    
    def test_short_username(self):
        """Test registration with short username"""
        response = self.client.post('/api/auth/register', json={
            'username': 'ab',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Username must be at least 3 characters long')
    
    def test_missing_data(self):
        """Test registration with missing data"""
        # Missing username
        response = self.client.post('/api/auth/register', json={
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 400)
        
        # Missing email
        response = self.client.post('/api/auth/register', json={
            'username': 'testuser'
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
