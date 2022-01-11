'''
Funciones para la app del weather

A mostrar:

- La descripción del clima (soleado, nuboso y lluvioso)
- La máxima
- La mínima
- Sensación térmica
- Humedad
- Velocidad del viento y dirección

'''
import json
import requests as req

def menu():
    print("-"*50)
    print("WEATHER APP".center(50))
    print("1. Search by city")
    print("2. Search by coordinates")
    print("3. Search an especific date")
    print("4. Plan a trip")
    print("-"*50)


def get_data(json_file):
    with open(json_file, encoding="utf8") as file:
        return json.load(file)

woeids_dic = get_data("woeids.json")  # Diccionario para poder evitar una request y así ahorrar tiempo

def write_data(data,json_file):
    with open(json_file, mode="w",encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_woeid(location, **kwargs):
    term = "query"
    woeid = woeids_dic.get(location) # Lo buscamos en el diccionario de woeids
    limit = kwargs.get("limit")

    if not woeid:
        if kwargs.get("coords"):
            term = "lattlong"
        # Hacemos el request
        url = f"https://www.metaweather.com/api/location/search/?{term}={location}"
        request = req.get(url).json()

        if request: 
            for city in request: # Cogemos totos los woeids posibles
                woeids_dic[city["title"].lower()] = city["woeid"]
                write_data(woeids_dic,"woeids.json")
            if limit:
                return [city["woeid"] for city in request[0:limit]]    
            else:
                woeid = request[0]["woeid"]    
        else:
            return None
    return [woeid]

def get_forecast(location,**kwargs):
    woeid = get_woeid(location, **kwargs)
    if woeid:
        woeid = woeid[0]
        date = kwargs.get("date")
        url = f"https://www.metaweather.com/api/location/{woeid}/"
        if date:
            url += date
        request = req.get(url).json()
        if request:
            return request
        else:
            return None
    else: 
        return None


def pretty_print(data,**kwargs): 
# Importante, cuando buscamos por date nos devuelve una lista, cuando lo hacemos sin date nos devuelve un dicc
    limit = 1
    if kwargs.get("see_next_three_days"):
        limit = 4
    for num in [n for n in range(0,limit)]:
        if type(data) == list:
            print(f"{kwargs.get('location').upper()} {kwargs.get('date')}".center(50))
            print(f"Descripción del tiempo: {data[num]['weather_state_name']}")
            print(f"    Temperatura máxima: {data[num]['max_temp']}°")
            print(f"    Temperatura mínima: {data[num]['min_temp']}°")
            print(f"     Sensación térmica: {data[num]['the_temp']}°")
            print(f"               Humedad: {data[num]['humidity']} %")
            print(f"  Velocidad del viento: {data[num]['wind_speed']} m/s")
            print(f"  Dirección del viento: {data[num]['wind_direction_compass'].upper()}")
        else:
            print(data['title'].upper().center(45))
            print(f"Descripción del tiempo: {data['consolidated_weather'][num]['weather_state_name']}")
            print(f"    Temperatura máxima: {data['consolidated_weather'][num]['max_temp']}°")
            print(f"    Temperatura mínima: {data['consolidated_weather'][num]['min_temp']}°")
            print(f"     Sensación térmica: {data['consolidated_weather'][num]['the_temp']}°")
            print(f"               Humedad: {data['consolidated_weather'][num]['humidity']} %")
            print(f"  Velocidad del viento: {data['consolidated_weather'][num]['wind_speed']} m/s")
            print(f"  Dirección del viento: {data['consolidated_weather'][num]['wind_direction_compass'].upper()}")
        if kwargs.get("see_next_three_days"):
            input("\nPress enter to continue ")
            print(" ")


def plan_trip(A,B):
    url_A = f"https://www.metaweather.com/api/location/search/?query={A}"
    coords_A = req.get(url_A).json()[0]["latt_long"]
    url_A = f"https://www.metaweather.com/api/location/search/?lattlong={coords_A}"
    req_A = req.get(url_A).json()

    is_trip_possible = False

    B_position = None

    for i,city in enumerate(req_A[1:]):
        if city["title"].lower() == B.lower():
            is_trip_possible = True
            B_position = i

    if is_trip_possible:
        velocity = 100 #km/h
        # AVISO DE MAL TIEMPO
        for city in [A,B]:
            woeid = woeids_dic.get(city)
            if not woeid:
                request = req.get(f"https://www.metaweather.com/api/location/search/?query={city}").json()
                if request: 
                    for city in request: # Cogemos totos los woeids posibles
                        woeids_dic[city["title"].lower()] = city["woeid"]
                        write_data(woeids_dic,"woeids.json")
                        woeid = request[0]["woeid"] 
            forecast = req.get(f"https://www.metaweather.com/api/location/{woeid}/").json()["consolidated_weather"][0]
            if forecast["weather_state_abbr"] in ["sn","sl","h","t","hr","s","lr"]:
                print(f"WARNING: there is bad weather in {city.capitalize()} ({forecast['weather_state_abbr']}), trip won't be possible")
                is_trip_possible = False
                break
            else:
                print(f"Nice! weather won't be a problem in {city.capitalize()} ({forecast['weather_state_abbr']})")
            is_wind_speed = True if forecast["wind_speed"] >= 10 else False
            if is_wind_speed:
                velocity = 90 #km/h

        # DISTANCE
        distance = req_A[B_position]["distance"] / 1000 # Lo convertimos a km
        # DURACIÓN DEL TRAYECTO
        time = distance / velocity # horas

        if is_trip_possible: # Solo si el trayecto es posible damos la info, sino no
            print(" ")
            print(f"Distance to go {distance}km")
            print(f"Trip duration {time} hours")
    else:
        print("Sorry, trip not possible, cities are too far away")



