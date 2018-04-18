'''tests/test_user_books.py'''
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
        self.client().post('/api/v1/auth/register?admin=true', content_type="application/json", data=json.dumps({"name": "Shalon", "username": "shalon", "email": "shalon@to.com", "password": "Test123", "confirm_password": "Test123"}))
        admin_login = ast.literal_eval((self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"shalon", "password":"Test123"}))).data)
        self.admin_token = admin_login["token"]
        # register and login 2 regular users
        self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Jay Jay", "username": "jay", "email": "j@to.com", "password": "Test123", "confirm_password": "Test123"}))
        user_login = ast.literal_eval((self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"jay", "password":"Test123"}))).data)
        self.user_token = user_login["token"]
        self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Sasha", "username": "sasha", "email": "sasha@to.com", "password": "Test123", "confirm_password": "Test123"}))
        user2_login = ast.literal_eval((self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"sasha", "password":"Test123"}))).data)
        self.user2_token = user2_login["token"]
        # add books
        self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title":"Don't", "author": "Eddy", "edition":"1st", "copies": 3}))
        self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title":"Cool Cool Cool!", "author": "Abed Nadir", "edition":"1st", "copies": 4}))
        #add unavailable book
        self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + self.admin_token), content_type="application/json", data=json.dumps({"title":"Away from home", "author": "Maya Kashigawa", "edition":"1st", "copies": 0}))
    
    def test_borrow_book(self):
        '''test user can borrow book'''
        # test successful borrow book
        result = self.client().post('api/v1/users/books/1', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result.status_code, 200)
        self.assertEqual("book successfully checked out", (ast.literal_eval(result.data))["message"])
        # test borrow same book twice
        result2 = self.client().post('api/v1/users/books/1', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result2.status_code, 409)
        self.assertEqual("You can't borrow the same book twice", (ast.literal_eval(result2.data))["message"])
        #test borrow non-existent book
        result3 = self.client().post('api/v1/users/books/20', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result3.status_code, 404)
        self.assertEqual("book doesn't exist", (ast.literal_eval(result3.data))["message"])
        #test borrow unavailable book
        result4 = self.client().post('api/v1/users/books/3', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result4.status_code, 403)
        self.assertEqual("book is currently unavailable", (ast.literal_eval(result4.data))["message"])

    def test_return_book(self):
        '''test user can return a book'''
        # borrow a book
        result = self.client().post('api/v1/users/books/2', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result.status_code, 200)
        #successful user return book
        result2 = self.client().put('api/v1/users/books/2', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result2.status_code, 200)
        self.assertEqual("book 2 successfully returned", (ast.literal_eval(result2.data))["message"])
        # returning a book twice
        result3 = self.client().put('api/v1/users/books/2', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result3.status_code, 403)
        self.assertEqual("You haven't borrowed this book", (ast.literal_eval(result3.data))["message"])
        #returning a book that doesn't exist
        result4 = self.client().put('api/v1/users/books/20', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result4.status_code, 404)
        self.assertEqual("book 20 you are trying to access doesn't exist", (ast.literal_eval(result4.data))["message"])
        # returning a book not yet borrowed
        result5 = self.client().put('api/v1/users/books/3', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result5.status_code, 403)
        self.assertEqual("You haven't borrowed this book", (ast.literal_eval(result5.data))["message"])

    def test_user_history(self):
        '''test to return a user's history'''
        # user borrow book
        self.client().post('api/v1/users/books/1', headers=dict(Authorization="Bearer " + self.user_token))
        self.client().post('api/v1/users/books/2', headers=dict(Authorization="Bearer " + self.user_token))
        # user return book
        self.client().put('api/v1/users/books/2', headers=dict(Authorization="Bearer " + self.user_token))
        result = self.client().get('api/v1/users/books', headers=dict(Authorization="Bearer " + self.user_token)) 
        self.assertEqual(result.status_code, 200)
        # test user with no borrowing history
        result2 = self.client().get('api/v1/users/books', headers=dict(Authorization="Bearer " + self.user2_token))
        self.assertEqual(result2.status_code, 200)
        self.assertEqual([], (ast.literal_eval(result2.data))["sasha"])

    def test_user_books_not_returned(self):
        '''test user books not yet returned'''
        #user borrow book
        self.client().post('api/v1/users/books/1', headers=dict(Authorization="Bearer " + self.user_token))
        result = self.client().get('api/v1/users/books?returned=false', headers=dict(Authorization="Bearer " + self.user_token))
        self.assertEqual(result.status_code, 200)
        # test user with no borrowing history
        result2 = self.client().get('api/v1/users/books?returned=false', headers=dict(Authorization="Bearer " + self.user2_token))
        self.assertEqual(result2.status_code, 200)
        self.assertEqual([], (ast.literal_eval(result2.data))["sasha"])

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
