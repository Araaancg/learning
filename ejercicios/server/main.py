from flask import Flask, request
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

def update_book(book_to_update):
    try:
        book_dicc = get_data("bookshop.json")
        for k,v in request.form.items():
            if k in ["title","author","genre","id"]:
                book_to_update[k] = v
        
        for book,i in enumerate(book_dicc["data"]):
            book_dicc["data"][i] = book_to_update
            write_data(book_dicc)
        return True
    except:
        return False

app = Flask(__name__)



@app.route("/all")
def all():
    return get_data("bookshop.json")

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
        book =  get_by_id(book_id)
        book_to_update = update_book(book)
        if book_to_update:
            return {"success":True,"book":book_to_update}
        else:
            return {"success":False}


        
            