'''app.py'''
from flask import Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt, get_jwt_claims, get_jwt_identity)
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import app_config
import resources
db = SQLAlchemy()

def create_app(config_name):
    '''function enclosing FlaskAPP'''
    app = Flask(__name__)
    api = Api(app)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'my-key'


    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    jwt = JWTManager(app)
    blacklist = set()
    db.init_app(app)

    api.add_resource(resources.Registration, '/api/v1/auth/register')
    api.add_resource(resources.Login, '/api/v1/auth/login')
    api.add_resource(resources.Logout, '/api/v1/auth/logout')
    api.add_resource(resources.ResetPassword, '/api/v1/auth/reset-password')
    api.add_resource(resources.ChangePassword, '/api/v1/auth/change-password')
    api.add_resource(resources.BorrowBook, '/api/v1/users/books/<int:book_id>')
    api.add_resource(resources.UserHistory, '/api/v1/users/books')
    #api.add_resource(resources.BooksNotReturned, '/api/v1/')
    api.add_resource(resources.Books, '/api/v1/books')
    api.add_resource(resources.BooksBookId, '/api/v1/books/<int:book_id>')


    return app    
