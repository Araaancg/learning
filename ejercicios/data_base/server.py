import sqlite3
from flask import Flask,request,g
# from main import *
from funcs import *

app = Flask(__name__)

DB = "./bookshop.db"

def con():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
    return db

# cur = con().cursor()

def db_to_dicc(cur,**kwargs):
    result = {"books":[]}
    fields = tuple([field[1] for field in cur.execute('''PRAGMA table_info(books);''')])
    
    sql_string = f'''SELECT * FROM books ORDER BY {kwargs.get('sort')};''' if kwargs.get('sort') else '''SELECT * FROM books;'''
    
    for book in cur.execute(sql_string):
        result["books"].append(dict(zip(fields,book)))
    return result


@app.route("/db_all", methods=["GET"])
def get_all():
    cur = con().cursor()
    params = request.args.to_dict()
    print(params)
    if params:
        return db_to_dicc(cur,sort=params["sort"])
    return db_to_dicc(cur)

if __name__ == "__main__":
    app.run(debug=True)