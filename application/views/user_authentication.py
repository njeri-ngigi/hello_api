'''views/user_authentication.py'''
import random
import string
from datetime import datetime
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_restful import Resource
from flask_jwt_extended import (create_access_token, jwt_required,
                                get_raw_jwt, get_jwt_claims, get_jwt_identity)
from application import UserModel, RevokedTokenModel
from validate import Validate

class Login(Resource):
    '''login user by verifying password and creating an access token'''

    def post(self):
        '''method ['POST']'''
        data = request.get_json()
        if not data:
            return {"message": "Fields cannot be empty"}, 400
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"message": "Username or password missing"}, 400

        user_object = UserModel.get_user_by_username(username)
        if user_object is None:
            return {"message": "Incorrect username"}, 401

        if check_password_hash(user_object.password, password) is True:
            access_token = create_access_token(identity=user_object)
            user_object.last_login = datetime.now()
            user_object.save()
            return dict(message="Login successful", token=access_token), 200

        return {"message": "Incorrect password"}, 401

class Logout(Resource):
    '''class representing logout endpoint'''
    @jwt_required
    def post(self):
        '''logout user by revoking token'''
        json_token_identifier = get_raw_jwt()['jti']

        revoked_token = RevokedTokenModel(
            json_token_identifier=json_token_identifier)
        revoked_token.save()
        return {"message": "Successfully logged out"}, 200

class ResetPassword(Resource):
    '''class representing reset password endpoint'''
    def post(self):
        '''Reset a password'''
        data = request.get_json()
        if not data:
            return {"message": "Enter username"}, 400
        username = data.get('username')
        if not username:
            return {"message": "Enter username"}, 400
        user = UserModel.get_user_by_username(username)
        if user is not None:
            generated_password = ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(7))

            user.reset_password = generate_password_hash(generated_password)
            user.save()
            reset_token = create_access_token(identity=user)
            return dict(reset_token=reset_token, reset_password=generated_password), 200

        return {"message": "User doesn't exist"}, 404

def change_reset_password(reset, data):
    '''helper method for change password through reset token'''
    if not data:
        return dict(message="Fields can't be empty"), 400
    reset_password = data.get("reset_password")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    if reset_password is None or new_password is None:
        return dict(message="reset password or new password fields missing"), 400

    password = Validate().validate_password(new_password, confirm_password)
    if "message" in password:
        return password, 400

    user_identity = get_jwt_identity()
    user = UserModel.get_user_by_username(user_identity)
    if check_password_hash(reset, reset_password) is True:
        user.password = generate_password_hash(new_password)
        user.reset_password = False
        user.last_reset_password = datetime.now()
        user.save()

        #revoke reset token after successfully changing password
        json_token_identifier = get_raw_jwt()['jti']
        revoked_token = RevokedTokenModel(json_token_identifier=json_token_identifier)
        revoked_token.save()
        return dict(message="password changed successfully"), 200

    return dict(message="incorrect reset password"), 401
    
class ChangePassword(Resource):
    '''class representing change password endpoint'''
    @jwt_required
    def put(self):
        '''Change a password'''
        data = request.get_json()

        claims = get_jwt_claims()
        reset = claims["reset_password"].encode('ascii')
        if reset != "false":
            '''if reset password is not false call change_reset_password() helper method'''
            return change_reset_password(reset, data)
        
        if not data:
            return dict(message="Fields cannot be empty"), 400

        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if old_password is None or new_password is None:
            return dict(message="old_password or new_password fields missing"), 400
        my_list = [old_password, new_password, confirm_password]
        for i in my_list:
            i = i.strip()
            if not i:
                return dict(message="enter valid data"), 400
        password = Validate().validate_password(new_password, confirm_password)
        if "message" in password:
            return password

        user_identity = get_jwt_identity()
        user = UserModel.get_user_by_username(user_identity)
        if check_password_hash(user.password, old_password) is True:
            user.password = generate_password_hash(new_password)
            user.last_change_password = datetime.now()
            user.save()

            return dict(message="password changed successfully"), 200
        return dict(message="Incorrect password"), 401
