from functions import create_database, create_table, request, update_data, delete_data, validate_table, resumen, plot


def app():
    print("Bienvenido a la aplicación.")
    a = input("Ingrese el modo de ejecución, 1 para actualizar, 2 para visualizar: ")
    if a == "1":
        b = input("Ingrese el ticker: ")
        c = input("Ingrese la fecha de inicio en formato YYYY-MM-DD: ")
        d = input("Ingrese la fecha fin en formato YYYY-MM-DD: ")
        #Si la función request retorna un dict, se crea la tabla o se borran sus datos (si ya existe), y luego se actualizan.
        #Si retorna algún tipo de error, se muestra en pantalla.
        if isinstance(request(b, c, d), dict):
            validate_table(b)
            update_data(request(b, c, d))
        else:
            print(request(b, c, d))
    elif a == "2":
        e = input("Ingrese 1 para ver resumen, 2 para graficar: ")
        if e == "1":
            resumen()
            print("Gracias por su visita.")
        elif e == "2":
            b = input("Ingrese el ticker: ")
            plot(b)
            print("Gracias por su visita.")
        else:
            print("Ingrese un valor válido.")
    else:
        print("Ingrese un valor válido.")


app()
