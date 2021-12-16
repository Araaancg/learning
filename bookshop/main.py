#programa de la librería

import test as bs

db = []
bs.csv_to_dict(db)

user = "0"
options = ["1","2","3","4","5","6","7","8","q"]

while user.lower() != "q":
    print("-"*50)
    print("LIBRERÍA".center(50))
    bs.menu()
    user = input("Escriba su opción: ").lower()
    print("-"*50)
    genre_list = bs.generar_lista("genre",db)
    if user in options:
        if user == "1":
            user = input("Introduzca id: ")
            book = bs.get_by_term("id",user, db)
            if book:
                bs.pretty_search_book(book)
                bs.history(book)
            else:
                print("No hemos encontrado ninguna coincidencia en nuestra base de datos")
            input("Presione enter para volver al menu")
            
        elif user == "2":
            user = input("Introduzca título: ").lower()
            book = bs.get_by_term("title", user, db)
            if book:
                bs.pretty_search_book(book)
                bs.history(book)
            else:
                print("No hemos encontrado ninguna coincidencia en nuestra base de datos")
            input("Presione enter para volver al menu")
        
        elif user == "3":
            user = input("Introduzca autor: ").lower()
            book = bs.get_by_term("author", user, db)
            if book:
                bs.pretty_search_book(book)
                bs.history(book)
            else:
                print("No hemos encontrado ninguna coincidencia en nuestra base de datos")
            input("Presione enter para volver al menu")
        
        elif user == "4":
            user = "0"
            genre_list = bs.generar_lista("genre",db)
            for i, genre in enumerate(genre_list):
                print(f"{i+1}: {genre}")
            user = input(": ")
            choosen_genre = genre_list[int(user)-1]
            book = bs.get_by_term("genre", choosen_genre, db)
            bs.pretty_search_book(book)
            bs.history(book)
            input("Presione enter para volver al menu")

        elif user == "5":
            user = input("Introduzca id:" ).lower()
            book = bs.get_by_term("id", user, db)
            if book:
                print("-"*50)
                print("Libro a modificar")
                bs.pretty_book(book)
                print("-"*50)
                bs.update_book(book)
                print("-"*50)
                print("El libro modificado:")
                bs.pretty_book(book)
            else:
                print("No hemos encontrado ninguna coincidencia en nuestra base de datos")
            input("Presione enter para volver al menu")

        elif user == "6":
            user = input("Introduzca id: ").lower()
            book = bs.get_by_term("id", user, db)
            if book:
                print("Libro a eliminar")
                bs.pretty_book(book)
                user = "0"
                bs.menu_remove()
                while user != "3": #Terminar acción
                    user = input(":" )
                    if user == "2": #Elegir otro libro
                        user = input("Introduzca id: ")
                        book = bs.get_by_term("id", user)
                        print("Libro a eliminar")
                        bs.pretty_book(book)
                        user = "0"
                        bs.menu_remove()
                    if user == "1": #Eliminar libro
                        bs.remove_book(book[0], db)
                        user = "3"
            else:
                print("No hemos encontrado ninguna coincidencia en nuestra base de datos")
            input("Presione enter para volver al menu")

        elif user == "7":
            new_book = {}
            bs.add_book(new_book, db,genre_list)
            bs.pretty_book(new_book)
            input("Presione enter para volver al menu")

        elif user == "8":
            print("-"*50)
            bs.pretty_book(db)
            print("-"*50)
            input("Presione enter para volver al menu")

        elif user.lower() == "q":             # Mensaje final programa y guardar los cambios
            user = input("¿Desea guardar los cambios? (y/n): ").lower()
            while user != "n":    
                if user == "y":
                    bs.export_db(db, "data.csv")
                    print("Cambios guardados")
                    user = "n"
                else:
                    user = input("Opción inexistente, por favor elija de nuevo (y/n): ")
            
            print("¡Hasta pronto!")
            user = "q"
    else:
        print("Número no válido")


