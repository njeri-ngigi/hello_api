'''models/user_model.py'''
from werkzeug.security import generate_password_hash
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

    def __init__(self, username, name, email, password, admin=False):
        self.username = username
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.admin = admin
        self.reset_password = False

    # def password_reset(self, reset_password):
    #     '''reset password'''
    #     self.reset_password = generate_password_hash(reset_password)
    #     pass

    def change_password(self, old_password):
        '''change password'''
        pass

    def save(self):
        '''commit and save data from object'''
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<name: %s, username: %s, email: %s>' % (self.name,
                                                        self.username, self.email)
