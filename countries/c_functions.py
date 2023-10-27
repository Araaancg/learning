import requests as req
import json
import random

separador = "-"*30

def menu():
    print("-"*30)
    print("COUNTRIES".center(30))
    print("1. Search info about a country")
    print("2. Download a country's flag")
    print("3. Game")
    print("Q. Quit")
    print("-"*30)

def get_by_term(c, **kwargs):
    term = "name"
    if kwargs.get("continent"):
        term = "region"
    c_info = req.get(f"https://restcountries.com/v3.1/{term}/{c}").json()  
    try:
        c_info["status"]
        return None
    except:
        return c_info

def pretty_print(country_info):
    print(country_info[0]["name"]["common"].upper().center(30))
    print(f"   Capital: {country_info[0]['capital'][0]}")
    print(f"Population: {country_info[0]['population']} habitants")
    print(f"   Surface: {country_info[0]['area']} km2")
    languages = list(country_info[0]['languages'].values())
    print(f" Languages: {languages}")

def choose_continent():
    continents = ["Asia","Europe","Oceania","Africa","Americas"]
    print("Continents".center(20))
    for i, continent in enumerate(continents):
        print(f"{i+1}. {continent}")
    print(separador)
    user = input("Choose the continent you wanna play with: ")
    if int(user) > 0 and int(user) <= len(continents):
        user_cont = continents[int(user)-1]
        return user_cont.lower()
    else:
        return None 



def quiz(countries,continent): # continent = nombre del continente elegido (str), countries = lista de paises
    count = 1
    score = 0

    while count <= 5:
    
        print(f"Question {count}".center(20))

        ch_co = random.choice(countries)
        quiz = [
            # {
            #     "q":f"Capital of {ch_co['name']}",
            #     "a":ch_co['capital'],
            #     "o":[random.choice(countries)['capital'], random.choice(countries)['capital'],ch_co['capital']]
            # },
            {
                "q":f"Population of {ch_co['name']}",
                "a":ch_co['population'],
                "o":[random.choice(countries)['population'], random.choice(countries)['population'],ch_co['population']]
            },
            {
                "q":f"What side do they drive from in {ch_co['name']}?",
                "a":ch_co['drive_side'],
                "o":["right","left"]
            },
            {
                "q":f"How many countries are there in {continent}?",
                "a": len(countries),
                "o":[len(countries)-11,len(countries)+6,len(countries)]
            }
        ]
    
        question = random.choice(quiz)
        print(question.get("q")) # Imprimimos la pregunta

        answers = [answer for answer in question["o"]]
        random.shuffle(answers)
        for i,answer in enumerate(answers): # Imprimimos las respuestas posibles
            print(f"{i+1}. {answer}")
        print(" ")
        user = input(": ").lower()
        print(" ")

        if answers[int(user)-1] == question["a"]: # Comprobamos si está bien la respuesta
            print("Respuesta correcta")
            score += 1
        else:
            print("Respuesta incorrecta")
        print(separador)
        count += 1
    
    print(f"Has acertado {score}/5")