'''models/book_model.py'''
from application.app import db

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

    @classmethod
    def get_book_by_id(cls, book_id):
        '''retrieve single book by id''' 
        return db.session.query.filter_by(book_id=book_id).first()

    @classmethod
    def get_book_by_title(cls, title):
        '''retrieve single book by title'''
        return db.session.query.filter_by(title=title).first()
    
    @classmethod
    def get_all_books(cls):
        '''retrieve all books'''
        all_books = {}
        result = db.session.query.all()
        for book in result:
            all_books[book.book_id] = {"title": book.title, "author": book.author,
                                       "edition": book.edition, "copies": book.copies, "status": book.status}

        return all_books

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
