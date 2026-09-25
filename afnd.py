import tkinter as tk
from tkinter import filedialog
import AFD

class AFND:
    def __init__(self):
        self.nombre = ""
        self.estados = set()
        self.alfabeto = set()
        self.inicial = ""
        self.finales = set()
        self.transiciones = {}

    def crear_manualmente(self):
        print("--- Creación de AFND Manual ---")
        self.nombre = input("Ingrese el nombre o identificador del autómata: ")
        estados_str = input("Ingrese los estados separados por coma (ej. q0,q1,q2): ")
        self.estados = set(estados_str.strip().split(','))
        
        alfabeto_str = input("Ingrese el alfabeto separado por coma (ej. a,b,c,d): ")
        self.alfabeto = set(alfabeto_str.strip().split(','))
        self.inicial = input("Ingrese el estado inicial del autómata (ej. q0): ")
        finales_str = input("Ingrese los estados finales del autómata separados por coma (ej. q6,q7): ")
        self.finales = set(finales_str.strip().split(','))
        
        print("\n--- Ingreso de Transiciones ---")
        print("NOTA: Ingrese los múltiples destinos separados por coma (ej. q0,q1).")
        print("NOTA: Si no hay transición (conjunto vacío), presione Enter o ingrese Ø.")
        
        for estado in sorted(self.estados):
            self.transiciones[estado] = {}
            for simbolo in sorted(self.alfabeto):
                siguientes = input(f"Transiciones para delta({estado}, {simbolo}): ").strip()
                
                if siguientes == "" or siguientes == "Ø":
                    self.transiciones[estado][simbolo] = set()
                else:
                    self.transiciones[estado][simbolo] = set(siguientes.split(","))

    def cargar_portxt(self):
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
                        destinos_o = partes[2].strip()
                        
                        if destinos_o == "Ø" or destinos_o == "":
                            destinos = set()
                        else:
                            destinos = set(destinos_o.split("|"))
                            
                        self.transiciones[origen][simbolo] = destinos

    def convertir_a_afd(self):
        print("\n--- Iniciando conversión de AFND a AFD ---")
        
        nuevo_afd = AFD.AFD()
        nuevo_afd.nombre = f"AFD_eq_{self.nombre}"
        nuevo_afd.alfabeto = self.alfabeto.copy()
        
        macroestado_inicial = frozenset([self.inicial])
        macroestados_pendientes = [macroestado_inicial]
        
        mapa_macroestados = {macroestado_inicial: "A"} 
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        contador_nombres = 1
        
        while macroestados_pendientes:
            estado_actual_conjunto = macroestados_pendientes.pop(0)
            nombre_estado_actual = mapa_macroestados[estado_actual_conjunto]
            
            nuevo_afd.estados.add(nombre_estado_actual)
            nuevo_afd.transiciones[nombre_estado_actual] = {}
            
            for simbolo in self.alfabeto:
                destinos_alcanzados = set()
                
                for sub_estado in estado_actual_conjunto:
                    if sub_estado in self.transiciones and simbolo in self.transiciones[sub_estado]:
                        destinos_alcanzados.update(self.transiciones[sub_estado][simbolo])
                
                destinos_alcanzados_frozen = frozenset(destinos_alcanzados)
                
                if not destinos_alcanzados_frozen:
                    nombre_destino = "Ø"
                    if frozenset() not in mapa_macroestados: 
                         mapa_macroestados[frozenset()] = "Ø"
                         macroestados_pendientes.append(frozenset())
                else:
                    if destinos_alcanzados_frozen not in mapa_macroestados:
                        nuevo_nombre = letras[contador_nombres]
                        mapa_macroestados[destinos_alcanzados_frozen] = nuevo_nombre
                        contador_nombres += 1
                        macroestados_pendientes.append(destinos_alcanzados_frozen)
                    
                    nombre_destino = mapa_macroestados[destinos_alcanzados_frozen]
                
                nuevo_afd.transiciones[nombre_estado_actual][simbolo] = nombre_destino

        nuevo_afd.inicial = "A"
        
        for conjunto, nombre in mapa_macroestados.items():
            if not conjunto:
                continue
            if not conjunto.isdisjoint(self.finales):
                nuevo_afd.finales.add(nombre)
        
        print("\n==== Tabla de Equivalencias de Macroestados ====")
        print(f"{'Macroestado del AFD':<25} | {'Conjunto de estados del AFND'}")
        for conjunto, nombre in mapa_macroestados.items():
            estados_str = "{" + ", ".join(sorted(list(conjunto))) + "}" if conjunto else "Ø"
            print(f"{nombre:<25} | {estados_str}")
            
        return nuevo_afd