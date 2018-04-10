'''models.py'''
from db import db

class BookModel(db.Model):
    '''class representing books table'''
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(70))
    title = db.Column(db.String(70), unique=True)
    edition = db.Column(db.String(10))
    status = db.Column(db.String(20))
    copies = db.Column(db.Integer)

    def __init__(self, author, title, edition, copies, status):
        self.author = author
        self.title = title
        self.edition = edition
        self.copies = copies
        self.status = status

    def save(self):
        '''commit and save data from object'''
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<title: %s, author: %s, edition: %s, copies: %s, status: %s>' % (self.title,
                self.author, self.edition, self.copies, self.status)

class UserModel(db.Model):
    '''class representing users table'''
    __tablename__ = 'users'

    username = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(200))
    admin = db.Column(db.Boolean)

    def __init__(self, username, name, email, password, admin=False):
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.admin = admin

    def save(self):
        '''commit and save data from object'''
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<name: %s, username: %s, email: %s>' % (self.name,
                self.username, self.email)
