import datetime as dt
from models import *

# flights = write_data("./airports.json")
# print(flights)
user = ""

cities = ["Sao Paulo","Madrid","Lima","Buenos Aires"]

separador = "-"*30

while user.lower() != "q":
    menu()
    user = input(": ")
    print(separador)

    if user == "1":
        print("Where do you fly from?")
        for i,origin in enumerate(cities):   
            print(f"{i+1}. {origin}")
        origin = cities[int(input(": ")) -1]

        print(separador)

        print("Available destinations:")
        for i,destination in enumerate(cities):
            print(f"{i+1}. {destination}")
        destination = cities[int(input(": "))-1]

        print(separador)

        flight_object = Flight(origin,destination)
        
        print(flight_object.departure_time)

        input(f"{separador}\nPress enter to return to the main menu ")

