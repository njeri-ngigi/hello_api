'''views/user_registration.py'''
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required,  get_jwt_identity, get_raw_jwt
from application import UserModel, UserBooksModel, RevokedTokenModel
from validate import Validate

class Registration(Resource):
    '''Register a user'''

    def post(self):
        '''method ['POST']'''
        data = request.get_json()
        if not data:
            return {"message": "Fields cannot be empty"}, 400
        username = data.get('username')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if not username or not name or not email or not password or not confirm_password:
            return dict(message=
                        "name, username, email, password or confirm_password fields missing"), 400
        v = Validate().validate_register(username, name, email, password, confirm_password)
        if "message" in v:
            return v, 400

        admin = data.get('admin')

        if UserModel.get_user_by_username(v["username"]):
            return {"message": "Add user failed. Username already exists"}, 409
        if UserModel.get_user_by_email(v["email"]):
            return {"message": "Add user failed. Email entered already exists"}, 409
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

        return {"message": "Admin has to be True or left empty"}, 400

class RemoveUser(Resource):
    '''class representing deleting a user account'''
    @jwt_required
    def delete(self):
        '''method to delete a user account'''
        identity = get_jwt_identity()
        my_user = UserModel.get_user_by_username(identity)
        books_not_returned = UserBooksModel.books_not_returned(identity)
        if len(books_not_returned[identity]) == 0:
            my_user.delete()
            #revoke user token after successfully deleting user account
            json_token_identifier = get_raw_jwt()['jti']
            revoked_token = RevokedTokenModel(json_token_identifier=json_token_identifier)
            revoked_token.save()
            return dict(message="user account successfully deleted"), 200
        return dict(message="Return all books to delete user account"), 403
