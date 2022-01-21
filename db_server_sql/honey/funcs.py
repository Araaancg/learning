def get_all(con, table):
    result = {"data":[]}
    cur = con().cursor()
    query = f"SELECT * FROM {table};"
    print(query)
    fields = tuple(field[1] for field in cur.execute(f"PRAGMA table_info ({table});"))
    for element in cur.execute(query):
        result["data"].append(dict(zip(fields, element)))
    return result

def insert_new_row(con,request,table):
    cur = con().cursor()
    query = f"INSERT INTO {table} VALUES ("
    fields = tuple(field[1] for field in cur.execute(f"PRAGMA table_info ({table});"))
    print(fields)
    values = []
    while len(values) < len(fields):
        for k,v in request.form.items():
            for field in fields:
                if k == field:
                    values.append(v)
    for value in values:
        query += f"'{value}',"
    query = query[0:-1] + ");" 
    print(query)
    cur.execute(query)
    con().commit()
    return True
    
    

