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
    if user in options:
        if user == "1":
            user = input("Introduzca el nombre de una ciudad: ").lower()
            # info_city = wf.search_by_city(user)
            info_city = wf.get_forcast(user,city=True)
            print("-"*50)
            wf.pretty_print(user,info_city)
            print("-"*50)
            user = input("Presione enter para volver al menu principal ")
        if user == "2":
            lattlong = input("Introduzca la latitud y la longitud deseadadeseada (latt,long): ")
            info_city = wf.get_forcast(lattlong, coordinates=True)[0]
            city_name = wf.get_forcast(lattlong, coordinates=True)[1]     
            print("-"*50)
            wf.pretty_print(city_name, info_city)
            print("-"*50)
            user = input("Presione enter para volver al menú principal ")
        if user == "3":
            user = input("Introduzca el nombre de una ciudad: ").lower()
            print("A continuación introduzca la fecha")
            year = input("Año: ")
            month = input("Mes: ")
            day = input("Day: ")
            print("-"*50)
            info_city = wf.get_forcast(user,date=(year,month,day))
            wf.pretty_print_date(user,info_city)
    else:
        print("Input inválido, por favor introduzca de nuevo la opción deseada")
        
print("Hasta pronto!")