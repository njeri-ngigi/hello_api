'''app.py'''
#import ast
import re
import ast
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt, get_jwt_claims, get_jwt_identity)
from flask_sqlalchemy import SQLAlchemy
from config import app_config

db = SQLAlchemy()

def create_app(config_name):
    '''function enclosing FlaskAPP'''
    from models import Books, Users
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'my-key'


    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    jwt = JWTManager(app)
    BLACKLIST = set()
    db.init_app(app)

    '''Error handlers'''
    @app.errorhandler(400)
    def bad_request(error):
        '''error handler for Bad request'''
        return jsonify(dict(error = 'Bad request')), 400
    @app.errorhandler(404)
    def page_not_found(error):
        '''error handler for 404'''
        return jsonify(dict(error = 'Page not found')), 404

    @app.errorhandler(405)
    def unauthorized_method(error):
        '''error handler for 405'''
        return jsonify(dict(error = 'Method not allowed')), 405

    @app.errorhandler(500)
    def server_error(error):
        '''error handler for 404'''
        return jsonify(dict(error = 'Internal server error')), 500
    
    @jwt.user_claims_loader
    def add_claims_to_access_token(user_object):
        return {"admin": user_object.admin}

    @jwt.user_identity_loader
    def user_identity_lookup(user_object):
        return user_object.username

    @jwt.token_in_blacklist_loader
    def check_if_token_blacklist(decrypted_token):
        '''check if jti(unique identifier) is in black list'''
        json_token_identifier = decrypted_token['jti']
        return json_token_identifier in BLACKLIST

    @app.route('/api/v1/auth/register', methods=['POST'])
    def register():
        '''endpoint to register a user'''
        all_users = Users.query.all()
        data = request.get_json()
        if not data:
            response = jsonify({"message": "Fields cannot be empty"})
            response.status_code = 206
            return response
        username = data.get('username')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        admin = data.get('admin')

        my_list = [username, name, password]
        for i in my_list:
            i = i.strip()
            if i is None or not i:
                response = jsonify({"message": "Enter valid data"})
                response.status_code = 206
                return response
        if len(password) < 4:
            response = jsonify({"message": "password is too short"})
            response.status_code = 206
            return response
        if confirm_password != password:
            response = jsonify({"message": "Passwords don't match"})
            response.status_code = 206
            return response
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match is None:
            response = jsonify({"message": "Enter a valid email address"})
            response.status_code = 206
            return response
        if not admin:
            my_user = Users(username=username, name=name, email=email, password=password)
            if my_user.username in [user.username for user in all_users]:
                response = jsonify({"message": "Add user failed. Username already exists"})
                response.status_code = 206
                return response
            if my_user.email in [user.email for user in all_users]:
                response = jsonify(
                    {"message": "Add user failed. Email entered already exists"})
                response.status_code = 206
                return response
            my_user.save()
            response = jsonify({"message": "User successfully added"})
            response.status_code = 201
            return response
        if admin == "True" or admin == "true":
            my_user = Users(username=username, name=name, email=email, password=password, admin=True)
            if my_user.username in [user.username for user in all_users]:
                response = jsonify({"message": "Add user failed. Username already exists"})
                response.status_code = 206
                return response
            if my_user.email in [user.email for user in all_users]:
                response = jsonify({"message": "Add user failed. Email entered already exists"})
                response.status_code = 206
                return response
            my_user.save()
            response = jsonify({"message": "Admin user successfully added"})
            response.status_code = 201
            return response
        response = jsonify({"message":"Admin has to be True or empty"})
        response.status_code = 206
        return response

    @app.route('/api/v1/auth/login', methods=['POST'])
    def login():
        '''login user by verifying password and creating an access token'''
        data = request.get_json()
        if not data:
            return jsonify({"message": "Fields cannot be empty"})
        username = data.get('username')
        password = data.get('password')

        user_object = Users.query.filter_by(username=username).first()
        if user_object is None:
            response = jsonify({"message":"Incorrect username"})
            response.status_code = 401
            return response

        if user_object.password == password:
            access_token = create_access_token(identity=user_object)
            return jsonify(dict(token=access_token, message="Login successful")), 200

        response = jsonify({"message": "Incorrect password"})
        response.status_code = 401
        return response        


    @app.route('/api/v1/books', methods=['POST'])
    @jwt_required
    def books():
        '''Only admin can add a book'''
        claims = get_jwt_claims()
        if claims["admin"] == "true":
            all_books = Books.query.all()

            data = request.get_json()
            if not data:
                response = jsonify({"message": "Fields cannot be empty"})
                response.status_code = 206
                return response
            
            title = data.get('title').strip()
            author = data.get('author').strip()
            edition = data.get('edition').strip()
            copies = data.get('copies')
    
            if not isinstance(copies, int):
                response = jsonify({"message":"Field Book_id and copies has to be an integer"})
                response.status_code = 206
                return response
            if copies < 0:
                response = jsonify({"message":"Copies entered cannot be a negative number"})
                response.status_code = 206
                return response
            if copies == 0:
                status = "unavailable"
            status = "available"
            my_list = [title, author, edition]
            for i in my_list:
                if i is None or not i:
                    response = jsonify({"message": "Enter valid data"})
                    response.status_code = 206
                    return response


            my_book = Books(author=author, title=title, edition=edition, copies=copies, status=status)
            if my_book.title in [book.title for book in all_books]:
                response = jsonify({"message":"Add book failed. Book title already exists"})
                response.status_code = 206
                return response
            my_book.save()
            response = jsonify({"message": "Book successfully added"})
            response.status_code = 201

            return response
        return jsonify({"message":"Admin privilege required"})
    return app    
