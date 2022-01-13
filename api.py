import os
import flask
from flask import json, request
from flask_cors import CORS
from middleware import Middleware

app = flask.Flask(__name__)
app.config["DEBUG"] = True

CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

user = os.environ.get('DATABASE_USER')
password = os.environ.get('DATABASE_PASSWORD')
database = os.environ.get('DATABASE_NAME')

middleware = Middleware(user, password, database)
middleware.populate_library()

@app.route('/', methods=['GET'])
def list_books():
    data = middleware.list_books()
    response = app.response_class(
        response = json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/increment/<BookID>', methods= ["GET"])
def incrementBook(BookID):
    middleware.increment_book(1, BookID)
    data = middleware.list_books()
    response = app.response_class(
        response = json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/decrement/<BookID>', methods= ["GET"])
def decrementBook(BookID):
    middleware.delete_book(1, BookID)
    data = middleware.list_books()
    response = app.response_class(
        response = json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/search/<bookName>', methods= ["GET"])
def searchBook(bookName):
    data = middleware.search_book("title", bookName)
    response = app.response_class(
        response = json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/add/', methods= ["POST"])
def addBook():
    body = request.get_json()
    available = int(body['available'])
    title = body['title']
    author = body['author']
    category = body['category']
    price = float(body['price'])
    url = body['url']

    middleware.add_book(available, title, author, category, price, url)

    data = middleware.list_books()
    response = app.response_class(
        response = json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


app.run()

