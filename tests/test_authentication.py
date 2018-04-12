'''tests/test_authentication.py'''
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

        self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Shalon", "username": "shalon", "email": "shalon@to.com", "password": "Test123", "confirm_password": "Test123"}))
        
    def test_login(self):
        '''test user can login'''
        #login successful
        result = self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"shalon", "password":"Test123"}))
        self.assertEqual(result.status_code, 200)
        self.assertIn("token", result.data)
        #no data passed
        result2 = self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({}))
        self.assertEqual(result2.status_code, 400)
        my_data2 = ast.literal_eval(result2.data)
        self.assertEqual("Fields cannot be empty", my_data2["message"])
        #empty strings
        result3 = self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"", "password":""}))
        self.assertEqual(result3.status_code, 400)
        my_data3 = ast.literal_eval(result3.data)
        self.assertEqual("Username or password missing", my_data3["message"])
        #incorrect username
        result4 = self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"sharon", "password":"Test123"}))
        self.assertEqual(result4.status_code, 401)
        my_data4 = ast.literal_eval(result4.data)
        self.assertEqual("Incorrect username", my_data4["message"])
        #incorrect password
        result5 = self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"shalon", "password":"test123"}))
        self.assertEqual(result5.status_code, 401)
        my_data5 = ast.literal_eval(result5.data)
        self.assertEqual("Incorrect password", my_data5["message"])

    def test_logout(self):
        '''test user can logout'''
        #login
        result = self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"shalon", "password":"Test123"}))
        self.assertEqual(result.status_code, 200)
        my_data = ast.literal_eval(result.data)
        token = my_data["token"]
        #logout
        result2 = self.client().post('/api/v1/auth/logout', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(result2.status_code, 200)
        self.assertEqual("Successfully logged out", (ast.literal_eval(result2.data))["message"])

    def test_reset_password(self):
        '''test user can reset password'''
        result = self.client().post('/api/v1/auth/reset-password', content_type="application/json", data=json.dumps({"username":"shalon"}))
        self.assertEqual(result.status_code, 200)
        self.assertIn("reset_token", result.data)
        self.assertIn("reset_password", result.data)
        reset_token = (ast.literal_eval(result.data))["reset_token"]
        reset_password = (ast.literal_eval(result.data))["reset_password"]
        self.assertEqual(len(reset_password), 7)
        #username not entered
        result2 = self.client().post('/api/v1/auth/reset-password', content_type="application/json", data=json.dumps({}))
        self.assertEqual(result2.status_code, 400)
        self.assertEqual("Enter username", (ast.literal_eval(result2.data))["message"])
        #incorrect username
        result3 = self.client().post('/api/v1/auth/reset-password', content_type="application/json", data=json.dumps({"username":"sharon"}))
        self.assertEqual(result3.status_code, 404)
        self.assertEqual("User doesn't exist", (ast.literal_eval(result3.data))["message"])
        #missing password fields in change password endpoint
        result4 = self.client().put('/api/v1/auth/change-password', content_type="application/json", headers=dict(Authorization="Bearer " + reset_token), data=json.dumps({"reset_password":None, "new_password":"", "confirm_password":""}))
        self.assertEqual(result4.status_code, 400)
        self.assertEqual("reset password or new password fields missing", (ast.literal_eval(result4.data))["message"])
        #missing fields in change password endpoint
        result5 = self.client().put('/api/v1/auth/change-password', content_type="application/json", headers=dict(Authorization="Bearer " + reset_token), data=json.dumps({}))
        self.assertEqual(result5.status_code, 400)
        self.assertEqual("Fields can't be empty", (ast.literal_eval(result5.data))["message"])
        #incorrect reset password in change password endpoint
        result6 = self.client().put('/api/v1/auth/change-password', content_type="application/json", headers=dict(Authorization="Bearer " + reset_token), data=json.dumps({"reset_password":"randomPassword", "new_password":"Hello_123", "confirm_password":"Hello_123"}))
        self.assertEqual(result6.status_code, 401)
        self.assertEqual("incorrect reset password", (ast.literal_eval(result6.data))["message"])
        #successful change password
        result7 = self.client().put('/api/v1/auth/change-password', content_type="application/json", headers=dict(Authorization="Bearer " + reset_token), data=json.dumps({"reset_password": reset_password, "new_password": "Hello_123", "confirm_password": "Hello_123"}))
        self.assertEqual(result7.status_code, 200)
        self.assertEqual("password changed successfully", (ast.literal_eval(result7.data))["message"])
        

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
