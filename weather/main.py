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
from w_funcs import *

user = "0"
separador = "-"*50


while user.lower() != "q":
    menu()
    user = input(": ")
    print(separador)

    if user == "1": # Search by city
        location = input("Enter city's name: ")
        print(separador)
        forecast = get_forecast(location)
        if forecast:
            user = input("Do you want to see the forecast for the next three days too? (y/n): ")
            print(separador)
            if user.lower() != "n": 
                pretty_print(forecast, see_next_three_days=True) # Muestra HOY y los tres siguientes días
            else:
                pretty_print(forecast)
        else:
            print("Data not found in our database")
        print(separador)
        input("Press enter to return to the main menu ")

    if user == "2": # Search by coordinates
        location = input("Enter coordinates (latt,long): ")
        print(separador)
        forecast = get_forecast(location, coords=True)
        if forecast:
            user = input("Do you want to see the forecast for the next three days too? (y/n): ")
            print(separador)
            if user.lower() != "n": 
                pretty_print(forecast, see_next_three_days=True) # Muestra HOY y los tres siguientes días
            else:
                pretty_print(forecast)
        else:
            print("Data not found in our database")
        print(separador)
        input("Press enter to return to the main menu ")
    
    if user == "3": # Search by an especific date
        location = input("Enter city's name: ")
        date = input("Enter date (yyyy/mm/dd): ")
        print(separador)
        try:
            forecast = get_forecast(location, date=date)
            pretty_print(forecast, date=date, location=location)
        except:
            print("Data not found in our database")
        print(separador)
        input("Press enter to return to the main menu ")
    
    if user == "4": # Plan your trip
        locationA = input("Enter origin city: ")
        locationB = input("Enter destination city: ")
        print(separador)
        plan_trip(locationA,locationB)
        print(separador)
        input("Press enter to return to the main menu ")
        '''
        La función lo primero que hace es ver si las ciudades están muy lejos, si lo están dejará de funcionar e imprimirá un mensaje
        tipo "las ciudades están muy lejos, viaje no posible"
        Lo segundo que hace es ver el tiempo, si en alguna de las dos ciudades hay mal tiempo también dejará de funcionar ya que 
        el viaje no será posible, imprimirá por supuesto un warning
        Si todo sale bien y las ciudades están medianamente cerca y además hay buen tiempo, imprimirá la distancia y la duración
        del trayecto además de un mensaje diciendo que hace buen tiempo
        '''