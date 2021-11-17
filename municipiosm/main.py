import requests as req
import csv

# url = "https://datos.comunidad.madrid/catalogo/dataset/032474a0-bf11-4465-bb92-392052962866/resource/ee750429-1e05-411a-b026-a57ea452a34a/download/municipio_comunidad_madrid.csv"
# res = req.get(url).content #de la url cogemos los datos, en este caso el csv
# res = res.decode("utf-8", errors="replace")
# print(res)
#decodificamos el csv porque viene en type bytes

# with open("data_municipios.csv", mode="w", encoding="utf8") as file:
#     file.write(res)

with open("./data_municipios.csv", mode="r", encoding="utf8") as file:
    data = csv.reader(file)
    next(data)
    print(next(data))
