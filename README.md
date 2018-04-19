# Hello Books API with PostgreSQL
Hello books API is a RESTful Flask application for a simple application that helps manage a library and its processes like stocking, tracking and renting books. Books can be added, deleted, retrieved and edited through endpoints. A user can login in, logout, reset password and borrow a book through the endpoints too. 
###### Travis CI [![Build Status](https://travis-ci.org/njeri-ngigi/hello_api.svg?branch=unittests)](https://travis-ci.org/njeri-ngigi/hello_api) Coveralls [![Coverage Status](https://coveralls.io/repos/github/njeri-ngigi/hello_api/badge.svg?branch=master)](https://coveralls.io/github/njeri-ngigi/hello_api?branch=master) Codeclimate [![Maintainability](https://api.codeclimate.com/v1/badges/134755222a765551cf15/maintainability)](https://codeclimate.com/github/njeri-ngigi/hello_api/maintainability)

#### Endpoints implemented include:
| http methods |    Endpoint route                  |   Endpoint functionality                                     |
| ------------ | ---------------------------------- | ------------------------------------------------------------ |
| POST         | /api/v1/auth/register              |   Creates a user account                                     |
| POST         | /api/v1/auth/login                 |   Logs in a user                                             |
| POST         | /api/v1/auth/logout                |   Logs out a user                                            |
| POST         | /api/v1/auth/reset-password        |   Password reset                                             |
| POST         | /api/v1/books                      |   add a book                                                 |
| PUT          | /api/v1/books/<bookId>             |   modify a book’s information                                |
| DELETE       | /api//books/<bookId>               |   Remove a book                                              |
| GET          | /api/v1/books                      |   Retrieves all books                                        |
| GET          | /api/v1/books/<bookId>             |   Get a book                                                 |
| POST         | /api/v1/users/books/<bookId>       |   Borrow a book                                              |
| PUT          | /api/v1/users/books/<bookId>       |   Return a book                                              |
| GET          | /api/v1/users/books?returned=false |   Get all books not yet returned                             |
| GET          | /api/v1/users/books                |   Get borrowing history of a user                            |


## Prerequisites
      * pip
      * virtualenv
      * python 3 or python 2.7
      * postgresql
      

## Installation
   clone the repo
   ```
   clone https://github.com/njeri-ngigi/hello-books-api.git
   ```
   create a virtual environment
   ```
   virtualenv <environment name>
   ```
   activate the environment:
   ```
   $source <path to env name>/Scripts/activate (in bash)
   ```
   install dependencies:
   ```
   $pip install -r requirements.txt
   ```
   set up two databases within the postgresql server, one for running tests and the other for the application.
   > PS: update instance/config.py with your database uri 
   ###### Run the app, and your ready to go!
   ```
   python run.py
   ```
      

## Running the tests
  The tests for this API are written using the python module unittests. The tests can be found under the folder tests.
  Python unit test framework nose that extends from unittest is used to run the tests.<br>
  To run the tests use the command:
      
   ```
   nosetests test_models.py
   nosetests test_api.py
  ```
  
  Tests have been set to run automatically and can be run using the command:
  ```
  python manage.py test
  ```
   
### Deployment
###### Application deployed to HEROKU [my-hello-books-api-unit]https://my-hello-books-api-unit.herokuapp.com/

### Documentation
###### [Apiary.io](https://helloword16.docs.apiary.io/#)

## Built with 
   Flask, a python framework
   
## Authors
[Njeri Ngigi](https://github.com/njeri-ngigi)

