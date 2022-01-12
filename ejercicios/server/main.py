from flask import Flask
import json

def get_data(json_file):
    with open(json_file, encoding="utf8") as file:
        return json.load(file)

def write_data(data):
    with open("bookshop.json", encoding="utf8", mode="w") as file:
        json.dump(data,file,ensure_ascii=False,indent=4)

def get_by_id(book_id):
    return next(filter(lambda book: book["id"] == book_id, get_data("bookshop.json")["data"]), False)

def delete_by_id(book_id):
    book_dicc = get_data("bookshop.json")
    book_to_delete = get_by_id(book_id)
    book_dicc["data"].remove(book_to_delete)
    return book_dicc

app = Flask(__name__)



@app.route("/all")
def all():
    return get_data("bookshop.json")

@app.route("/book/<book_id>")
def book_by_id(book_id):
    book_found = get_by_id(book_id)
    if book_found:
        return {"success":True,"book":book_found}
    else:
        return {"success":False}

@app.route("/delete_book/<book_id>")
def delete(book_id):
    book = delete_by_id(book_id)
    if book:
        write_data(book)
        return {"success":True}
    else:
        return {"success":False}