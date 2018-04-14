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
        
    def test_admin_edit_book(self):
        '''test only admin can edit a book'''
        # successful admin add book
        result = self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title":"The Davinci Code", "author":"Leonardo Davinci", "edition":"2nd", "copies":3}))
        self.assertEqual(result.status_code, 201)
        # regular user edit book
        result2 = self.client().put('/api/v1/books/1', headers=dict(Authorization="Bearer " + self.user_token), content_type="application/json", data=json.dumps({"title":"Davinci's Demons"}))
        self.assertEqual(result2.status_code, 403)
        self.assertEqual("Admin privilege required", (ast.literal_eval(result2.data))["message"])
        # successful admin edit book title
        result3 = self.client().put('/api/v1/books/1', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title":"Davinci's Demons"}))
        self.assertEqual(result3.status_code, 200)
        self.assertEqual("Book 1 successfully edited", (ast.literal_eval(result3.data))["message"])
        # empty fields
        result4 = self.client().put('/api/v1/books/1', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({}))
        self.assertEqual(result4.status_code, 400)
        self.assertEqual("Enter valid data for edit", (ast.literal_eval(result4.data))["message"])
        # empty strings
        result5 = self.client().put('/api/v1/books/1', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title": ""}))
        self.assertEqual(result5.status_code, 400)
        self.assertEqual("all fields cannot be empty enter data to edit", (ast.literal_eval(result5.data))["message"])
        # non-existent book
        result6 = self.client().put('/api/v1/books/20', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title": ""}))
        self.assertEqual(result6.status_code, 404)
        self.assertEqual("book doesn't exist", (ast.literal_eval(result6.data))["message"])
        # invalid data
        result7 = self.client().put('/api/v1/books/1', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title": "   "}))
        self.assertEqual(result7.status_code, 400)
        self.assertEqual("Enter vaild data", (ast.literal_eval(result7.data))["message"])
        # invalid data in copies
        result8 = self.client().put('/api/v1/books/1', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"copies": "four"}))
        self.assertEqual(result8.status_code, 400)
        self.assertEqual("Field copies has to be an integer and cannot be a negative number", (ast.literal_eval(result8.data))["message"])
        # invalid status
        result9 = self.client().put('/api/v1/books/1', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"status": "gibberish"}))
        self.assertEqual(result9.status_code, 400)
        self.assertEqual("status has to be either available or unavailble", (ast.literal_eval(result9.data))["message"])
        
    def test_admin_delete_book(self):
        '''test only admin can delete book'''
        # successful admin add book
        result = self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title":"The Davinci Code", "author":"Leonardo Davinci", "edition":"2nd", "copies":3}))
        self.assertEqual(result.status_code, 201)
        # regular user delete book
        result2 = self.client().delete('/api/v1/books/1', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result2.status_code, 403)
        self.assertEqual("Admin privilege required", (ast.literal_eval(result2.data))["message"])
        #non-existent book
        result3 = self.client().delete('/api/v1/books/20', headers=dict(Authorization="Bearer " + self.admin_token))
        self.assertEqual(result3.status_code, 404)
        self.assertEqual("book 20 doesn't exist", (ast.literal_eval(result2.data))["message"])
        #successful admin delete book
        result4 = self.client().delete('/api/v1/books/1', headers=dict(Authorization="Bearer " + self.admin_token))
        self.assertEqual(result4.status_code, 200)
        self.assertEqual("book 1 deleted successfully", (ast.literal_eval(result4.data))["message"])
        #assert book has been deleted
        result5 = self.client().get('/api/v1/books/1')
        self.assertEqual(result5.status_code, 404)
        
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
