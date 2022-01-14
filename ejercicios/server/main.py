from flask import Flask, request
import json
from funcs import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB = get_data()

@app.route("/")
def home():
    return "Your are on the home page"

@app.route("/all")
def all():
    return DB

@app.route("/book/<book_id>", methods=["GET","PUT","DELETE"])
def book_by_id(book_id):
    if request.method == "GET":
        book_found = get_by_id(book_id)
        if book_found:
            return {"success":True,"book":book_found}
        else:
            return {"success":False}

    if request.method == "DELETE":
        if delete_by_id(book_id):
            return {"success":True}
        else:
            return {"success":False}

    if request.method == "PUT":
        book_to_update = update_book(book_id,request)
        if book_to_update:
            return {"success":True,"book":book_to_update[1]}
        else:
            return {"success":False}

if __name__ == "__main__":
    app.run(debug=True)