'''views/user_authentication.py'''
import random
import string
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_raw_jwt, get_jwt_claims, get_jwt_identity)
from application import UserModel, RevokedTokenModel

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

        revoked_token = RevokedTokenModel(
            json_token_identifier=json_token_identifier)
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
            return {"message": "Enter username"}, 400
        username = data.get('username')
        user = UserModel.query.filter_by(username=username).first()
        if user is not None:
            generated_password = ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(7))

            user.reset_password = generate_password_hash(generated_password)
            user.save()
            reset_token = create_access_token(identity=user)
            return dict(reset_token=reset_token, reset_password=generated_password), 200

        return {"message": "User doesn't exist"}, 404


class ChangePassword(Resource):
    @jwt_required
    def put(self):
        '''Change a password'''
        claims = get_jwt_claims()
        reset = claims["reset_password"].encode('ascii')
        if reset != "false":
            data = request.get_json()
            if not data:
                return dict(message="Fields can't be empty"), 400
            reset_password = data.get("reset_password")
            new_password = data.get("new_password")
            confirm_password = data.get("confirm_password")

            if reset_password is None or new_password is None:
                return dict(message="reset password or new password fields missing"), 400

            if new_password != confirm_password:
                return dict(message="passwords don't match"), 400

            user_identity = get_jwt_identity()
            user = UserModel.query.filter_by(username=user_identity).first()
            if check_password_hash(reset, reset_password) is True:
                user.password = generate_password_hash(new_password)
                user.reset_password = False
                user.save()
                
                json_token_identifier = get_raw_jwt()['jti']
                revoked_token = RevokedTokenModel(json_token_identifier=json_token_identifier)
                revoked_token.save()
                return dict(message="password changed successfully"), 200

            return dict(message="incorrect reset password"), 401

        data = request.get_json()
        if not data:
            return dict(message="Fields cannot be empty"), 400

        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        my_list = [old_password, new_password, confirm_password]
        for i in my_list:
            if i is None:
                return dict(message="enter valid data"), 400
            i = i.strip()
            if not i:
                return dict(message="enter valid data"), 400
        if new_password != confirm_password:
            return dict(message="passwords don't match"), 400

        user_identity = get_jwt_identity()
        user = UserModel.query.filter_by(username=user_identity).first()
        if check_password_hash(user.password, old_password) is True:
            user.password = generate_password_hash(new_password)
            user.save()

            return dict(message="password changed successfully"), 200

        
        return dict(message="Incorrect password"), 401