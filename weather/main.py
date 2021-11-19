'''
Aplicación del tiempo usando una url dinámica para que depende de la ciudad que pone el user sale 
una info u otra
En el menú hay que poner:
- Buscar por coordenadas, latitud y longitud
- Buscar por ciudad
- Buscar por ciudad y fecha *DE MOMENTO NO*

hacer lo de si mete un numero que no esta que de un mensaje erroneo y vuelva al menu
'''

import requests as req
import weather_functions as wf

options = ["1","2","3","q"]

user = "0"

while user.lower() != "q":
    wf.menu()
    user = input(": ")
    if user == "1":
        user = input("Introduzca el nombre de una ciudad: ").lower()
        info_city_to_search = wf.search_by_city(user)
        print("-"*50)
        wf.pretty_print(user,info_city_to_search)
        print("-"*50)
        user = input("Presione enter para volver al menu principal ")
        
print("Hasta pronto!")