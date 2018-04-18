'''application/__init__.py'''
from models import BookModel, UserModel, RevokedTokenModel, UserBooksModel
from views import (Books, BooksBookId, Registration, RemoveUser, Login, Logout, ResetPassword,
                   ChangePassword, BorrowAndReturnBook, UserHistory)
from app import create_app, db
