import datetime as dt

def get_all(con, table):
    result = {"data":[]}
    cur = con().cursor()
    query = f"SELECT * FROM {table};"
    # print(query)
    fields = tuple(field[1] for field in cur.execute(f"PRAGMA table_info ({table});"))
    for element in cur.execute(query):
        result["data"].append(dict(zip(fields, element)))
    return result

def create_id(con,table):
    cur = con().cursor()
    fields = tuple(field[1] for field in cur.execute(f"PRAGMA table_info ({table});"))
    for field in fields:
        if field == f"id_{table[0:-1]}":
            gen = tuple(next(cur.execute(f"SELECT MAX({field}) FROM {table}"),False))
            next_id = gen[0][0:3] + str(int(gen[0][3:]) +1).zfill(3)
    return next_id


def insert_new_row(con,request,table):
    cur = con().cursor()
    query = f'''INSERT INTO {table} VALUES ('{create_id(con,table)}','{request.form["name"]}','{request.form["email"]}',0);''' if table == "collectors" else f'''INSERT INTO {table} VALUES ('{create_id(con,table)}','{request.form["name"]}','{request.form["email"]}');'''
    cur.execute(query)
    con().commit()
    return True
    
def purchase(con,request,table):
    cur = con().cursor()

    colle = str(next(cur.execute(f'''SELECT id_collector FROM collectors WHERE name='{request.form["collector"]}';'''), False))
    prov = str(next(cur.execute(f'''SELECT id_provider FROM providers WHERE name='{request.form["provider"]}';'''), False))

    date = request.form["date"] if request.form["date"] else dt.datetime.isoformat(dt.datetime.now()).split("T")[0]

    query = f'''INSERT INTO {table} VALUES ('{create_id(con,table)}','{date}',{request.form["price"]},{request.form["quantity"]},'{colle[2:8]}','{prov[2:8]}');'''
    print(query)
    cur.execute(query)
    con().commit()

    query = f'''UPDATE collectors SET quantity=quantity+{request.form["quantity"]} WHERE id_collector='{colle[2:8]}';'''
    cur.execute(query)
    con().commit()

    return True


