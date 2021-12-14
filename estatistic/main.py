# Datos abiertos de la c. Madrid, incidencia covid
import requests as req
import json
from obj_std import *
import matplotlib.pyplot as plt

url = "https://datos.comunidad.madrid/catalogo/dataset/b3d55e40-8263-4c0b-827d-2bb23b5e7bab/resource/907a2df0-2334-4ca7-aed6-0fa199c893ad/download/covid19_tia_zonas_basicas_salud_s.json"
res = req.get(url).json()

with open("./covid.json",mode="w",encoding="utf8") as file:
    json.dump(res,file,indent=4,ensure_ascii=False)

def get_data(json_file):
    with open(json_file,encoding="utf8") as file:
        return json.load(file)

data = get_data("./covid.json")


# Función que convierte el data en un DICCIONARIO (keys: fechas, values: lista de info de cada municipio(dic))
def data_by_date(dataset):
    result = {}
    for zone in dataset["data"]:
        idate = zone["fecha_informe"].split(" ")[0]
        if result.get(idate):
            result[idate].append(zone)
        else:
            result[idate] = [zone]
    return result

data_by_date = data_by_date(data)


#CASOS CONFIRMADOS TOTALES
casos_totales = sum([zone["casos_confirmados_totales"] for zone in data_by_date["2021/12/07"]])
# print(casos_totales)
# print(len(data_by_date["2021/12/07"]))


# GRÁFICA
x = [num for num in range(1, len(data_by_date) + 1)] # Representa las semanas (de la primera a la 80)
y = [] 
for zones_by_date in data_by_date.values(): #valores de y
      y.append(sum(z["casos_confirmados_totales"] for z in zones_by_date))
y.reverse() 


analyze = Std(x,y)

predicted_y = analyze.lineals




