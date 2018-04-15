'''models/user_books_model.py'''
from datetime import date
from application.app import db

class UserBooksModel(db.Model):
    '''class representing users table'''
    __tablename__ = 'user_books'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('users.username'), nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    date_borrowed = db.Column(db.DateTime)
    date_returned = db.Column(db.DateTime)
    return_status = db.Column(db.Boolean)

    def __init__(self, username, book_id):
        self.username = username
        self.book_id = book_id

    @classmethod
    def date_format(cls, my_date):
        '''method to return date format dd-mm-yyyy'''
        return str(my_date.day) + '-' + str(my_date.month) + '-' + str(my_date.year)

    @classmethod
    def find_user_book(cls, username, book_id):
        '''filter by username and book'''
        #book = cls.query.filter_by(username=username, book_id=book_id).first()
        book = cls.query.filter_by(username=username, book_id=book_id, return_status=False).first()
        return book

    def borrow_book(self):
        '''borrow a book'''
        self.return_status = False
        self.date_borrowed = date.today()

    @classmethod
    def user_history(cls, username):
        '''return user book history'''
        all_user_books = cls.query.filter_by(username=username).all()
        history = []        
        for book in all_user_books:
            date_returned = book.date_returned
            if date_returned is not None:
                date_returned = cls.date_format(date_returned)
            if date_returned is None:
                date_returned = "None"
            date_borrowed = cls.date_format(book.date_borrowed)

            details = dict(book_id=book.book_id, date_borrowed=date_borrowed,
                           date_returned=date_returned, returned=book.return_status)
            history.append(details)
        return history
    
    @classmethod
    def books_not_returned(cls, username):
        '''return all user books not returned'''
        unreturned_books = cls.query.filter_by(username=username).all()
        unreturned_list = []
        for book in unreturned_books:
            if book.return_status is False:
                date_borrowed = cls.date_format(book.date_borrowed)
                details = dict(book_id=book.book_id, date_borrowed=date_borrowed, date_returned="None", returned=book.return_status)
                unreturned_list.append(details)
        return {username: unreturned_list}

    def save(self):
        '''commit and save data from object'''
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<name: %s, username: %s, email: %s>' % (self.name, self.username, self.email)
