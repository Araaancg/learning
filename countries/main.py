import requests as req
import json

'''
APP DE TERMINAL
características
- buscar un país y que te devuelva
    - capital
    - población
    - superficie
    - idioma
'''

import c_functions as cf

separador = "-"*30

user = "0"

while user != "q".lower():
    cf.menu()
    user = input(": ")
    print(separador)

    if user == "1":
        user = input("Name of the country: ").lower()
        country_to_search = cf.get_by_term(user)
        print(separador)
        if country_to_search:
            cf.pretty_print(country_to_search)
        else:
            print(f"The country {user.capitalize()} does not exist in our data base")
        input(f"{separador}\nPress enter to return to the main menu ")

    if user == "2":
        user = input("Name of the country: ").lower()
        country_to_search = cf.get_by_term(user)
        if country_to_search:
            flag_url = country_to_search[0]["flags"]["svg"]
            print(flag_url)
            flag = req.get(flag_url).content
            with open(f"./img/{country_to_search[0]['name']['common'].lower()}.svg", mode="wb") as file:
                file.write(flag)
        else:
            print(f"The country {user.capitalize()} does not exist in our data base")
        input(f"{separador}\nPress enter to return to the main menu ")

    if user == "3":
        user = cf.choose_continent()
        print(separador)
        request = cf.get_by_term(user, continent=True)
        
        countries = list(map(lambda country: {
            "name":country["name"]["common"],
            # "capital":country["capital"][0],
            # "capital":country.get("capital"[0]),
            "area":country["area"],
            "drive_side":country["car"]["side"],
            "population":country["population"]
        }, request))

        cf.quiz(countries,user)

        input(f"{separador}\nPress enter to return to the main menu ")
