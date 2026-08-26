import AFD
salida = False
historial = []
afd = AFD.AFD()
print("Bienvenido al sistema de validacion y simulacion de Automatas finitos deterministas")
while salida == False:
    print("=====================================================================================")
    opcion = input("""Seleccione una opción:
    1. Crear AFD manualmente
    2. Cargar AFD desde archivo .txt
    3. Mostrar definición formal del AFD
    4. Mostrar la tabla de transición
    5. Validar la estructura del autómata
    6. Evaluar una cadena
    7. Evaluar un archivo de cadenas
    8. Consultar el historial de evaluaciones
    9. Cargar o crear otro autómata
    10. Salir\n""")
    print("=====================================================================================")
    match opcion:
        case "1":
            afd.crear_manualmente()
        case "2":
            afd.crear_portxt()
        case "3":
            print("Hola")
        case "4":
            print("Hola")
        case "5":
            print("Hola")
        case "6":
            print("Hola")
        case "7":
            print("Hola")
        case "8":
            print("Hola")
        case "9":
            print("Hola")
        case "10":
            print("Saliendo del programa...")
            salida = True
        case _:
            print("Opción invalida, intente nuevamente")