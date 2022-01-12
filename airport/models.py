import json
import datetime as dt


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
tickets_dicc = get_data("tickets.json")

class Flight:
    def __init__(self, origin, destination, departure_hour, flight_time, utc_destination,utc_origin,identification_number):
        self.origin = origin
        self.destination = destination
        self.departure_hour = departure_hour
        self.flight_time = flight_time
        self.utc_destination = utc_destination
        self.utc_origin = utc_origin
        self.identification_number = identification_number
        
    @staticmethod
    def tomorrow():
        pre = dt.datetime.now() + dt.timedelta(days=1)
        pos = dt.datetime(year=pre.year, month=pre.month, day=pre.day)
        return pos

    @property
    def eta(self):
        date1 = dt.datetime.fromisoformat(f"{dt.datetime.isoformat(self.tomorrow()).split('T')[0]}T{self.departure_hour}")
        flight_time = dt.timedelta(hours=self.flight_time)
        eta_origen = date1 + flight_time
        utc_destination = dt.timedelta(hours=(self.utc_destination-self.utc_origin))
        eta_destination = eta_origen + utc_destination
        return eta_origen, eta_destination
  
    @property
    def flight_dicc(self):
        flight_dicc = {
            "id":self.identification_number,
            "purchase_time":dt.datetime.isoformat(dt.datetime.now()),
            "origin":self.origin,
            "destination":self.destination,
            "departure_hour":self.departure_hour,
            "flight_time":self.flight_time
        }
        return flight_dicc 

    @property
    def write_data(self):
        tickets_dicc["tickets"].append(self.flight_dicc)
        with open("./tickets.json", mode="w", encoding="utf8") as file:
            json.dump(tickets_dicc,file,ensure_ascii=False,indent=4)
    
    def pretty_print(self):
        print("FLIGHT INFORMATION".center(30))
        print(f"Identification number: {self.identification_number}")
        print(f"Origin: {self.origin}")
        print(f"Destination: {self.destination}")
        print(f"Departure time: {self.departure_hour}")
        print(f"F. Duration: {self.flight_time} hours")
        print(f"Estimated arrival (origin): {self.eta[0]} hora en {self.origin}")
        print(f"Estimated arrival (local): {self.eta[1]} hora en {self.destination}")