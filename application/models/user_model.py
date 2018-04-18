'''models/user_model.py'''
from datetime import datetime
from werkzeug.security import generate_password_hash
#from sqlalchemy import and_
from application.app import db

class UserModel(db.Model):
    '''class representing users table'''
    __tablename__ = 'users'

    username = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(200))
    admin = db.Column(db.Boolean)
    reset_password = db.Column(db.String(200))
    date_registered = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    last_change_password = db.Column(db.DateTime)
    last_reset_password = db.Column(db.DateTime)
    user_books = db.relationship("UserBooksModel", cascade="all, delete-orphan")
    
    def __init__(self, username, name, email, password, admin=False):
        self.username = username
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.admin = admin
        self.reset_password = False
        self.date_registered = datetime.now()

    @classmethod
    def get_user_by_username(cls, username):
        '''query user table using username'''
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email):
        '''query user table using email'''
        return cls.query.filter_by(email=email).first()

    def save(self):
        '''commit and save data from object'''
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''delete a user account'''
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<name: %s, username: %s, email: %s>' % (self.name,
                                                        self.username, self.email)
