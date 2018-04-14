'''views/user_books.py'''
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required, jwt_refresh_token_required)
from application import BookModel

class BorrowAndReturnBook(Resource):
    '''class representing borrow and return books endpoint'''
    @jwt_required
    def post(self, book_id):
        '''Borrow a book'''
        book = BookModel.get_book_by_id(book_id)
        if book is None:
            return dict(message="book doesn't exist"), 404
        if book.status == "available":
            book.copies -= 1
            if book.copies == 0:
                book.status = "unavailable"

            book.save()
            return dict(message="book successfully checked out"), 200
        return dict(message="book is currently unavailable"), 403

    @jwt_required
    def put(self, book_id):
        '''Return a book'''
        book = BookModel.get_book_by_id(book_id)
        if book is None:
            return dict(message="book {} you are trying to access doesn't exist".format(book_id)), 404
        book.copies += 1
        if book.status == "unavailable":
            book.status = "available"
        book.save()
        return dict(message="book {} successfully returned".format(book_id)), 200


class UserHistory(Resource):
    '''class representing user history endpoint'''
    @jwt_required
    def get(self):
        '''User's book history'''
        pass


class BooksNotReturned(Resource):
    '''class representing books not returned endpoint'''
    @jwt_required
    def get(self):
        '''Books not yet returned'''
        pass
