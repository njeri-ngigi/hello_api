'''models.py'''
from app import db

class Books(db.Model):
    '''Class representing books table'''
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255))
    title = db.Column(db.String(255))
    edition = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, book_id):
        self.book_id = book_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(self):
        return books.query.all()
    
    def get_single_book(self):
        return books.query

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Book: {}>".format(self.book_id)