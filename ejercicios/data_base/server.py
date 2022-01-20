import sqlite3
from flask import Flask,request,g

app = Flask(__name__)

DB = "./bookshop.db"

def con():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
    return db

# cur = con().cursor()

@app.route("/db_all", methods=["GET"])
def get_all():
    cur = con().cursor()
    result = {"books":[]}
    params = request.args.to_dict() 
    sql_string = f'''SELECT * FROM books ORDER BY {params["sort"]}''' if params else '''SELECT * FROM books'''
    fields = tuple([field[1] for field in cur.execute('''PRAGMA table_info(books);''')])
    for book in cur.execute(sql_string):
        result["books"].append(dict(zip(fields,book)))
    return result


@app.route("/db_book/<book_id>",methods=["GET","DELETE","PUT"])
def search_book(book_id):
    cur = con().cursor()
    result = {"books":[]}
    if request.method == "GET":
        # print(result)

        sql_string = f'''SELECT * FROM books WHERE id="{book_id}";'''
        fields = tuple([field[1] for field in cur.execute('''PRAGMA table_info(books);''')])

        for book in cur.execute(sql_string):
            result["books"].append(dict(zip(fields,book)))
        if result["books"]:
            return result
        else:
            return "Book not found"
    
    if request.method == "DELETE":
        sql_string = f'''DELETE FROM books WHERE id="{book_id}";'''
        cur.execute(sql_string)
        con().commit()
        return {"success":True}
    
    if request.method == "PUT":
        info = request.form
        # print(info)
        set_info = f""
        for k,v in info.items():
            set_info += f"'{k}' = '{v}',"
        
        set_info = set_info[0:-1]
        sql_string = f'''UPDATE books SET {set_info} WHERE id='{book_id}';'''
        # print(sql_string)

        cur.execute(sql_string)
        con().commit()
        
        fields = tuple([field[1] for field in cur.execute('''PRAGMA table_info(books);''')])

        for book in cur.execute(f"SELECT * FROM books WHERE id='{book_id}';"):
            result["books"].append(dict(zip(fields,book)))
        if result["books"]:
            return result
        return {"success":False}
    
    if request.method == "POST":
        pass



if __name__ == "__main__":
    app.run(debug=True)