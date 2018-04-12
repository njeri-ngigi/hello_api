'''tests/test_authentication.py'''
import unittest
import json
import ast
from application import create_app, db

class ChangePasswordTestCase(unittest.TestCase):
    '''class representing BookModel Test case'''
    
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()

        self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Shalon", "username": "shalon", "email": "shalon@to.com", "password": "Test123", "confirm_password": "Test123"}))
        login = self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"shalon", "password":"Test123"}))
        
        self.token = (ast.literal_eval(login.data))["token"]
    
    def test_change_password(self):
        '''test api can change user password'''
        #successful change password
        result = self.client().put('/api/v1/auth/change-password', headers=dict(Authorization="Bearer " + self.token), content_type="application/json", data=json.dumps({"old_password":"Test123", "new_password":"Here123", "confirm_password":"Here123"}))
        self.assertEqual(result.status_code, 200)
        self.assertEqual("password changed successfully", (ast.literal_eval(result.data))["message"])
        #empty fields
        result2 = self.client().put('/api/v1/auth/change-password', headers=dict(Authorization="Bearer " + self.token), content_type="application/json", data=json.dumps({}))
        self.assertEqual(result2.status_code, 400)
        self.assertEqual("Fields cannot be empty", (ast.literal_eval(result2.data))["message"])
        #missing old_password or new_password
        result3 = self.client().put('/api/v1/auth/change-password', headers=dict(Authorization="Bearer " + self.token), content_type="application/json", data=json.dumps({"old_password":None, "new_password":"Here123", "confirm_password":"Here123"}))
        self.assertEqual(result3.status_code, 400)
        self.assertEqual("old_password or new_password fields missing", (ast.literal_eval(result3.data))["message"])
        #invalid data
        result4 = self.client().put('/api/v1/auth/change-password', headers=dict(Authorization="Bearer " + self.token), content_type="application/json", data=json.dumps({"old_password":"   ", "new_password":"Here123", "confirm_password":"Here123"}))
        self.assertEqual(result4.status_code, 400)
        self.assertEqual("enter valid data", (ast.literal_eval(result4.data))["message"])
        #incorrect old_password
        result5 = self.client().put('/api/v1/auth/change-password', headers=dict(Authorization="Bearer " + self.token), content_type="application/json", data=json.dumps({"old_password":"test123", "new_password":"Here123", "confirm_password":"Here123"}))
        self.assertEqual(result5.status_code, 401)
        self.assertEqual("Incorrect password", (ast.literal_eval(result5.data))["message"])

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
