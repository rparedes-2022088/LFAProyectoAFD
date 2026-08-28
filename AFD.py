import tkinter as tk 
from tkinter import filedialog

class AFD:
    def __init__(self):
        self.nombre = ""
        self.estados = set()
        self.alfabeto = set()
        self.inicial = ""
        self.finales = set()
        self.transiciones = {}
        self.historial_evaluaciones = []

    def crear_manualmente(self):
        print("--- Creación de AFD Manual ---")
        self.nombre = input("Ingrese el nombre o identificador del autómata: ")
        estados_str = input("Ingrese los estados separados por coma (ej. q0,q1,q2): ")
        self.estados = set(estados_str.strip().split(','))
        
        alfabeto_str = input("Ingrese el alfabeto separado por coma (ej. a,b,c,d):")
        self.alfabeto = set(alfabeto_str.strip().split(','))
        self.inicial = input("Ingrese el estado inicial del autómata (ej. q0): ")
        finales_str = input("Ingrese los estados finales del autómata separados por coma (ej. q6,q7):")
        self.finales = set(finales_str.strip().split(','))
        print("\n--- Ingreso de Transiciones ---")
        print("NOTA: Si un estado no tiene transición con un símbolo, simplemente presione Enter (déjelo en blanco).")
        for estado in sorted(self.estados):
            self.transiciones[estado] = {}
            for simbolo in sorted(self.alfabeto):
                siguiente = input(f"Transición para delta({estado}, {simbolo}): ").strip()
                if siguiente != "":
                    self.transiciones[estado][simbolo] = siguiente
        
    def crear_portxt(self):
        ruta = filedialog.askopenfilename()
        if not ruta:
            return
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            self.nombre = lineas[0].strip().split("=")[1].strip()
            self.estados = set(lineas[1].strip().split("=")[1].split(","))
            self.alfabeto = set(lineas[2].strip().split("=")[1].split(","))
            self.inicial = lineas[3].strip().split("=")[1].strip()
            self.finales = set(lineas[4].strip().split("=")[1].split(","))
            
            self.transiciones = {}
            for estado in self.estados:
                self.transiciones[estado] = {}
                
            if lineas[5].strip() == "TRANSICIONES:":
                for linea in lineas[6:]:
                    linea = linea.strip()
                    if not linea:
                        continue
                    partes = linea.split(",")
                    
                    if len(partes) == 3:
                        origen = partes[0].strip()
                        simbolo = partes[1].strip()
                        destino = partes[2].strip()
                        
                        if origen in self.transiciones:
                            if simbolo in self.transiciones[origen]:
                                self.transiciones[origen][simbolo] += f",{destino}"
                            else:
                                self.transiciones[origen][simbolo] = destino
            
    def definicion(self):
        print("Estados del autómata: ")
        for estado in sorted(self.estados):
            print(f" {estado}")
        print("Alfabeto del autómata: ")
        for caracter in sorted(self.alfabeto):
            print(f" {caracter}")
        print("Funciones de transiciones: ")
        for estado_origen, transiciones_estado in sorted(self.transiciones.items()):
            for simbolo, estado_destino in sorted(transiciones_estado.items()):
                print(f"  d({estado_origen}, {simbolo}) = {estado_destino}")
        print(f"Estado inicial: {self.inicial}")
        print("Estados finales:")
        for final in sorted(self.finales):
                    print(f" {final}")
            
    def tabla_trans(self):
        print("\n==== Tabla de Transiciones ====")

        alfabeto_ordenado = sorted(self.alfabeto)
        estados_ordenados = sorted(self.estados)
        
        encabezado = f"{'Estado':<10}"
        for simbolo in alfabeto_ordenado:
            encabezado += f" | {simbolo:<8}"
            
        print(encabezado)
        print("-" * len(encabezado))
        
        for estado in estados_ordenados:
            marca = ""
            if estado == self.inicial and estado in self.finales:
                marca = "->* "
            elif estado == self.inicial:
                marca = "-> "
            elif estado in self.finales:
                marca = "* "
            else:
                marca = "    "
                
            nombre_estado = f"{marca}{estado}"
            fila = f"{nombre_estado:<10}"
            
            for simbolo in alfabeto_ordenado:
                destino = self.transiciones.get(estado, {}).get(simbolo, "-")
                fila += f" | {destino:<8}"
                
            print(fila)
    
    #Carga nuevo automata unicamente reemplaza los datos anteriores almacenados.
    
    def validar_automata(self):
        print("\n==== Validación Estructural del Autómata ====")
        es_valido = True
        es_afd = True
        if self.inicial not in self.estados:
            print(f"[Error] El estado inicial '{self.inicial}' no pertenece al conjunto de estados Q.")
            es_valido = False

        if not self.finales.issubset(self.estados):
            estados_invalidos = self.finales - self.estados
            print(f"[Error] Los estados finales {estados_invalidos} no pertenecen al conjunto de estados Q.")
            es_valido = False

        for estado in sorted(self.estados):
            for simbolo in sorted(self.alfabeto):
                destino = self.transiciones.get(estado, {}).get(simbolo, "")
                
                if destino == "":
                    print(f"[Alerta AFND] Falta transición para d({estado}, {simbolo}). Transición vacía.")
                    es_afd = False
                    es_valido = False
                    
                elif "," in destino:
                    print(f"[Alerta AFND] Múltiples destinos para d({estado}, {simbolo}) -> {destino}.")
                    es_afd = False
                    es_valido = False
                    
                elif destino not in self.estados:
                    print(f"[Error] El estado destino '{destino}' de d({estado}, {simbolo}) no pertenece a Q.")
                    es_valido = False

        print("-" * 50)
        if not es_afd:
            print("La estructura corresponde a un AFND, no a un AFD.")
        elif not es_valido:
            print("El autómata tiene errores de consistencia en su tupla.")
        else:
            print("¡Validación exitosa! El autómata es un AFD determinista y consistente.")
            
        return es_valido

    

    def evaluar_cadena(self, cadena = None):
        #Si no se envía una cadena desde el archivo se lo pide al usuario
        if cadena is None:
            cadena = input("Ingrese una cadena (ej: ababa, abab, babab)")

        #para validar que todos los símobolos pertenezcan al alfabeto
        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                print(f"Error: el símbolo {simbolo} no pertenece al alfabeto definido")
                return #detiene la evaluación sin colapsar el programa

        #comenzar en el orden definido (estado inicial)
        estado_actual = self.inicial

        print("\n==== Ejecución ====")

        #procesar los simbolos en el orden ingresado
        for simbolo in cadena:
            #aplicar la función de transición usando el diccionario
            siguiente_estado = self.transiciones.get(estado_actual, {}).get(simbolo)

            if siguiente_estado is None or siguiente_estado == "":
                print(f"Error: el autómata se atascó no nay transición para d({estado_actual}, {simbolo})")
                return

            print(f"Estado actual: {estado_actual} | Símbolo procesado: {simbolo} | Siguiente estado: {siguiente_estado}")

            estado_actual = siguiente_estado

        #deterinar el estado final e dinicar si fue aceptada o rechazada
        if estado_actual in self.finales:
            veredicto = 'Aceptado'
        else:
            veredicto = 'Rechazado'

        print(f"Veredicto final: {veredicto} (El autómata se detuvo en '{estado_actual}')")

        #guardar en el historial para la opción del historial
        self.historial_evaluaciones.append({
            "cadena":cadena,
            "estado_final":estado_actual,
            "veredicto":veredicto
        })

    def evaluar_archivo_cadenas(self):
        ruta = filedialog.askopenfilename()
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()

                if not lineas:
                    print("El archivo está vaío")
                    return

                print(f"\nEvaluando {len(lineas)} cadenas del archivo...")

                for linea in lineas:
                    #Quitar saltos de linea y espacios en blanco de los extremos
                    cadena_limpia = linea.strip()
                    print(f"\n == Evaluando cadena: {cadena_limpia}")
                    self.evaluar_cadena(cadena = cadena_limpia) #reutilizamos la función de la opción anterior

        except FileNotFoundError:
            print(f"Error: no se encontro el archivo en la ruta {ruta}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al leer el archivo: {e}")

    def consultar_historial(self):
        print("\n == Historial de evaluaciones ==")

        if not self.historial_evaluaciones:
            print("Aún no hay historial, vuelve pronto")
            return

        #recorrer e imprimir cada registro
        for indice, registro in enumerate(self.historial_evaluaciones, start=1):
            cad_formato = registro['cadena'] if registro['cadena'] != "" else "Vacía (Epsilon)"
            print(f"{indice}. Cadena: {cad_formato} | Estado final: {registro['estado_final']} | resultado: {registro['veredicto']}")
