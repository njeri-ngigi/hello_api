import unittest
import json
import ast
from hello_api import app


class BooksTestCase(unittest.TestCase):
    '''Class representing Books Testcase'''

    def setUp(self):
        self.app = app.create_app(config_name="testing")
        self.client = self.app.test_client
        self.book = json.dumps({'title':'Go home, susan',
                     'author':'Mary Mary', 'edition':'4th',
                     'book_id':1, 'status':'available', 'copies':1})
        self.user = json.dumps({"name":"Kimani", "username":"kymani",
                                "email":"kymani@example.com", "password":"where",
                                "confirm_password":"where"})

        #binds the app to the current context
        with self.app.app_context():
            #create all tables
            app.db.create_all()
    def test_get_all_books(self):
        '''Test API can retrieve all books'''
        pass
    def test_get_single_book(self):
        '''Test API can retrieve single book'''
        result = self.client().post('/api/v1/books', data=self.book, content_type="application/json")
        self.assertEqual(result.status_code, 201)

        result2 = self.client().get('/api/v1/books/1')
        self.assertEqual(result2.status_code, 200)
        self.assertIn("Go home, Susan", result2.data)

    def test_add_book(self):
        '''Test API can add a book'''
        result = self.client().post('/api/v1/books', data=self.book, content_type="application/json")
        self.assertEqual(result.status_code, 201)
        self.assertIn('Go home, susan', result.data)

    def test_edit_book(self):
        '''Test API can edit a book'''
        result = self.client().post('/api/v1/books', data=self.book,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)
        result2 = self.client().put('/api/v1/books/1',
                                   data=json.loads({"title": "Go home, Robert"}), content_type="application/json")
        my_data = ast.literal_eval(result2.data)
        self.assertEqual(result2.status_code, 200)
        self.assertEqual('Book edited successfully', my_data["message"])

    def test_delete_book(self):
        '''Test API can delete book'''
        result = self.client().post('/api/v1/books', data=self.book,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)
        result2 = self.client().delete('/api/v1/books/1')
        self.assertEqual(result2.status_code, 204)
        self.assertEqual("Book 1 deleted successfully", ast.literal_eval(result2.data)["message"])
        
        #test if book is deleted
        result3 = self.client().get('.api/v1/books/1')
        self.assertEqual(result3.status_code, 404)

    def test_user_actions(self):
        '''Test a user can register, login, borrow and return a book and logout'''
        #test register
        result = self.client().post('/api/v1/auth/register')
        self.assertEqual(result.status_code, 201)
        self.assertIn("User successfully registered", result.data)

        #test login
        result2 = self.client().post('/api/v1/auth/login', data=json.dumps({"username":"kymani","password":"where"}), content_type='application/json')
        a_token = ast.literal_eval(result2.data)
        self.assertEqual(result.status_code, 200)
        self.assertIn("token", result2.data)

        #test borrow book
        result3 = self.client().post('/api/v1/books', data=self.book,
                                     content_type="application/json")
        self.assertEqual(result3.status_code, 201)
        result4 = self.client().post('api/v1/users/books/1',
                                     headers=dict(Authorization="Bearer "+a_token))
        result5 = self.client().post('api/v1/users/books/1',
                                     headers=dict(Authorization="Bearer "+a_token))
        self.assertEqual(result4.status_code, 200)
        self.assertIn("Book successfully checked out", result4.data)
        self.assertEqual(result5.status_code, 404)
        self.assertIn("Book is currently unavailable", result5.data)
        
        #test return book
        result6 = self.client().put('/api/v1/users/books/1',
                                    headers=dict(Authorization="Bearer "+a_token))
        self.assertEqual(result6.status_code, 200)
        self.assertIn("Book returned successfully", result6.data)

if __name__ == "__main__":
    unittest.main()


    
