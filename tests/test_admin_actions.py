'''tests/test_admin_actions.py'''
import unittest
import json
import ast
from application import create_app, db

class AuthenticationTestCase(unittest.TestCase):
    '''class representing BookModel Test case'''
    
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()
        # register and login admin
        self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Shalon", "username": "shalon", "email": "shalon@to.com", "password": "Test123", "confirm_password": "Test123", "admin":"true"}))
        admin_login = ast.literal_eval((self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"shalon", "password":"Test123"}))).data)
        self.admin_token = admin_login["token"]
        # register and login regular user
        self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Njeri", "username": "njeri", "email": "njeri@to.com", "password": "Test123", "confirm_password": "Test123"}))
        user_login = ast.literal_eval((self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"njeri", "password":"Test123"}))).data)
        self.user_token = user_login["token"]
    
    def test_admin_add_book(self):
        '''test only admin can add book'''
        # regular user add book
        result = self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + self.user_token), content_type="application/json", data=json.dumps({"title":"The Davinci Code", "author":"Leonardo Davinci", "edition":"2nd", "copies":3}))
        self.assertEqual(result.status_code, 403)
        self.assertEqual("Admin privilege required", (ast.literal_eval(result.data))["message"])        
        # successful admin add book
        result2 = self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title":"The Davinci Code", "author":"Leonardo Davinci", "edition":"2nd", "copies":3}))
        self.assertEqual(result2.status_code, 201)
        self.assertEqual("Book successfully added", (ast.literal_eval(result2.data))["message"])
        # adding the same book twice
        result3 = self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title":"The Davinci Code", "author":"Leonardo Davinci", "edition":"2nd", "copies":3}))
        self.assertEqual(result3.status_code, 409)
        self.assertEqual("Add book failed. Book title already exists", (ast.literal_eval(result3.data))["message"])
        # no data in fields
        result4 = self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({}))
        self.assertEqual(result4.status_code, 400)
        self.assertEqual("Fields cannot be empty", (ast.literal_eval(result4.data))["message"])
        # empty strings in field
        result5 = self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title":"", "author":"", "edition":"", "copies":3}))
        self.assertEqual(result5.status_code, 400)
        self.assertEqual("title, author, edition or copies fields missing", (ast.literal_eval(result5.data))["message"])
        # invalid data
        result6 = self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title":"   ", "author":"Leornado Davinci", "edition":"2nd", "copies":3}))
        self.assertEqual(result6.status_code, 400)
        self.assertEqual("Enter valid data", (ast.literal_eval(result6.data))["message"])
        # negative numbers entered in copies field
        result7 = self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title":"The Davinci Code", "author":"Leornado Davinci", "edition":"2nd", "copies":-3}))
        self.assertEqual(result7.status_code, 400)
        self.assertEqual("Copies entered cannot be a negative number", (ast.literal_eval(result7.data))["message"])
        
        
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
