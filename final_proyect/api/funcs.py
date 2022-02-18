import json
import sqlite3

DB = "./vocab.db"

con = sqlite3.connect(DB, check_same_thread=False)
cur = sqlite3.Cursor(con)


def get_all(con,table):
    result = {"users":[]}
    cur = con().cursor()
    query = f"SELECT * FROM {table};"
    fields = tuple(field[1] for field in cur.execute(f"PRAGMA table_info ({table});"))
    for element in cur.execute(query):
        result["users"].append(dict(zip(fields,element)))
    return json.dumps(result, sort_keys=False)

def json_data(json_file):
    with open(json_file, encoding="utf8") as file:
        return json.load(file)

data = json_data("./test_vocab.json")
print(data)

def insert_test_vocab():
    cur = con.cursor()
    starting_id = 21
    for k,v in data["test_vocab_2"].items():
        query = f"INSERT INTO p0002a VALUES ('w{str(starting_id).zfill(4)}a','{k}','{v}');"
        cur.execute(query)
        con.commit()
        starting_id += 1

insert_test_vocab()