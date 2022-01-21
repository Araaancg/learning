def get_all(con, table):
    result = {"data":[]}
    cur = con().cursor()
    query = f"SELECT * FROM {table};"
    print(query)
    fields = tuple(field[1] for field in cur.execute(f"PRAGMA table_info ({table});"))
    for element in cur.execute(query):
        result["data"].append(dict(zip(fields, element)))
    return result

def create_id(con,table):
    cur = con().cursor()
    fields = tuple(field[1] for field in cur.execute(f"PRAGMA table_info ({table});"))
    for field in fields:
        if field.find("id") >= 0:
            gen = tuple(next(cur.execute(f"SELECT MAX({field}) FROM {table}"),False))
            next_id = gen[0][0:3] + str(int(gen[0][3:]) +1).zfill(3)
    return next_id


def insert_new_row(con,request,table):
    cur = con().cursor()
    query = f"INSERT INTO {table} VALUES ("
    fields = tuple(field[1] for field in cur.execute(f"PRAGMA table_info ({table});"))
    values = []
    count=0
    while len(values) < len(fields)-1:
        for k,v in request.form.items():
            for field in fields:

                if k == field:
                    values.append(v)

                while count < 1:
                    if field.find("id") >= 0:
                        id = create_id(con,table)
                        values.append(id)
                        count += 1

    for value in values:
        query += f"'{value}',"
    query = query[0:-1] + ");" 
    print(query)
    cur.execute(query)
    con().commit()
    return True
    
    

