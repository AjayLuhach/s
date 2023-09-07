import unittest
from app import app
from services.crud_service import crud_service
from domain.model.user_model import user_model
from infrastructure.user_database import db

class TestYourAPI(unittest.TestCase):
    def setUp(self):
        # Set up a test client and configure it
        self.app = app.test_client()
        self.app.testing = True

        # Create a test database and bind it to the app
        self.db = db
        self.db.init_app(app)
        with app.app_context():
            self.db.create_all()

        # Create any necessary test data or perform setup tasks
        # For example, create a test user
        self.test_user = user_model(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password1='testpassword'
        )
        self.db.session.add(self.test_user)
        self.db.session.commit()

    def tearDown(self):
        # Clean up after each test
        # Remove test data, close database connections, and drop the test database
        with app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_register_user(self):
        # Send a POST request to the registration endpoint with test data
        response = self.app.post('/register', json={
            'username': 'ajay',
            'password1': 'ajay',
            'first_name': 'ajay',
            'last_name': 'kumar',
            'email': 'ajayluhahc@gmail.com'
        })

        # Check if the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User registered successfully')

    def test_login(self):
        # Send a POST request to the login endpoint with test user credentials
        response = self.app.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })

        # Check if the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Login successful')

if __name__ == '__main__':
    unittest.main()
