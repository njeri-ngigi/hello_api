'''resources.py'''
import random
import string
from flask import request
from werkzeug.security import check_password_hash
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_raw_jwt, get_jwt_claims, get_jwt_identity)
from validate import Validate
from models import BookModel, UserModel, RevokedTokenModel


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
    
        if UserModel.query.filter_by(username=v["username"]).first():
            return {"message": "Add user failed. Username already exists"}, 200
        if UserModel.query.filter_by(email=v["email"]).first():
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
        
        return {"message": "Admin has to be True or left empty"}, 200      

class Login(Resource):
    '''login user by verifying password and creating an access token'''
    def post(self):
        '''method ['POST']'''
        data = request.get_json()
        if not data:
            return {"message": "Fields cannot be empty"}
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"message": "Username or password missing"}

        user_object = UserModel.query.filter_by(username=username).first()
        if user_object is None:
            return {"message": "Incorrect username"}, 401

        if check_password_hash(user_object.password, password) is True:
            access_token = create_access_token(identity=user_object)
            return dict(token=access_token, message="Login successful"), 200

        return {"message": "Incorrect password"}, 401
'''class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"access_token": access_token}'''

class Logout(Resource):
    @jwt_required
    def post(self):
        '''logout user by revoking token'''
        json_token_identifier = get_raw_jwt()['jti']

        revoked_token = RevokedTokenModel(json_token_identifier=json_token_identifier)
        revoked_token.save()
        return {"message": "Successfully logged out"}, 200

'''class LogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        json_token_identifier = get_raw_jwt()['jti']
        revoked_token = RevokedTokenModel(json_token_identifier=json_token_identifier)
        revoked_token.save()
        return {"message":"refresh token has been revoked"}'''

class ResetPassword(Resource):
    def post(self):
        '''Reset a password'''
        username = request.get_json().get('username')
        if not username:
            return {"message":"Enter username"}
        my_user = UserModel.query.filter_by(username=username).first()
        if my_user is not None:
            new_password = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
            UserModel.reset_password(new_password)

            reset_token = create_access_token(identity="reset_password")
            return {"reset_token": reset_token}

        return {"message":"Incorrect username"}

class ChangePassword(Resource):
    @jwt_required
    def put(self):
        '''Change a password'''
        pass        

class BorrowAndReturnBook(Resource):
    @jwt_required
    def post(self, book_id):
        '''Borrow a book'''
        pass 
    @jwt_required
    def put(self):
        '''Return a book'''
        pass

class UserHistory(Resource):
    @jwt_required
    def get(self):
        '''User's book history'''
        pass

class BooksNotReturned(Resource):
    @jwt_required
    def get(self):
        '''Books not yet returned'''
        pass

class Books(Resource):
    def get(self):
        '''retrieve all books'''
        pass
    @jwt_required
    def post(self):
        '''Only admin can add a book'''
        claims = get_jwt_claims()
        
        if claims["admin"] is True:
            data = request.get_json()
            if not data:
                return {"message": "Fields cannot be empty"}, 200

            title = data.get('title')
            author = data.get('author')
            edition = data.get('edition')
            copies = data.get('copies')

            my_list = [title, author, edition, copies]
            for i in my_list:
                if i is None or not i:
                    return {"message": "title, author, edition or copies fields missing"}, 200
            my_list = [title, author, edition]
            for i in my_list:
                i = i.strip()
                if not i:
                    return {"message": "Enter valid data"}


            if not isinstance(copies, int):
                return {"message": "Field copies has to be an integer"}, 200
            if copies < 0:
                return {"message": "Copies entered cannot be a negative number"}, 200
            if copies == 0:
                status = "unavailable"
            status = "available"

            
            if BookModel.query.filter_by(title=title).first():
                return {"message": "Add book failed. Book title already exists"}, 200
            my_book = BookModel(author, title, edition, copies, status)
            my_book.save()
            return {"message": "Book successfully added"}, 201
        return {"message": "Admin privilege required"}

class BooksBookId(Resource):
    '''class representing book by id actions'''
    def get(self):
        '''retrieve a single book'''
        pass

    @jwt_required
    def put(self):
        '''Only admin can edit a book'''
        claims = get_jwt_claims()
        if claims["admin"] is True:
            pass

        return {"message": "Admin privilege required"} 
    @jwt_required
    def delete(self):
        '''Only admin can delete a book'''
        claims = get_jwt_claims()
        if claims["admin"] is True:
            pass

        return {"message": "Admin privilege required"}

