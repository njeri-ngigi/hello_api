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

    def test_register_user(self):
        '''test handling user registration'''
        #test successfull user registration
        result = self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Njeri Ngigi", "username": "njeri-ngigi", "email": "njeri@to.com", "password": "Test123", "confirm_password": "Test123"}))
        my_data = ast.literal_eval(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual("User successfully added", my_data["message"])
        #test double registration of the same user
        result2 = self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Njeri Ngigi", "username": "njeri-ngigi", "email": "njeri@to.com", "password": "Test123", "confirm_password": "Test123"}))
        my_data2 = ast.literal_eval(result2.data)
        self.assertEqual(result2.status_code, 409)
        self.assertEqual("Add user failed. Username already exists", my_data2["message"])
        #test registration using an already existent email
        result3 = self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Shalon Njeri", "username": "shalon-njeri", "email": "njeri@to.com", "password": "Test123", "confirm_password": "Test123"}))
        my_data3 = ast.literal_eval(result3.data)
        self.assertEqual(result3.status_code, 409)
        self.assertEqual("Add user failed. Email entered already exists", my_data3["message"])
        #test successful registration of admin
        result4 = self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Shalon", "username": "shalon", "email": "shalon@to.com", "password": "Test123", "confirm_password": "Test123", "admin": "true"}))
        my_data4 = ast.literal_eval(result4.data)
        self.assertEqual(result4.status_code, 201)
        self.assertEqual("Admin user successfully added", my_data4["message"])
        #test registration of admin with invalid admin value
        result5 = self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Shalon", "username": "shalon1", "email": "shalon1@to.com", "password": "Test123", "confirm_password": "Test123", "admin": "giberish"}))
        my_data5 = ast.literal_eval(result5.data)
        self.assertEqual(result5.status_code, 400)
        self.assertEqual("Admin has to be True or left empty", my_data5["message"])
        #test registration using empty fields
        result6 = self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({}))
        my_data6 = ast.literal_eval(result6.data)
        self.assertEqual(result6.status_code, 400)
        self.assertEqual("Fields cannot be empty", my_data6["message"])
        #test registration using empty data strings
        result7 = self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Shalon", "username": None, "email": None, "password": None, "confirm_password": None}))
        my_data7 = ast.literal_eval(result7.data)
        self.assertEqual(result7.status_code, 400)
        self.assertEqual("name, username, email, password or confirm_password fields missing", my_data7["message"])

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
