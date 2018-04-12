'''views/user_registration.py'''
from flask import request
from flask_restful import Resource
from application import UserModel
from validate import Validate

class Registration(Resource):
    '''Register a user'''

    def post(self):
        '''method ['POST']'''
        data = request.get_json()
        if not data:
            return {"message": "Fields cannot be empty"}, 400
        v = Validate().validate_register(data)

        if "message" in v:
            return v, 400

        admin = data.get('admin')

        if UserModel.query.filter_by(username=v["username"]).first():
            return {"message": "Add user failed. Username already exists"}, 409
        if UserModel.query.filter_by(email=v["email"]).first():
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
