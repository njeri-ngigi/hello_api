'''application/__init__.py'''
from views import (Books, BooksBookId, Registration, RemoveUser, Login, Logout, ResetPassword,
                   ChangePassword, BorrowAndReturnBook, UserHistory)
from models import BookModel, UserModel, RevokedTokenModel, UserBooksModel
from app import create_app, db
