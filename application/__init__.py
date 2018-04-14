'''application/__init__.py'''
from models import BookModel, UserModel, RevokedTokenModel
from views import (Books, BooksBookId, Registration, Login, Logout, ResetPassword,
                   ChangePassword, BorrowAndReturnBook, BooksNotReturned, UserHistory)

from app import create_app, db

