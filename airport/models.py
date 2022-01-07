import json

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
    print("3. Change flight")
    print("2. Cancel flight")
    print("Q. Quit")
    print("-"*30)     

def write_data(json_file):
    with open(json_file,encoding="utf8") as file:
        return json.load(file)

flights = write_data("./airports.json")

class Flight:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

    # @property
    # def departure_time(self):
    #     departures = flights[country_codes[self.destination]][country_codes[self.origin]]["departures"]
        