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

weather_abbreviation_dic = {
    "lr":"Light Rain",
    "hr":"Heavy Rain",
    "h":"Hail",
    "sn":"Snow",
    "sl":"Sleet",
    "t":"Thunderstorm",
    "s":"Showers",
    "hc":"Heavy Cloud",
    "lc":"Light Cloud",
    "c":"clear"
}

def get_data(json_file):
    with open(json_file, encoding="utf8") as file:
        return json.load(file)

woeids_dic = get_data("woeids.json")  # Diccionario para poder evitar una request y así ahorrar tiempo

def write_data(data,json_file):
    with open(json_file, mode="w",encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def menu():
    print("-"*50)
    print("EL TIEMPO".center(50))
    print("1. Buscar por ciudad")
    print("2. Buscar por coordendadas (latitud,longitud)")
    print("3. Buscar el tiempo de una ciudad por fecha")
    print("4. Planea tu viaje")
    print("Q. Terminar programa")
    print("-"*50)

def get_forecast(method,**kwargs):
    if kwargs.get("date"):
        woeid = woeids_dic.get(method)
        if not woeid:
            try:
                woeid = req.get(f"https://www.metaweather.com/api/location/search/?query={method}").json()[0]["woeid"]
                woeids_dic[method] = woeid
                write_data(woeids_dic,"woeids.json")
            except IndexError:
                return None
        res = req.get(f"https://www.metaweather.com/api/location/{woeid}/{kwargs.get('date')[0]}/{kwargs.get('date')[1]}/{kwargs.get('date')[2]}").json()
        return res
    else:
        if kwargs.get("city"):
            woeid = woeids_dic.get(method)
            if not woeid:
                try: 
                    woeid = req.get(f"https://www.metaweather.com/api/location/search/?query={method}").json()[0]["woeid"]
                    woeids_dic[method] = woeid
                    write_data(woeids_dic,"woeids.json")
                except IndexError:
                    return None
            res = req.get(f"https://www.metaweather.com/api/location/{woeid}").json()
            return res
        if kwargs.get("coords"):
            res = req.get(f"https://www.metaweather.com/api/location/search/?lattlong={method}").json()
            woeid = res[0]["woeid"]
            city_name = res[0]["title"]
            res = req.get(f"https://www.metaweather.com/api/location/{woeid}").json()
            if woeid not in woeids_dic:
                woeids_dic[city_name.lower()] = woeid
                write_data(woeids_dic,"woeids.json")
            return res, city_name


# def get_forecast(location, **kwargs):
#     # PRIMER PASO: encontrar el woeid
#     term = "query"
#     woeid = woeids_dic.get("location")
#     if not woeid:
#         if kwargs.get("coords"):
#             term = "lattlong"

#         try: # Manejo de errores consultando la base de datos
#             woeid = req.get(f"https://www.metaweather.com/api/location/search/?{term}={location}").json()[0]["woeid"]
#         except:
#             return None


#     # SEGUNDO PASO: valorar si nos han pasado una fecha o no
#     if kwargs.get("date"): # Fecha SI
#         try: # Manejo de errores
#             date = f"{kwargs.get('date')[0]}/{kwargs.get('date')[1]}/{kwargs.get('date')[2]}"
#             res = req.get(f"https://www.metaweather.com/api/location/{woeid}/{date}").json()
#             return res
#         except:
#             return None
#     # Fecha NO
#     try: # Manejo de errores
#         res = req.get(f"https://www.metaweather.com/api/location/{woeid}").json()
#         return res
#     except:
#         return None


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

def warning_bad_weather(city_list):
    bad_weather = ["sn","sl","h","t","hr","lr"]
    # sn = snow, sl = sleet, h = hail, t = thunderstorm, hr = heavy rain, lr = light rain
    for city in city_list:
        prediction_weather = city["consolidated_weather"][0]["weather_state_abbr"]
        city_name = city["title"]
        if prediction_weather in bad_weather:
            weather_state = weather_abbreviation_dic[prediction_weather]
            print(f"WARNING: en {city_name} va a hacer mal tiempo ({weather_state})")
        else:
            print(f"Yay, en {city_name} va a hacer buen tiempo")




'''
Optimizar la función de forcast añadiendo manejo del error y sin quitar lo de los woeids
def forecast(location, **kwargs) siendo kwargs date=fecha_a_elegir y coords=True/False
- Empezar por buscar el woeids
    primero en el json, si no está en el json es posible que hayn puesto la clave de coords
    en ese caso cambiar term a lattlong. si no han puesto la clave de coords no cambiar term
    pero si que tenemos que buscar el woeid
    poner manejo de error para esa búsqueda
    añadir los woeids que no estén el json y cuando se busque por coords añadir todos los que
    te salgan
- Un vez tengamos el woeid comprobar que no nos han pedido una fecha
    en caso de que sea así, o sea que no tengamos fecha, continuamos con el programa buscando
    toda la info del pronóstico
    en caso de que tengamos una fecha a elegir pues se comprueba y se añade a la url
    añadir manejo del error en la búsqueda no vaya a ser...

Añadir lo de que te salgan los pronósticos de los tres siguientes dias, no sé si hacerlo 
una opción voluntaria a gusto del consumidor o que se joday que le salga siempre
Añadir también lo de los viajes, con lo de las distancias etc
meter en lo que llevo de los viajes manejo del error, en el warning digo

me voy a divertir mañana si

si ya me da tiempo, que obviamente no tiene pinta, añadir un while para que si se equivoca
al añadir la ciudad pues que no vuelva al menú principal, vamos a darle al user otra
oportunidad

ya si encima me aburro mucho añadir lo de ciudades favoritas

ambiciosa me llamaban 

genovese.work@gmail.com
genovese.work@protonmail.com

'''