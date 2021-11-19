'''
Aquí estarán las funciones de la app del weather

A mostrar:
- La descripción del tiempo (nuboso, soleado...)
- La temp max y min
- Sensación térmica
- Humedad
- Velocidad del viento
'''
import requests as req


def menu():
    print("-"*50)
    print("EL TIEMPO".center(50))
    print("1. Buscar por ciudad")
    print("2. Buscar por coordendadas (latitud,longitud)")
    # print("3. Buscar el tiempo de una ciudad por fecha")
    print("Q. Terminar programa")
    print("-"*50)

def search_by_city(city):
    res = req.get(f"https://www.metaweather.com/api/location/search/?query={city}").json()
    woeid = res[0]["woeid"]
    res = req.get(f"https://www.metaweather.com/api/location/{woeid}").json()
    return res
    # print(woeid)
# search_by_city("madrid")

def pretty_print(city_name, city_list):
    print(city_name.upper().center(45))
    print(f"Descripción del tiempo: {city_list['consolidated_weather'][0]['weather_state_name']}")
    print(f"    Temperatura máxima: {city_list['consolidated_weather'][0]['max_temp']}")
    print(f"    Temperatura mínima: {city_list['consolidated_weather'][0]['min_temp']}")
    print(f"     Sensación térmica: {city_list['consolidated_weather'][0]['the_temp']}")
    print(f"               Humedad: {city_list['consolidated_weather'][0]['humidity']}")
    print(f"  Velocidad del viento: {city_list['consolidated_weather'][0]['wind_speed']}")
