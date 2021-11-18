#programa de la librería

'''
Cuando le doy a enter cuando no he puesto nada me sale el db entero y se inicia la función de 
rescribir libros
arreglar lo de añadir géneros 
poner un historial
lo del input erróneo, mensaje de que input no existente en la db
poner las impresiones más bonitas
'''


import test as bs

db = []
bs.csv_to_dict(db)
# print(db)

user = "0"

while user.lower() != "q":
    print(" LIBRERÍA ".center(50, "_"))
    bs.menu()
    user = input(": ")

    if user == "1":
        user = input("Introduzca id: ")
        book = bs.get_by_term("id",user, db)
        bs.pretty_book(book)
        
    elif user == "2":
        user = input("Introduzca título: ")
        book = bs.get_by_term("title", user, db)
        bs.pretty_book(book)
    
    elif user == "3":
        user = input("Introduzca autor: ")
        book = bs.get_by_term("author", user, db)
        bs.pretty_book(book)
    
    elif user == "4":
        user = "0"
        for i, genre in enumerate(bs.genre_list):
            print(f"{i+1}: {genre}")
        user = input(": ")
        choosen_genre = bs.genre_list[int(user)-1]
        book = bs.get_by_term("genre", choosen_genre, db)
        bs.pretty_book(book)

    elif user == "5":
        user = input("Introduzca id:" )
        book = bs.get_by_term("id", user, db)
        print(f"Libro a modificar\n {book}")
        bs.update_book(book)
        print("El libro modificado:")
        bs.pretty_book(book)

    elif user == "6":
        user = input("Introduzca id: ")
        book = bs.get_by_term("id", user, db)
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

    elif user == "7":
        new_book = {}
        bs.add_book(new_book, db)
        bs.pretty_book(new_book)
        print(db)

    elif user == "8":
        bs.pretty_book(db)

    elif user.lower() == "q":
        user = input("¿Desea guardar los cambios? (y/n): ")
        while user != "n":    
            if user == "y":
                bs.export_db(db, "data.csv")
                print("Cambios guardados")
                user = "n"
            else:
                user = input("Opción inexistente, por favor elija de nuevo (y/n): ")
        
        print("Hasta pronto")
        user = "q"

    else:
        print("Opción inexistente, por favor elija de nuevo: ")


