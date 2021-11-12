#App de la librería, sin base de datos ni funciones que cogemos desde el fichero bookshop

import bookshop as bs

user = "0"

while user.lower() != "q":
    #Menú standard
    print("LIBRERÍA".center(30,"-"))
    bs.menu()
    user = input("Escriba su elección: ")

    #Búsqueda por número introducido
    if user == str(1): #Id
        enter_id = input("Escriba el id del libro: ").lower()
        bs.search_by_terms("id",enter_id)  

    elif user == str(2): #Título
        enter_title = input("Escribe el título del libro: ").capitalize()

        bs.search_by_terms("title", enter_title)

    elif user == str(3): #Autor
        enter_author = input("Escribe el autor del libro: ").title()
        bs.search_by_terms("author", enter_author)

    elif user == str(4): #Género
        print(f"Estos son los géneros disponibles: {bs.genre}")
        enter_genre = input("Escribe el género deseado: ").capitalize()
        bs.search_by_terms("genre", enter_genre)

    elif user == str(5):
        bookid_to_search = input("Introduzca el id del libro a modificar: ")
        print(" ")
        print("Libro a modificar:")
        print(" ")
        book_to_search = bs.look_for_id(bookid_to_search)
        bs.pretty_book(book_to_search)
        print(" ")
        print("Presione enter si no quiere modificar nada")
        bs.update_book(book_to_search)
        print(" ")
        print("Las modificaciones han quedado así:")
        print(" ")
        bs.pretty_book(book_to_search)
    
    elif user == str(6):
        bookid_to_remove = input("Introduzca el id del libro a eliminar: ")
        print(" ")
        print("Libro a eliminar: ")
        print(" ")
        book_to_remove = bs.look_for_id(bookid_to_remove)
        bs.pretty_book(book_to_remove)
        print(" ")
        print("¿Está seguro que quiere eliminar este libro de la base de datos?")
        bs.remove_menu()
        user = input("Escriba su elección: ")
        if user == str(1):
            bs.remove_book(book_to_remove)
            print(" ")
            print(bs.DB)
        elif user == str(2):
            pass

    else: #Función quit para terminar el programa
        if user.lower() == "q":
            print("¡Hasta pronto!")
        else:
            print("Número no válido")
    
    input("")
