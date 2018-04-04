# Hello Books API with PostgreSQL
Hello books API is a RESTful Flask application for a simple application that helps manage a library and its processes like stocking, tracking and renting books. Books can be added, deleted, retrieved and edited through endpoints. A user can login in, logout, reset password and borrow a book through the endpoints too. 
###### Travis CI, Coveralls, Codeclimate

## Prerequisites
      pip
      virtualenv
      python 3 or python 2.7
      

## Installation
   clone the repo using
   ```
   clone https://github.com/njeri-ngigi/hello-books-api.git
   ```
   create a virtual environment using 
   ```
   virtualenv <environment name>
   ```
   activate the environment using:
   ```
   $source <path to env name>/Scripts/activate (in bash)
   ```
   install dependencies using 
   ```
   $pip install -r requirements.txt
   ```
      

## Running the tests
  The tests for this API are written using the python module unittests. The tests can be found within the folder api under the folder tests.
  Python unit test framework nose that extends from unittest is used to run the tests.<br>
  To run the tests use the command:
      
   ```
   nosetests test_models.py
   nosetests test_api.py
  ```
   
### Deployment
###### Application deployed to HEROKU [Hello-books-api](https://my-hello-books-api.herokuapp.com/)

### Documentation
###### [Apiary.io](https://hellobooksapi3.docs.apiary.io/#)

## Built with 
   Flask, a python framework
   
## Authors
[Njeri Ngigi](https://github.com/njeri-ngigi)

