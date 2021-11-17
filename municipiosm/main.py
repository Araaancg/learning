import requests as req
import csv


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

