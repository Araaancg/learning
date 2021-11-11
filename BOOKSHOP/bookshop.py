#Crear como una app de terminal en la que se pueda buscar por los diferentes libros en base a diferentes parámetros

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

def look_for_id(bookid):
    for book in DB:
        if book["id"] == bookid:
            return book

def update_book(book):
    for k,v in list(book.items())[1:]:
        new_book = input(f"{k}: ")
        if new_book:
            book[k] = new_book

def remove_book(book):
    DB.remove(book)

def remove_menu():
    print("1. Continuar con el libro seleccionado")
    print("2. Detener acción y volver al menú principal")


# while user.lower() != "q":
#     #Menú standard
#     print("LIBRERÍA".center(30,"-"))
#     menu()
#     user = input("Escriba su elección: ")

#     #Búsqueda por número introducido
#     if user == str(1): #Id
#         enter_id = input("Escriba el id del libro: ").lower()
#         search_by_terms("id",enter_id)  

#     elif user == str(2): #Título
#         enter_title = input("Escribe el título del libro: ").capitalize()

#         search_by_terms("title", enter_title)

#     elif user == str(3): #Autor
#         enter_author = input("Escribe el autor del libro: ").title()
#         search_by_terms("author", enter_author)

#     elif user == str(4): #Género
#         print(f"Estos son los géneros disponibles: {genre}")
#         enter_genre = input("Escribe el género deseado: ").capitalize()
#         search_by_terms("genre", enter_genre)

#     elif user == str(5):
#         bookid_to_search = input("Introduzca el id del libro a modificar: ")
#         print(" ")
#         print("Libro a modificar:")
#         print(" ")
#         book_to_search = look_for_id(bookid_to_search)
#         pretty_book(book_to_search)
#         print(" ")
#         print("Presione enter si no quiere modificar nada")
#         update_book(book_to_search)
#         print(" ")
#         print("Las modificaciones han quedado así:")
#         print(" ")
#         pretty_book(book_to_search)
    
#     elif user == str(6):
#         bookid_to_remove = input("Introduzca el id del libro a eliminar: ")
#         print(" ")
#         print("Libro a eliminar: ")
#         print(" ")
#         book_to_remove = look_for_id(bookid_to_remove)
#         pretty_book(book_to_remove)
#         print(" ")
#         print("¿Está seguro que quiere eliminar este libro de la base de datos?")
#         remove_menu()
#         user = input("Escriba su elección: ")
#         if user == str(1):
#             remove_book(book_to_remove)
#             print(" ")
#             print(DB)
#         elif user == str(2):
#             pass

#     else: #Función quit para terminar el programa
#         if user.lower() == "q":
#             print("¡Hasta pronto!")
#         else:
#             print("Número no válido")
    
#     input("")

    


