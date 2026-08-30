import AFD
salida = False
caso = 0
historial = []
afd = AFD.AFD()
print("Bienvenido al sistema de validacion y simulacion de Automatas finitos deterministas")
while salida == False:
    if(caso == 0):
        print("=====================================================================================")
        opcion = input("""Seleccione una opción:
    1. Crear AFD manualmente
    2. Cargar AFD desde archivo .txt
    3. Salir\n""")
        print("=====================================================================================")
        match opcion:
            case "1":
                afd.crear_manualmente()
                caso = 1
            case "2":
                afd.crear_portxt()
                caso = 1
            case "3":
                print("Saliendo del programa...")
                salida = True
            case _:
                print("Opción invalida, intente nuevamente")
    elif(caso == 1):
        print("=====================================================================================")
        opcion = input("""Seleccione una opción:
    1. Mostrar definición formal del AFD
    2. Mostrar la tabla de transición
    3. Validar la estructura del autómata
    4. Evaluar una cadena
    5. Evaluar un archivo de cadenas
    6. Consultar el historial de evaluaciones
    7. Cargar o crear otro autómata
    8. Salir\n""")
        print("=====================================================================================")
        match opcion:
            case "1":
                afd.definicion()
            case "2":
                afd.tabla_trans()
            case "3":
                afd.validar_automata()
            case "4":
                afd.evaluar_cadena()
            case "5":
                afd.evaluar_archivo_cadenas()
            case "6":
                afd.consultar_historial()
            case "7":
                caso = 0
            case "8":
                print("Saliendo del programa...")
                salida = True
            case _:
                print("Opción invalida, intente nuevamente")