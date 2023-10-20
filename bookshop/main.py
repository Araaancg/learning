#programa de la librería

from b_funcs import *

db = []
csv_to_dict(db)

user = "0"
options = ["1","2","3","4","5","6","7","8","q"]

while user.lower() != "q":
    print("-"*50)
    print("LIBRERÍA".center(50))
    menu()
    user = input("Escriba su opción: ").lower()
    print("-"*50)
    genre_list = generar_lista("genre",db)

    if user in options:
        if user == "1":
            user = input("Introduzca id: ")
            book = get_by_term("id",user, db)
            if book:
                pretty_search_book(book)
                history(book, "Search")
            else:
                print("\nNo hemos encontrado ninguna coincidencia en nuestra base de datos\n")
            input("Presione enter para volver al menu")
            
        elif user == "2":
            user = input("Introduzca título: ").lower()
            book = get_by_term("title", user, db)
            if book:
                pretty_search_book(book)
                history(book, "Search")
            else:
                print("\nNo hemos encontrado ninguna coincidencia en nuestra base de datos\n")
            input("Presione enter para volver al menu")
        
        elif user == "3":
            user = input("Introduzca autor: ").lower()
            book = get_by_term("author", user, db)
            if book:
                pretty_search_book(book)
                history(book, "Search")
            else:
                print("\nNo hemos encontrado ninguna coincidencia en nuestra base de datos\n")
            input("Presione enter para volver al menu")
        
        elif user == "4":
            user = "0"
            genre_list = generar_lista("genre",db)
            for i, genre in enumerate(genre_list):
                print(f"{i+1}: {genre}")
            user = input(": ")
            if int(user) in [num for num in range(1,len(genre_list))]:
                choosen_genre = genre_list[int(user)-1]
                book = get_by_term("genre", choosen_genre, db)
                pretty_search_book(book)
                history(book, "Search")
            else:
                print("Input no válido")
                print("-"*50)
            input("Presione enter para volver al menu")

        elif user == "5":
            user = input("Introduzca id: " ).lower()
            book = get_by_term("id", user, db)
            if book:
                print("-"*50)
                print("LIBRO A MODIFICAR\n")
                pretty_book(book)
                print("-"*50)
                update_book(book,genre_list)
                print("-"*50)
                print("LIBRO MODIFICADO\n")
                pretty_book(book)
                history(book, "Update")
            else:
                print("\nNo hemos encontrado ninguna coincidencia en nuestra base de datos\n")
            input("Presione enter para volver al menu")

        elif user == "6":
            user = input("Introduzca id: ").lower()
            print("-"*50)
            book = get_by_term("id", user, db)
            if book:
                print("LIBRO A ELIMINAR\n")
                pretty_book(book)
                print(" ")
                user = "0"
                menu_remove()
                print("-"*50)
                while user != "3": #Terminar acción
                    user = input(": ")
                    if user == "2": #Elegir otro libro
                        user = input("Introduzca id: ")
                        book = get_by_term("id", user)
                        print("LIBRO A ELIMINAR\n")
                        pretty_book(book)
                        user = "0"
                        menu_remove()
                    if user == "1": #Eliminar libro
                        history(book, "Removal") 
                        remove_book(book[0], db)
                        print("-"*50)
                        print("Libro eliminado correctamente")
                        print("-"*50)
                        user = "3"
            else:
                print("\nNo hemos encontrado ninguna coincidencia en nuestra base de datos\n")
            input("Presione enter para volver al menu")

        elif user == "7":
            new_book = [add_book(db,genre_list)]
            history(new_book, "Insertion")
            print(" ")
            pretty_book(new_book)
            input("\nPresione enter para volver al menu")

        elif user == "8":
            pretty_book(db)
            print("-"*50)
            input("Presione enter para volver al menu")

        elif user.lower() == "q":   # Mensaje final programa y guardar los cambios
            user = input("¿Desea guardar los cambios? (y/n): ").lower()
            while user != "n":    
                if user == "y":
                    export_db(db, "data.csv")
                    print("Cambios guardados")
                    user = "n"
                else:
                    user = input("Opción inexistente, por favor elija de nuevo (y/n): ")
            
            print("¡Hasta pronto!")
            user = "q"
    else:
        print("Número no válido")


