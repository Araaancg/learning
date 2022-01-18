import json
import sqlite3

def get_data(json_file):
    with open(json_file,encoding="utf8") as file:
        return json.load(file)

con = sqlite3.connect("./bookshop.db")
cur = sqlite3.Cursor(con)

cur.execute('''CREATE TABLE books (id TEXT PRIMARY KEY, title TEXT, author TEXT, genre TEXT, stock INTEGER);''')

DB = get_data("./bookshop.json")

for book in DB["data"]:
    cur.execute(f'''INSERT INTO books 
    VALUES ("{book["id"]}","{book["title"]}","{book["author"]}","{book["genre"]}",{book["stock"]});
    ''')

# cur.execute('''SELECT * FROM books ORDER BY author DESC;''')

con.commit()