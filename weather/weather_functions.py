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
import json

def get_data(json_file):
    with open(json_file, encoding="utf8") as file:
        return json.load(file)

woeids = get_data("woeids.json")  # Diccionario para poder evitar una request y así ahorrar tiempo

def write_data(data,json_file):
    with open(json_file, mode="w",encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def menu():
    print("-"*50)
    print("EL TIEMPO".center(50))
    print("1. Buscar por ciudad")
    print("2. Buscar por coordendadas (latitud,longitud)")
    print("3. Buscar el tiempo de una ciudad por fecha")
    print("Q. Terminar programa")
    print("-"*50)

def get_forcast(method,**kwargs):
    if kwargs.get("date"):
        woeid = woeids.get(method)
        if not woeid:
            try:
                woeid = req.get(f"https://www.metaweather.com/api/location/search/?query={method}").json()[0]["woeid"]
                woeids[method] = woeid
                write_data(woeids,"woeids.json")
            except IndexError:
                return None
        res = req.get(f"https://www.metaweather.com/api/location/{woeid}/{kwargs.get('date')[0]}/{kwargs.get('date')[1]}/{kwargs.get('date')[2]}").json()
        return res
    else:
        if kwargs.get("city"):
            woeid = woeids.get(method)
            if not woeid:
                try: 
                    woeid = req.get(f"https://www.metaweather.com/api/location/search/?query={method}").json()[0]["woeid"]
                    woeids[method] = woeid
                    write_data(woeids,"woeids.json")
                except IndexError:
                    return None
            res = req.get(f"https://www.metaweather.com/api/location/{woeid}").json()
            return res
        if kwargs.get("coordinates"):
            res = req.get(f"https://www.metaweather.com/api/location/search/?lattlong={method}").json()
            woeid = res[0]["woeid"]
            city_name = res[0]["title"]
            res = req.get(f"https://www.metaweather.com/api/location/{woeid}").json()
            if woeid not in woeids:
                woeids[city_name.lower()] = woeid
                write_data(woeids,"woeids.json")
            return res, city_name

def pretty_print(city_name, city_list):
    print(city_name.upper().center(45))
    print(f"Descripción del tiempo: {city_list['consolidated_weather'][0]['weather_state_name']}")
    print(f"    Temperatura máxima: {city_list['consolidated_weather'][0]['max_temp']}°")
    print(f"    Temperatura mínima: {city_list['consolidated_weather'][0]['min_temp']}°")
    print(f"     Sensación térmica: {city_list['consolidated_weather'][0]['the_temp']}°")
    print(f"               Humedad: {city_list['consolidated_weather'][0]['humidity']} %")
    print(f"  Velocidad del viento: {city_list['consolidated_weather'][0]['wind_speed']} m/s")

def pretty_print_date(city_name, city_list, date):
    print(f"{city_name.upper()}   {date}".center(50))
    print(f"Descripción del tiempo: {city_list[0]['weather_state_name']}")
    print(f"    Temperatura máxima: {city_list[0]['max_temp']}°")
    print(f"    Temperatura mínima: {city_list[0]['min_temp']}°")
    print(f"     Sensación térmica: {city_list[0]['the_temp']}°")
    print(f"               Humedad: {city_list[0]['humidity']} %")
    print(f"  Velocidad del viento: {city_list[0]['wind_speed']} m/s")






'''
Optimizar la función de forcast añadiendo manejo del error y sin quitar lo de los woeids
Entender como fucniona el json de woeids porque ni idea lol

'''