'''app.py'''
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import ast
from config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from models import Books
    app = Flask(__name__)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/api/v1/books', methods=['POST', 'GET'])
    def books():
        '''Add and retrieve all books'''
        if request.method == 'POST':
            #add a book method="POST"
            all_books = Books.query.all()

            data = request.get_json()
            if not data:
                return jsonify({"message": "Fields cannot be empty"})
            

            title = data.get('title')
            author = data.get('author')
            edition = data.get('edition')
            book_id = data.get('book_id')            
            copies = data.get('copies')
            

            '''if (isinstance(book_id, int) and isinstance(copies, int)) != True:
                return jsonify({"message":"Field Book_id and copies has to be an integer"})'''
            if copies < 0:
                return jsonify({"message":"Copies entered cannot be a negative number"})
            if copies == 0:
                status = "unavailable"
            status = "available"
            
            my_book = Books(author=author, title=title, edition=edition, copies=copies, status=status)
            if my_book.title in [book.title for book in all_books]:
                return jsonify({"message":"fail"})
            my_book.save()
            response = jsonify({"message": "pass"})
            response.status_code = 201

            return response

        '''#method ['GET']
        response = jsonify(my_book.get_all())
        response.status_code = 200'''


    return app


'''#method to run app.py
if __name__ == '__main__':
    app.run(debug=True)'''
    
