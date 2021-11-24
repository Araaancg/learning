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

options = ["1","2","3","4","q"]

user = "0"

while user.lower() != "q":
    wf.menu()
    user = input(": ")
    if user in options:

        # Buscar por ciudad
        if user == "1":
            user = input("Introduzca el nombre de una ciudad: ").lower()
            info_city = wf.get_forecast(user,city=True)
            if info_city: 
                print("-"*50)
                wf.pretty_print(user,info_city)
                print("-"*50)
            else:
                print("-"*50)
                print("Localización no encontrada en la base de datos")
                # print("-"*50)
            user = input("Presione enter para volver al menu principal ")
        
        # Buscar por coordenadas
        if user == "2":
            lattlong = input("Introduzca la latitud y la longitud deseadadeseada (latt,long): ")
            info_city = wf.get_forecast(lattlong, coords=True)[0]
            city_name = wf.get_forecast(lattlong, coords=True)[1]   
            print("-"*50)
            wf.pretty_print(city_name, info_city)
            print("-"*50)
            user = input("Presione enter para volver al menú principal ")

        # Buscar por fecha y ciudad
        if user == "3":
            user = input("Introduzca el nombre de una ciudad: ").lower()
            print("A continuación introduzca la fecha")
            year = input("Año: ")
            month = input("Mes: ")
            day = input("Day: ")
            print("-"*50)
            info_city = wf.get_forecast(user,date=(year,month,day))

            # Manejo del error
            if info_city:
                wf.pretty_print_date(user,info_city,f"{day}/{month}/{year}")
            else:
                print("Datos no encontrados en la base de datos")
        
        if user == "4":
            city_1 = input("Introduza el origen: ")
            city_1 = wf.get_forecast(city_1, city=True)
            city_2 = input("Introduzca el destino: ")
            city_2 = wf.get_forecast(city_2, city=True)
            cities = [city_1,city_2]
            print("-"*50)
            wf.warning_bad_weather(cities)
            print("-"*50)
            user = input("Presione enter para volver al menú principal ")

    else: # Input en el menú inválido
        print("Input inválido, por favor introduzca de nuevo la opción deseada")
        
print("Hasta pronto!")



'''
Nueva parte del programa: VIAJES

La misma permitirá elegir un origen y un destino e indicará, en base al clima lo siguiente:
- Aviso de mal clima (sn, sl, h, t hr)
- Distancia a recorrer (km.)
- Duración del trayecto (100 km/h)
- Si la velocidad del viento supera los 10 nudos, reducir la velocidad media a 90 km/h
'''