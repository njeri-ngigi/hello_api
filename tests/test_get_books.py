'''tests/test_get_books.py'''
import unittest
import json
import ast
from application import create_app, db

class GetBooksTestCase(unittest.TestCase):
    '''class representing BookModel Test case'''
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()

        #register and login admin to add books for subsequent tests
        self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps({"name": "Shalon", "username": "shalon", "email": "shalon@to.com", "password": "Test123", "confirm_password": "Test123", "admin": "true"}))
        my_result = self.client().post('/api/v1/auth/login', content_type="application/json", data=json.dumps({"username":"shalon", "password":"Test123"}))
        login = ast.literal_eval(my_result.data)
        token = login["token"]
        self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + token), content_type="application/json", data=json.dumps({"title":"I am here", "author":"Kimemia", "edition":"7th", "copies":12}))
        self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + token), content_type="application/json", data=json.dumps({"title":"Dandy Daddy", "author":"Macey Mace", "edition":"2nd", "copies":3}))
        self.client().post('/api/v1/books', headers=dict(Authorization="Bearer " + token), content_type="application/json", data=json.dumps({"title":"There's something you don't know", "author":"Macey Mace", "edition":"2nd", "copies":3}))

    def test_get_all_books(self):
        '''test to get all books'''
        result = self.client().get('/api/v1/books')
        self.assertEqual(result.status_code, 200)
        self.assertIn("I am here", result.data)
        self.assertIn("Macey Mace", result.data)

    def test_get_books_by_user_limit(self):
        '''test pagination, get books by user limit'''
        result = self.client().get('/api/v1/books?limit=2')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(2, len(ast.literal_eval(result.data)))

    def test_get_single_book_by_id(self):
        '''test to get single book by id'''
        #test successful book retrieval
        result = self.client().get('/api/v1/books/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn("I am here", result.data)
        #test non-exixtent book id
        result2 = self.client().get('/api/v1/books/20')
        self.assertEqual(result2.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
