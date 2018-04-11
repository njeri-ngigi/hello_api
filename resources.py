'''resources.py'''
import random
import string
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash
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
        data = request.get_json()
        if not data:
            return {"message":"Enter username"}
        username = data.get('username')
        user = UserModel.query.filter_by(username=username).first()
        if user is not None:
            generated_password = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
            
            user.reset_password = generate_password_hash(generated_password)
            user.save()
            reset_token = create_access_token(identity=user)
            return dict(reset_token=reset_token, reset_password=generated_password)

        return {"message":"User doesn't exist"}


class ChangePassword(Resource):
    @jwt_required
    def put(self):
        '''Change a password'''
        claims = get_jwt_claims()
        reset = claims["reset_password"].encode('ascii')
        if reset != "false":
            data = request.get_json()
            if not data:
                return dict(message="Fields can't be empty")
            reset_password = data.get("reset_password")
            new_password = data.get("new_password")
            confirm_password = data.get("confirm_password")

            if not reset_password and not new_password:
                dict(message="reset password or new password fields missing")

            if new_password != confirm_password:
                return dict(message="passwords don't match")
            
            user_identity = get_jwt_identity()
            user = UserModel.query.filter_by(username=user_identity).first()
            if check_password_hash(reset, reset_password) is True:
                user.password = generate_password_hash(new_password)
                user.reset_password = False
                user.save()
                return dict(message="password changed successfully")
            return dict(message="incorrect reset password")
                
        data = request.get_json()
        if not data:
            return dict(message="Fields cannot be empty")

        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        my_list = [old_password, new_password, confirm_password]
        for i in my_list:
            if i is None:
                return dict(message="enter valid data")
            i = i.strip()
            if not i:
                return dict(message="enter valid data")
        if new_password != confirm_password:
            return dict(message="passwords don't match")

        user_identity = get_jwt_identity()
        user = UserModel.query.filter_by(username=user_identity).first()
        if check_password_hash(user.password, old_password) is True:
            user.password = generate_password_hash(new_password)
            user.save()
            return dict(message="password changed successfully")
        return dict(message="Incorrect password")


class BorrowAndReturnBook(Resource):
    @jwt_required
    def post(self, book_id):
        '''Borrow a book'''
        book = BookModel.query.filter_by(book_id=book_id).first()
        if book is None:
             return dict(message="book doesn't exist")
        if book.status == "available":
            book.copies -= 1
            if book.copies == 0:
                book.status = "unavailable"

            book.save()
            return dict(message="book successfully checked out")   
        return dict(message="book is currently unavailable")
   
    @jwt_required
    def put(self, book_id):
        '''Return a book'''
        book = BookModel.query.filter_by(book_id=book_id).first()
        if book is None:
            return dict(message="book {} you are trying to access doesn't exist".format(book_id))
        book.copies += 1
        if book.status == "unavailable":
            book.status = "available"
        book.save()
        return dict(message="book {} successfully returned".format(book_id))

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
    '''retrieve all books'''
    def get(self):
        '''method ['GET']'''
        all_books={}
        result =BookModel.query.all()
        for book in result:
            all_books[book.book_id]={"title":book.title, "author":book.author,
                                          "edition":book.edition, "copies":book.copies, "status":book.status}
            
        return all_books, 200
    @jwt_required
    def post(self):
        '''Only admin can add a book'''
        claims = get_jwt_claims()
        user = get_jwt_identity()
        
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
    def get(self, book_id):
        '''retrieve a single book'''
        book = BookModel.query.filter_by(book_id=book_id).first()
        if book is None:
            return {"message": "Book doesn't exist"}
        return {book.book_id: {"title": book.title, "author": book.author,
                "edition": book.edition, "copies": book.copies, "status": book.status}}
    @jwt_required
    def put(self, book_id):
        '''Only admin can edit a book'''
        claims = get_jwt_claims()
        if claims["admin"] is True:
            data = request.get_json()
            if not data:
                return {"message": "Enter valid data for edit"}
            title = data.get("title")
            author = data.get("author")
            edition = data.get("edition")
            copies = data.get("copies")
            status = data.get("status")

            book = BookModel.query.filter_by(book_id=book_id).first()
            if book is None:
                return dict(message="book doesn't exist")
            if not title and not author and not edition and not copies and not status:
                return dict(message="all fields cannot be empty enter data to edit")
            if not title:
                title = book.title
            if not author:
                author = book.author
            if not edition:
                edition = book.edition
            if not copies:
                copies = book.copies
            if not status:
                status = book.status

            my_list = [title, edition, author, status]
            for i in my_list:
                i = i.strip()
                if i is None or not i:
                    return dict(message="Enter vaild data")

            if not isinstance(copies, int):
                return {"message": "Field copies has to be an integer"}, 200
            if copies < 0:
                return {"message": "Copies entered cannot be a negative number"}, 200
            status = status.encode('ascii')
            if status == "available" or status == "unavailable":
                book.title = title
                book.author = author
                book.edition = edition
                book.copies = copies
                book.status = status
                book.save()
                return dict(message="Book {} successfully edited".format(book_id))

            return dict(message="status has to be either available or unavailble", status=title)
        return {"message": "Admin privilege required"} 
    @jwt_required
    def delete(self, book_id):
        '''Only admin can delete a book'''
        claims = get_jwt_claims()
        if claims["admin"] is True:
            book = BookModel.query.filter_by(book_id=book_id).first()
            if book is None:
                return {"message": "book {} doesn't exist".format(book_id)}
            book.delete()
            return {"message": "book {} deleted successfully".format(book_id)}

        return {"message": "Admin privilege required"}

