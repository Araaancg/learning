import requests as req
import random

# Quiz aquí para que sea más manejable

# Nos dan el continente, el nombre
# Continentes: Africa, Asia, Americas, Oceania, Europa
#Hacemos request para traernos de primeras la api del continente, lo hacemos filtrando la info que necesitamos
continent = "Europe"
url = "https://restcountries.com/v3.1/region/"
res = req.get(url+continent).json()
countries = list(map(lambda country: {
    "name":country["name"]["common"],
    "capital":country["capital"][0],
    "area":country["area"],
    "drive_side":country["car"]["side"],
    "population":country["population"]
},res))

count = 1
score = 0

'''
        Salen 10 preguntas en total
        Damos opciones
        ¿Cuál es la capital de {country}?
        ¿Población aproximada de {country}?
        ¿País más pequeño del {continente}?
        ¿País más grande del continente?
        ¿En qué lado conducen en {country}
        '''



while count <= 5:
    print(f"Pregunta {count}") # Ponemos el número de pregunta para que el user sepa cuantas lleva
    ch_co = random.choice(countries) # Se reinicia la chosen country
    quiz = [
        {
            "q":f"Capital de {ch_co['name']}",
            "a":ch_co['capital'],
            "o":[random.choice(countries)['capital'], random.choice(countries)['capital'],ch_co['capital']]
        },
        {
            "q":f"Población de {ch_co['name']}",
            "a":ch_co['population'],
            "o":[random.choice(countries)['population'], random.choice(countries)['population'],ch_co['population']]
        }
    ]

    question = random.choice(quiz)
    print(question.get("q"))

    answers = [answer for answer in question["o"]]
    print(answers)
    random.shuffle(answers)
    print(answers)

    for i,answer in enumerate(answers):
        print(f"{i+1}. {answer}")
    user = input(": ").lower()
    if question["o"][int(user)-1] == question["a"]:
        print("Respuesta correcta")
        score += 1
    else:
        print("Respuesta incorrecta")

    count += 1
