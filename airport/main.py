import datetime as dt
from math import e
from models import *
from random import randint
import json

airports = get_data("./airports.json")
user = ""


separador = "-"*30

while user.lower() != "q":
    tickets = get_data("./tickets.json")
    # print(tickets)
    cities = [city["city"] for city in airports.values()]
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
        departures = airports[country_codes[destination]][country_codes[origin]]["departures"]

        print("Choose a time of departure:")
        for i,time in enumerate(departures):
            print(f"{i+1}. {time}")
        departure_hour = departures[int(input(": ")) -1]

        flight_time = airports[country_codes[destination]][country_codes[origin]]["flight_time"]
        utc_destination = airports[country_codes[destination]]["UTC"]
        utc_origin = airports[country_codes[origin]]["UTC"]

        #CREATE OBJECT
        flight_object = Flight(origin,destination,departure_hour,flight_time,utc_destination,utc_origin,str(randint(100000,999999)))
        flight_object.write_data

        print(separador)

        flight_object.pretty_print()
    
        input(f"{separador}\nPress enter to return to the main menu ")

    if user == "2": #Cancel flight
        flight_id = input("Enter your flight's id: ")
        print(separador)
        all_flights_id = [ticket["id"] for ticket in tickets["tickets"]]

        if flight_id in all_flights_id:
            print("FLIGHT TO CANCEL".center(30))
            for k,v in tickets["tickets"][all_flights_id.index(flight_id)].items():
                print(f"{k.capitalize()}: {v}")
            print(separador)
            user = input("Are you sure you want to cancel this flight? (y/n): ")
            if user.lower() == "y":
                tickets["tickets"].pop(all_flights_id.index(flight_id))
                with open("./tickets.json", mode="w", encoding="utf8") as file:
                    json.dump(tickets,file,ensure_ascii=False,indent=4)
                print("Flight canceled")
            else:
                print("Action canceled")
        
        else:
            print("Sorry, you have no flights with that id number")

        input(f"{separador}\nPress enter to return to the main menu ")

    if user == "3": #Change flight, solo se puede cambiar la hora de salida
        flight_id = input("Enter your flight's id: ")
        print(separador)
        all_flights_id = [ticket["id"] for ticket in tickets["tickets"]]

        if flight_id in all_flights_id:
            print("FLIGHT TO MODIFY".center(30))
            for k,v in tickets["tickets"][all_flights_id.index(flight_id)].items():
                print(f"{k.capitalize()}: {v}")
            print(separador)
            
            user = input("Are you sure you want to modify your departure hour? (y/n): ")
            print(separador)
            if user.lower() == "y":

                origin, destination = tickets["tickets"][all_flights_id.index(flight_id)]["origin"], tickets["tickets"][all_flights_id.index(flight_id)]["destination"]

                departures = airports[country_codes[destination]][country_codes[origin]]["departures"]
                departures.remove(tickets["tickets"][all_flights_id.index(flight_id)]["departure_hour"])

                print("Choose a time of departure:")
                for i,time in enumerate(departures):
                    print(f"{i+1}. {time}")
                departure_hour = departures[int(input(": ")) -1]

                print(separador)

                tickets["tickets"][all_flights_id.index(flight_id)]["departure_hour"] = departure_hour
                with open("./tickets.json", mode="w", encoding="utf8") as file:
                    json.dump(tickets,file,ensure_ascii=False,indent=4)
                print("Departure hour modified")
            
            else:
                print("Action canceled")
        
        else:
            print("Sorry, you have no flights with that id number")

        input(f"{separador}\nPress enter to return to the main menu ")