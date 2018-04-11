'''models.py'''
from werkzeug.security import generate_password_hash
from app import db

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

    def get_single_book(self, book_id):
        '''retrieve single book by id'''

    def get_all_books(self, book_id):
        '''retrieve all books'''
        pass

    def edit_book(self, book_id):
        '''edit book by id'''
        pass 

    def delete(self):
        '''delete a book by id'''
        db.session.delete(self)
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

# class UserBooksModel(db.Model):
#     '''class representing a user's books'''
#     __tablename__ = 'user_books'
#     book_id = db.Column(db.Integer, foreign_key=True)
#     username = db.Column(db.String, foreign_key=True)
#     date_borrowed = db.Column(db.Datetime)
#     date_returned = db.Column(db.Datetime)
#     returned = db.Column(db.Boolean)

#     def borrow_book(self):
#         '''borrow a book'''
#         pass

#     def return_book(self):
#         '''return a book'''
#         pass 

#     def user_history(self):
#         '''return user history (entire table)'''
#         pass 

#     def books_not_returned(self):
#         '''return books not yet returned'''
#         pass 

class RevokedTokenModel(db.Model):
    '''class representing rovoked tokens table'''
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    json_token_identifier = db.Column(db.String(120))

    def save(self):
        '''commit and save data from object'''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, json_token_identifier):
        query = cls.query.filter_by(
        json_token_identifier=json_token_identifier).first()
        return bool(query)

