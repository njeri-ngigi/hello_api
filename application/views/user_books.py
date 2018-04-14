'''views/user_books.py'''
from datetime import date
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required, jwt_refresh_token_required, get_jwt_identity)
from application import BookModel, UserBooksModel

class BorrowAndReturnBook(Resource):
    '''class representing borrow and return books endpoint'''
    @jwt_required
    def post(self, book_id):
        '''Borrow a book'''
        identity = get_jwt_identity()
        book = BookModel.get_book_by_id(book_id)
        if book is None:
            return dict(message="book doesn't exist"), 404
        user_book = UserBooksModel(identity, book_id)
        found_book = user_book.find_user_book(identity, book_id)
        if found_book is not None:
            return dict(message="You can't borrow the same book twice"), 409
        if book.status == "available":
            book.copies -= 1
            if book.copies == 0:
                book.status = "unavailable"
            book.save()
            user_book.borrow_book()
            user_book.save()
            
            return dict(message="book successfully checked out"), 200
        
        return dict(message="book is currently unavailable"), 403

    @jwt_required
    def put(self, book_id):
        '''Return a book'''
        identity = get_jwt_identity()
        book = BookModel.get_book_by_id(book_id)
        if book is None:
            return dict(message="book {} you are trying to access doesn't exist".format(book_id)), 404
        find_book = UserBooksModel.find_user_book(identity, book_id)
        if find_book is None:
            return dict(message="You haven't borrowed this book"), 403
        book.copies += 1
        if book.status == "unavailable":
            book.status = "available"
        book.save()
        find_book.return_status = True
        find_book.date_returned = date.today()
        find_book.save()
        return dict(message="book {} successfully returned".format(book_id)), 200


class UserHistory(Resource):
    '''class representing user history endpoint'''
    @jwt_required
    def get(self):
        '''User's book history'''
        identity = get_jwt_identity()
        if request.args.get('returned') == 'false':
            '''Books not yet returned'''
            unreturned_books = UserBooksModel.books_not_returned(identity)
            return unreturned_books, 200

        all_user_books = UserBooksModel.user_history(identity)
        history = []
        for book in all_user_books:
            my_date = book.date_returned
            if my_date is not None:
                my_date = str(my_date.day) + '-' + str(my_date.month) + '-' + str(my_date.year)
            if my_date is None:
                my_date = "None"
            date_borrowed = str(book.date_borrowed.day) + '-' + str(book.date_borrowed.month) + '-' + str(book.date_borrowed.year)

            details = dict(book_id=book.book_id, date_borrowed=date_borrowed, date_returned=my_date, returned=book.return_status)
            history.append(details)
        return {identity:history}, 200
        
