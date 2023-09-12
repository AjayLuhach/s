# tests.py

import unittest
from flask import Flask
from flask_testing import TestCase
from app import app, db, user_model

class TestCRUDAPI(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ajay@localhost:5432/test_db'
        return app

    def setUp(self):
        db.create_all()
        user = user_model(username='testuser', email='test@example.com',first_name='testuser',last_name='test',password1='testhj')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        url = '/create?username=newuser1&email=new@example.com&first_name=newuser&last_name=newuser&password1=test'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        print(' Sa')
        
    def test_delete_user(self):
        url = '/delete?username=testuser'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        user = user_model.query.filter_by(username='testuser').first()
        self.assertIsNone(user)
        print(" Ra")

    def test_search_user(self):
        url = '/search?username=testuser'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        user_data = response.json

        # Print the user data to the console for inspection
        print("User Data:")
        print(user_data)

        # Add assertions to check for correct data retreival 
        self.assertEqual(user_data['username'], 'testuser')
        self.assertEqual(user_data['first_name'], 'testuser')
        self.assertEqual(user_data['last_name'], 'test')
        self.assertEqual(user_data['email'], 'test@example.com')
        print("Assertions completed.")

    def test_update_user(self):
        url = '/update?username=testuser&first_name=newname&last_name=newlastname&email=new@example.com&password1=newpassword'
        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)
        user = user_model.query.filter_by(username='testuser').first()
        self.assertEqual(user.first_name, 'newname')
        self.assertEqual(user.last_name, 'newlastname')
        self.assertEqual(user.email, 'new@example.com')
        print(" Ma")    


    
if __name__ == '__main__':
    unittest.main()
