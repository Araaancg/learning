import requests as req
import random

# Quiz aquí para que sea más manejable

# Nos dan el continente, el nombre

'''
Salen 10 preguntas en total
Damos opciones
¿Cuál es la capital de {country}?
¿País más pequeño del {continente}?
¿País más grande del continente?
¿En qué lado conducen en {country}
'''
# Continentes: Africa, Asia, Americas, Oceania, Europa
#Hacemos request para traernos de primeras la api del continente, lo hacemos filtrando la info que necesitamos
continent = "Europe"
url = "https://restcountries.com/v3.1/region/"
res = req.get(url+continent).json()
countries = list(map(lambda country: {
    "name":country["name"]["common"],
    "capital":country["capital"][0],
    "area":country["area"],
    "drive_side":country["car"]["side"]
},res))
# print(countries)

right_answers = {
    "question 1":"b"
}
q_count = 1
score = 0

while q_count <= 1:
    print(f"Pregunta {q_count}") # Ponemos el número de pregunta para que el user sepa cuantas lleva
    ch_co = random.choice(countries) # Se reinicia la chosen country
    quiz = [
        {
            "n":"question 1",
            "QUESTION":f"Capital de {ch_co['name']}",
            "a":random.choice(countries)['capital'],
            "b":ch_co['capital'],
            "c":random.choice(countries)["capital"]
        }
    ]  
    ch_q = random.choice(quiz) #Se reinicia la pregunta elegida
    for k,v in ch_q.items():
        if k == "n":
            pass
        else:
            print(f"{k}: {v}")
    user = input("Respuesta: ").lower()
    if user == right_answers[ch_q["n"]]:
        print("Respuesta correcta")
        score += 1
    else:
        print("Respuesta incorrecta")
    print(f"Score: {score}")
    q_count += 1
    user = input(":")






'''
Respuestas correctas
1 b
'''