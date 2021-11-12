#Base de datos y funciones para la app de la librería

DB = [{
    "id": "cf_1",
    "title": "El hombre bicentenario",
    "author": "Isaac Asimov",
    "genre": "Ciencia ficción"
},
{
    "id": "ne_1",
    "title": "Lobo de mar",
    "author": "Jack London",
    "genre": "Narrativa extranjera"
},
{
    "id": "np_1",
    "title": "El legado de los huesos",
    "author": "Dolores Redondo",
    "genre": "Narrativa policíaca"
},
{
    "id": "dc_1",
    "title": "El error de Descartes",
    "author": "Antonio Damasio",
    "genre": "Divulgación científica"
},
{
    "id": "dc_2",
    "title": "El ingenio de los pájaros",
    "author": "Jennifer Ackerman",
    "genre": "Divulgación científica"
},
{
    "id": "ne_2",
    "title": "El corazón de las tinieblas",
    "author": "Joseph Conrad",
    "genre": "Narrativa extranjera"
},
{
    "id": "dc_5",
    "title": "Metro 2033",
    "author": "Dmitri Glujovski",
    "genre": "Divulgación científica"
},
{
    "id": "dc_6",
    "title": "Sidharta",
    "author": "Hermann Hesse",
    "genre": "Narrativa extranjera"
},
{
    "id": "el_1",
    "title": "Andres Trapiello",
    "author": "Las armas y las letras",
    "genre": "Narrativa extranjera"
},
{
    "id": "aa_1",
    "title": "El poder del ahora",
    "author": "Ekhart Tolle",
    "genre": "Narrativa extranjera"
},
]

genre = ["Narrativa extranjera", "Divulgación científica", "Narativa policíaca", "Ciencia ficción", "Autoayuda"]

user = "0"

#Funciones a utilizar

def menu():
    print("1. Buscar por id (ISBN)")
    print("2. Buscar por Título")
    print("3. Buscar por Autor")
    print("4. Buscar por Género")
    print("5. Actualizar libro")
    print("6. Quitar un libro")
    print("Q. Salir")

def pretty_book(book): #Imprimir más bonitos los libros
    for k,v in book.items():
        print(f"{k.capitalize()}: {v}")

def search_by_terms(term, term2search): #Encontrar el libro por el término seleccionado
    print(" ")
    print("LIBRO(S) ENCONTRADO(S)")
    for book in DB:
        if book[term].find(term2search) >= 0:
            print(" ")
            pretty_book(book)
            print(" ")
            with open("./History.txt", mode="a") as file: #añadimos el libro encontrado al historial
                file.write(f"El {term} buscado ha sido '{term2search}' con este resultado:\n {book}\n")
    

def look_for_id(bookid):
    for book in DB:
        if book["id"] == bookid:
            return book

def update_book(book):
    for k,v in list(book.items())[1:]:
        new_book = input(f"{k.capitalize()}: ")
        if new_book:
            book[k] = new_book

def remove_book(book):
    DB.remove(book)

def remove_menu():
    print("1. Continuar con el libro seleccionado")
    print("2. Detener acción y volver al menú principal")
