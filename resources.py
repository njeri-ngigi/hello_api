'''resources.py'''
from flask import request
from flask_restful import Resource
from validate import Validate
from models import BookModel, UserModel

class Registration(Resource):
    '''Register a user'''
    def post(self):
        '''method ['POST']'''
        data = request.get_json()
        if not data:
            return {"message": "Fields cannot be empty"}, 200
        v = Validate().validate_register(data)

        if "message" in v:
            return v, 200

        admin = data.get('admin')
    
        if UserModel.query.filter_by(username=v["username"]).first() is not None:
            return {"message": "Add user failed. Username already exists"}, 200
        if UserModel.query.filter_by(email=v["email"]).first() is not None:
            return {"message": "Add user failed. Email entered already exists"}, 200
        if not admin:
            my_user = UserModel(username=v["username"], name=v["name"],
                                email=v["email"], password=v["password"])
            my_user.save()
            return {"message": "User successfully added"}, 201

        if admin == "True" or admin == "true":
            my_user = UserModel(username=v["username"], name=v["name"],
                                email=v["email"], password=v["password"], admin=True)
            my_user.save()
            return {"message": "Admin user successfully added"}, 201
        
        return {"message": "Admin has to be True or empty"}, 200      

class Login(Resource):
    def post(self):
        '''Login a user'''
        pass

class Logout(Resource):
    def post(self):
        '''Logout a user'''
        pass

class ResetPassword(Resource):
    def post(self):
        '''Reset a password'''
        pass

class ChangePassword(Resource):
    def put(self):
        '''Change a password'''
        pass

class BorrowBook(Resource):
    def post(self):
        '''Borrow a book'''
        pass
    
    def put(self):
        '''Return a book'''
        pass

class UserHistory(Resource):
    def get(self):
        '''User's book history'''
        pass

class BooksNotReturned(Resource):
    def get(self):
        '''Books not yet returned'''
        pass

class Books(Resource):
    def get(self):
        '''return all books'''
        pass

    def post(self):
        '''add a book'''
        pass

class BooksBookId(Resource):
    def get(self):
        '''return a single book'''
        pass
    
    def put(self):
        '''edit a book'''
        pass

    def delete(self):
        '''delete a book'''
        pass

