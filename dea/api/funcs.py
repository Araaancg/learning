import json
import requests as req
# import sqlite3
# from flask import g
import utm
from operator import itemgetter

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


#METER DATOS DEA EN LA BASE DE DATOS
def json_data():
    url = "https://datos.comunidad.madrid/catalogo/dataset/35609dd5-9430-4d2e-8198-3eeb277e5282/resource/c38446ec-ace1-4d22-942f-5cc4979d19ed/download/desfibriladores_externos_fuera_ambito_sanitario.json"
    result = req.get(url).json()
    with open("./deas.json", mode="w", encoding="utf8") as file:
        json.dump(result,file, indent=4, ensure_ascii=False)

# # json_data()

# def get_data(json_file):
#     with open(json_file, mode="r") as file:
#         return json.load(file)

# deas_dicc = get_data("./deas.json")
# # print(deas_dicc)

# DB = "./deas.db"

# con = sqlite3.connect(DB, check_same_thread=False)
# cur = sqlite3.Cursor(con)

# def insert_data():
#     for dea in deas_dicc["data"]:
#         adress = f"{dea['direccion_ubicacion']},{dea['direccion_via_nombre']}"
#         id, name, x, y = dea['codigo_dea'], dea['direccion_portal_numero'], dea['direccion_coordenada_x'], dea['direccion_coordenada_y']
#         # query = f'''INSERT INTO deas VALUES('{id}',"{name}","{adress}",{x},{y});'''
#         query = f'''INSERT INTO deas VALUES (?,?,?,?,?)''', (id,name,adress,x,y)
#         cur.execute(f'''INSERT INTO deas VALUES (?,?,?,?,?)''', (id,name,adress,x,y))
#         con.commit()
# #CREATE TABLE deas ("id" TEXT PRIMARY KEY UNIQUE, "name" TEXT, "adress" TEXT, "x" INTEGER, "y" INTEGER);

# # insert_data()

#DEA LOCATION
def sorter(item):
    nearest_deas = []
    distances = []
    for dea in item:
        distances.append(dea.keys())

    print(distances)
    print(distances[0])
    top_5 = distances[0:6]
    print(top_5)
    for dea in item:
        for distance in top_5:
            if dea[0] == distance:
                nearest_deas.append(dea)
    return nearest_deas

def nearest_dea(x,y):
    utm_x, utm_y = utm.from_latlon(x,y)[0:2]
    distances_to_deas = []
    url = "https://datos.comunidad.madrid/catalogo/dataset/35609dd5-9430-4d2e-8198-3eeb277e5282/resource/c38446ec-ace1-4d22-942f-5cc4979d19ed/download/desfibriladores_externos_fuera_ambito_sanitario.json"
    data = req.get(url).json()
    for dea in data["data"]:
        if dea["direccion_coordenada_x"] and dea["direccion_coordenada_y"]:
            base = int(dea["direccion_coordenada_x"]) - utm_x
            height = int(dea["direccion_coordenada_y"]) - utm_y
            hipo = ((base**2) + (height**2))**0.5
            distances_to_deas.append({hipo:dea})
   
    distances_to_deas.sort(key = lambda x: x.keys())
    print(distances_to_deas[:5])
    top_5 = distances_to_deas[:5]
    return top_5







