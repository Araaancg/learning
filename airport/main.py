import datetime as dt
from models import *

flights = get_data("./airports.json")
# print(flights)
user = ""

cities = ["Sao Paulo","Madrid","Lima","Buenos Aires"]

separador = "-"*30

while user.lower() != "q":
    menu()
    user = input(": ")
    print(separador)

    if user == "1":
        #CHOOSE CITY OF ORIGIN
        print("Where do you fly from?")
        for i,origin in enumerate(cities):   
            print(f"{i+1}. {origin}")
        origin = cities[int(input(": ")) -1]

        cities.remove(origin)

        print(separador)

        #CHOOSE DESTINATION
        print("Available destinations:")
        for i,destination in enumerate(cities):
            print(f"{i+1}. {destination}")
        destination = cities[int(input(": "))-1]

        print(separador)

        #CHOOSE TIME OF DEPARTURE
        departures = flights[country_codes[destination]][country_codes[origin]]["departures"]

        print("Choose a time of departure:")
        for i,time in enumerate(departures):
            print(f"{i+1}. {time}")
        departure_hour = departures[int(input(": ")) -1]

        flight_time = flights[country_codes[destination]][country_codes[origin]]["flight_time"]
        utc_destination = flights[country_codes[destination]]["UTC"]

        #CREATE OBJECT
        flight_object = Flight(origin,destination,departure_hour,flight_time,utc_destination)
        flight_object.write_data

        print(separador)

        flight_object.pretty_print()
    
        input(f"{separador}\nPress enter to return to the main menu ")

    if user == "2": #Cancel flight
        pass

    if user == "3": #Change flight
        pass
