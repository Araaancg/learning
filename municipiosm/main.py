import requests as req
import csv
import json


# url = "https://datos.comunidad.madrid/catalogo/dataset/032474a0-bf11-4465-bb92-392052962866/resource/ee750429-1e05-411a-b026-a57ea452a34a/download/municipio_comunidad_madrid.csv"
# res = req.get(url).content #de la url cogemos los datos, en este caso el csv
# res = res.decode("utf-8", errors="replace")
# print(res)

#decodificamos el csv porque viene en type bytes

# with open("data_municipios.csv", mode="w", encoding="utf8") as file:
#     file.write(res)

def get_by_ine(dataset, ine_code):
    for mun in dataset[1:]:
        if mun[2] == ine_code:
            return mun

def bigger_mun(dataset):
    big_area = 0
    big_mun = None
    for mun in dataset[1:]:
        if float(mun[-2]) > big_area:
            big_area = float(mun[-2])
            big_mun = mun
    return big_mun

def sup_total(dataset):
    superficie = 0
    for mun in dataset[1:]:
        superficie += float(mun[-2])
        # print(superficie)
    return superficie

def get_pobl_total(dataset):
    pobl_total = 0
    for mun in dataset[1:]:
        pobl_local = float(mun[-1])*float(mun[-2])
        pobl_total += pobl_local
    return pobl_total



with open("./data_municipios.csv", mode="r", encoding="utf8") as file:
    data = list(csv.reader(file, delimiter=";"))
    del data[0]
    

# #obtener municipio por ine
# mun_to_search = get_by_ine(data, "28014")
# print(mun_to_search)

# #municipio más grande
# mun_to_search = bigger_mun(data)
# print(mun_to_search)

# #Obtener superficie total
# superficie_total = sup_total(data)
# print(superficie_total)

# #Obtener la poblacion de madrid
# poblacion_madrid = get_pobl_total(data)
# print(poblacion_madrid)

# #Obtener la población media de los municipios
# poblacion_media = get_pobl_total(data) / len(data)
# print(poblacion_media)

#Ley de benhorf


#Ejercicio 8. convertir el csv en json

# función de conversión y luego le aplico el data set

def csv_to_dict(data_base):
    with open("data.csv", mode="r") as file:
        csv_reader = csv.reader(file, delimiter=";")
        next(csv_reader)
        for i, row in enumerate(csv_reader):
            # print(i, row)
            book = {
                "id": row[0],
                "title": row[1],
                "author":row[2],
                "genre":row[3]
            }
            data_base.append(book)

data_dict = []

def csv_to_json(new_dict):
    with open("data_municipios.csv", mode="r", encoding="utf8") as file:
        csv_reader = csv.reader(file, delimiter=";")
        next(csv_reader)
        for i, row in enumerate(csv_reader):
            mun = {
                "municipio_codigo":row[0],
                "municipio_nombre":row[1],
                "municipio_codigo_ine":row[2],
                "nuts4_nombre":row[3],
                "superficie_km2":row[4],
                "densidad_por_km2":row[5],
            }
            new_dict.append(mun)
        json.dump(dict(new_dict),"data_municipios.json")

csv_to_json(data_dict)
