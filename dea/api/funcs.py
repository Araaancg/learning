import json

def get_all(con,table):
    result = {"users":[]}
    cur = con().cursor()
    query = f"SELECT * FROM {table};"
    fields = tuple(field[1] for field in cur.execute(f"PRAGMA table_info ({table});"))
    for element in cur.execute(query):
        result["users"].append(dict(zip(fields,element)))
    return json.dumps(result, sort_keys=False)

def create_id(cur):
    gen = tuple(next(cur.execute(f"SELECT MAX(id) FROM users;"),False))
    print(gen)
    next_id = str(int(gen[0]) + 1)
    return next_id