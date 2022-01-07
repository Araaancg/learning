import json
import datetime as dt
from hashlib import sha256
from random import random

SECRET = b"ryanground"

country_codes = {
    "Buenos Aires":"ARG",
    "Lima":"PER",
    "Sao Paulo":"BRA",
    "Madrid":"SPA"
}

def menu():
    print("-"*30)
    print("AIRPORT SHOP".center(30))
    print("1. Purchase flight")
    print("2. Cancel flight")
    print("3. Change flight")
    print("Q. Quit")
    print("-"*30)     

def get_data(json_file):
    with open(json_file,encoding="utf8") as file:
        return json.load(file)

flights = get_data("./airports.json")

class Flight:
    def __init__(self, origin, destination, departure_hour, flight_time, utc_destination):
        self.origin = origin
        self.destination = destination
        self.departure_hour = departure_hour
        self.flight_time = flight_time
        self.utc_destination = utc_destination
        
    # @staticmethod
    # def tomorrow():
    #     pre = dt.datetime.now() + dt.datetime(days=1)
    #     pos = dt.datetime(year=pre.year, month=pre.month, day=pre.day)
    #     return pos

    @property
    def eta(self):
        date1 = dt.datetime.fromisoformat(f"2022-01-07T{self.departure_hour}")
        flight_time = dt.timedelta(hours=self.flight_time)
        eta_origen = date1 + flight_time
        utc_destination = dt.timedelta(hours=self.utc_destination)
        eta_destination = eta_origen + utc_destination
        return eta_origen, eta_destination

    def pretty_print(self):
        print("FLIGHT INFORMATION".center(30))
        print(f"Origin: {self.origin}")
        print(f"Destination: {self.destination}")
        print(f"F. Duration: {self.flight_time} hours")
        print(f"Estimated arrival (origin): {self.eta[0]} hora en {self.origin}")
        print(f"Estimated arrival (local): {self.eta[1]} hora en {self.destination}")
    
    @property
    def create_id(self):
        id = sha256(self.origin.encode())
        id.update(self.destination.encode())
        id.update(self.departure_hour.encode())
        return id.hexdigest()

    @property
    def flight_dicc(self):
        flight_dicc = {
            "id":self.create_id,
            "purchase_time":dt.datetime.isoformat(dt.datetime.now()),
            "origin":self.origin,
            "destination":self.destination,
            "departure_hour":self.departure_hour,
            "flight_time":self.flight_time
        }
        return flight_dicc 

    @property
    def write_data(self):
        dicc = {"tickets":[]}
        dicc["tickets"].append(self.flight_dicc)
        with open("./tickets.json", mode="w", encoding="utf8") as file:
            json.dump(dicc,file,ensure_ascii=False,indent=4)



    
