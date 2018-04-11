'''app.py'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import app_config

db = SQLAlchemy()


def create_app(config_name):
    '''function enclosing FlaskAPP'''
    import resources
    from models import RevokedTokenModel

    app = Flask(__name__)
    api = Api(app)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'my-key'
    db.init_app(app)

    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access' '''refresh''']
    jwt = JWTManager(app)
    blacklist = set()

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
        return RevokedTokenModel.is_jti_blacklisted(json_token_identifier) 
    

    api.add_resource(resources.Registration, '/api/v1/auth/register')
    api.add_resource(resources.Login, '/api/v1/auth/login')
    api.add_resource(resources.Logout, '/api/v1/auth/logout')
    api.add_resource(resources.ResetPassword, '/api/v1/auth/reset-password')
    api.add_resource(resources.ChangePassword, '/api/v1/auth/change-password')
    api.add_resource(resources.BorrowAndReturnBook, '/api/v1/users/books/<int:book_id>')
    api.add_resource(resources.UserHistory, '/api/v1/users/books')
    #api.add_resource(resources.BooksNotReturned, '/api/v1/')
    api.add_resource(resources.Books, '/api/v1/books')
    api.add_resource(resources.BooksBookId, '/api/v1/books/<int:book_id>')


    return app    
