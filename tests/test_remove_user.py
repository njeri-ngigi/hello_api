'''tests/test_register_user.py'''
import unittest
import json
import ast
from application import create_app, db


class RegisterUserTestCase(unittest.TestCase):
    '''class representing BookModel Test case'''

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()

        # register and login regular user
        self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Jay Jay", "username": "jay", "email": "j@to.com", "password": "Test123", "confirm_password": "Test123"}))
        user_login = ast.literal_eval((self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"jay", "password":"Test123"}))).data)
        self.user_token = user_login["token"]
        # register and login admin
        self.client().post('/api/v1/auth/register?admin=true', content_type="application/json", data=json.dumps({"name": "Shalon", "username": "shalon", "email": "shalon@to.com", "password": "Test123", "confirm_password": "Test123"}))
        admin_login = ast.literal_eval((self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"shalon", "password":"Test123"}))).data)
        self.admin_token = admin_login["token"]
        #admin add book
        self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title":"Don't", "author": "Eddy", "edition":"1st", "copies": 3}))

    def test_unsuccessful_remove(self):
        '''test a user cannot delete account while having unreturned books'''
        # borrow a book
        result = self.client().post('api/v1/users/books/1', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result.status_code, 200)
        # delete account with unreturned book
        result2 = self.client().delete('api/v1/auth/remove-user', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result2.status_code, 403)
        self.assertEqual("Return all books to delete user account", (ast.literal_eval(result2.data))["message"])
    
    def test_remove_user_account(self):
        '''test successful remove user account'''
        result = self.client().delete('api/v1/auth/remove-user', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result.status_code, 200)
        self.assertEqual("user account successfully deleted", (ast.literal_eval(result.data))["message"])
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
