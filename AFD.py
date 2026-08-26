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
        for estado in self.estados:
            self.transiciones[estado] = {}
            for simbolo in self.alfabeto:
                siguiente = input(f"Transición para delta({estado}, {simbolo}): ").strip()
                if siguiente != "":
                    self.transiciones[estado][simbolo] = siguiente
        
    def crear_portxt(self):
        ruta = filedialog.askopenfilename()
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            self.nombre = lineas[0].strip().split("=")[1]
            self.estados = set(lineas[1].strip().split("=")[1].split(","))
            self.alfabeto = set(lineas[2].strip().split("=")[1].split(","))
            self.inicial = lineas[3].strip().split("=")[1]
            self.finales = set(lineas[4].strip().split("=")[1].split(","))
            
            
    def definicion(self):
        print("Estados del autómata: ")
        for estado in self.estados:
            print(f" {estado}")
        print("Alfabeto del autómata: ")
        for caracter in self.alfabeto:
            print(f" {caracter}")
        print("Función de transiciones: ")
        