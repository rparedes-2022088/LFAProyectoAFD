import AFD
import afnd
salida = False
esAfnd = False
caso = 0
historial = []
afd = AFD.AFD()
afnd = afnd.AFND()
print("Bienvenido al sistema de validacion y simulacion de Automatas finitos deterministas")
while salida == False:
    #se mantiene con las primeras 3 opciones hasta que se ingrese un autómata para evaluar
    if(caso == 0):
        print("=====================================================================================")
        opcion = input("""Seleccione una opción:
    1. Crear AFD manualmente
    2. Cargar AFD desde archivo .txt
    3. Crear AFND manualmente
    4. Cargar AFND desde archivo .txt
    5. Salir\n""")
        print("=====================================================================================")
        match opcion:
            case "1":
                afd.crear_manualmente()
                caso = 1
            case "2":
                afd.crear_portxt()
                caso = 1
            case "3":
                afnd.crear_manualmente()
                esAfnd = True
                caso = 1
            case "4":
                afnd.cargar_portxt()
                esAfnd = True
                caso = 1
            case "5":
                print("Saliendo del programa...")
                salida = True
            case _:
                print("Opción invalida, intente nuevamente")
    #avanza a las demás opciones si es que ya hay un autómata cargado
    elif(caso == 1):
        if esAfnd: 
            print("=====================================================================================")
            opcion = input("""Seleccione una opción:
            1. Mostrar definición formal del AFD
            2. Mostrar la tabla de transición
            3. Validar la estructura del autómata
            4. Convertir AFND cargado a AFD equivalente
            5. Evaluar una cadena
            6. Evaluar un archivo de cadenas
            7. Consultar el historial de evaluaciones
            8. Cargar o crear otro autómata
            9. Salir\n""")
            print("=====================================================================================")
            match opcion:
                case "1":
                    if esAfnd:
                        print("Convierte primero el AFND a un AFD")
                    else:
                        afd.definicion()
                case "2":
                    if esAfnd:
                        print("Convierte primero el AFND a un AFD")
                    else:
                        afd.tabla_trans()
                case "3":
                    if esAfnd:
                        print("Convierte primero el AFND a un AFD")
                    else:
                        afd.validar_automata()
                case "4":
                    afd = afnd.convertir_a_afd()
                    esAfnd = False
                case "5":
                    if esAfnd:
                        print("Convierte primero el AFND a un AFD")
                    else:
                        afd.evaluar_cadena()
                case "6":
                    if esAfnd:
                        print("Convierte primero el AFND a un AFD")
                    else:
                        afd.evaluar_archivo_cadenas()
                case "7":
                    if esAfnd:
                        print("Convierte primero el AFND a un AFD")
                    else:
                        afd.consultar_historial()
                case "8":
                    caso = 0
                    #regresa al caso 0 para poder cargar uno nuevo
                case "9":
                    print("Saliendo del programa...")
                    salida = True
                case _:
                    print("Opción invalida, intente nuevamente")
        else:
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
                    if esAfnd:
                        print("Convierte primero el AFND a un AFD")
                    else:
                        afd.definicion()
                case "2":
                    if esAfnd:
                        print("Convierte primero el AFND a un AFD")
                    else:
                        afd.tabla_trans()
                case "3":
                    if esAfnd:
                        print("Convierte primero el AFND a un AFD")
                    else:
                        afd.validar_automata()
                case "4":
                    if esAfnd:
                        print("Convierte primero el AFND a un AFD")
                    else:
                        afd.evaluar_cadena()
                case "5":
                    if esAfnd:
                        print("Convierte primero el AFND a un AFD")
                    else:
                        afd.evaluar_archivo_cadenas()
                case "6":
                    if esAfnd:
                        print("Convierte primero el AFND a un AFD")
                    else:
                        afd.consultar_historial()
                case "7":
                    caso = 0
                    #regresa al caso 0 para poder cargar uno nuevo
                case "8":
                    print("Saliendo del programa...")
                    salida = True
                case _:
                    print("Opción invalida, intente nuevamente")
