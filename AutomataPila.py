import tkinter as tk
from tkinter import filedialog
from collections import deque

class AutomataPila:
    def __init__(self):
        self.nombre = ""
        self.tipo = ""  
        self.estados = set()
        self.alfabeto = set()
        self.alfabeto_pila = set()
        self.inicial = ""
        self.inicial_pila = ""
        self.finales = set()
        self.transiciones = {}
        self.historial_evaluaciones = []

    def crear_manualmente(self):
        print("\n--- Creación de Autómata de Pila Manual ---")
        
        self.nombre = input("Ingrese el nombre o identificador del autómata: ").strip()
        
        while True:
            self.tipo = input("Ingrese el tipo de autómata (APD / APND): ").strip().upper()
            if self.tipo in ["APD", "APND"]:
                break
            print("Tipo inválido. Debe ingresar 'APD' o 'APND'.")
            
        estados_str = input("Ingrese los estados separados por coma (ej. q0,q1,q2): ").strip()
        self.estados = set(estados_str.split(','))
        
        alfabeto_str = input("Ingrese el alfabeto de entrada separado por coma (ej. a,b): ").strip()
        self.alfabeto = set(alfabeto_str.split(','))
        
        alfabeto_pila_str = input("Ingrese el alfabeto de la pila separado por coma (ej. Z0,A,B): ").strip()
        self.alfabeto_pila = set(alfabeto_pila_str.split(','))
        
        self.inicial = input("Ingrese el estado inicial (ej. q0): ").strip()
        self.inicial_pila = input("Ingrese el símbolo inicial de la pila (ej. Z0): ").strip()
        
        finales_str = input("Ingrese los estados finales separados por coma (ej. q2,q3): ").strip()
        self.finales = set(finales_str.split(','))
        for estado in self.estados:
            self.transiciones[estado] = {}
            for simbolo in self.alfabeto | {"EPS"}:
                self.transiciones[estado][simbolo] = {}
                for tope in self.alfabeto_pila:
                    self.transiciones[estado][simbolo][tope] = []
                    
        print("\n--- Ingreso de Transiciones ---")
        print("NOTA: Formato de ingreso para destinos: estadoDestino,reemplazoPila")
        print("NOTA: Para múltiples destinos sepárelos con '|' (ej. q0,A;Z0|q1,EPS)")
        print("NOTA: Si no hay transición, simplemente presione Enter.")
        
        for estado in sorted(self.estados):
            for simbolo in sorted(list(self.alfabeto) + ["EPS"]):
                for tope in sorted(self.alfabeto_pila):
                    destinos_input = input(f"Transiciones para delta({estado}, {simbolo}, tope {tope}): ").strip()
                    
                    if destinos_input:
                        destinos_raw = destinos_input.split("|")
                        for dest in destinos_raw:
                            try:
                                subpartes = dest.split(",")
                                estado_dest = subpartes[0].strip()
                                reemplazo = subpartes[1].strip()
                                self.transiciones[estado][simbolo][tope].append((estado_dest, reemplazo))
                            except IndexError:
                                print(f"Error de formato al ingresar: '{dest}'. Se ignorará esta transición.")
                                
        self.validar_automata()

    def cargar_portxt(self):
        ruta = filedialog.askopenfilename()
        if not ruta:
            return
        
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = [linea.strip() for linea in archivo if linea.strip()]
            
            self.nombre = lineas[0].split("=")[1].strip()
            self.tipo = lineas[1].split("=")[1].strip()
            self.estados = set(lineas[2].split("=")[1].split(","))
            self.alfabeto = set(lineas[3].split("=")[1].split(","))
            self.alfabeto_pila = set(lineas[4].split("=")[1].split(","))
            self.inicial = lineas[5].split("=")[1].strip()
            self.inicial_pila = lineas[6].split("=")[1].strip()
            self.finales = set(lineas[7].split("=")[1].split(","))
            
            for estado in self.estados:
                self.transiciones[estado] = {}
                for simbolo in self.alfabeto | {"EPS"}:
                    self.transiciones[estado][simbolo] = {}
                    for tope in self.alfabeto_pila:
                        self.transiciones[estado][simbolo][tope] = []
            
            if lineas[8] == "TRANSICIONES:":
                for linea in lineas[9:]:
                    partes = linea.split(",")
                    origen = partes[0].strip()
                    simbolo = partes[1].strip()
                    tope = partes[2].strip()
                    
                    destinos_raw = ",".join(partes[3:]).split("|")
                    for dest in destinos_raw:
                        subpartes = dest.split(",")
                        estado_dest = subpartes[0].strip()
                        reemplazo = subpartes[1].strip()
                        
                        self.transiciones[origen][simbolo].setdefault(tope, []).append((estado_dest, reemplazo))
        
        self.validar_automata()

    def validar_automata(self):
        print(f"\n--- Validando {self.tipo}: {self.nombre} ---")
        errores = []
        
        if "EPS" in self.alfabeto or "EPS" in self.alfabeto_pila:
            errores.append("EPS no puede declararse como elemento de ALFABETO ni de ALFABETO_PILA.")
            
        if self.tipo == "APD":
            for estado in self.estados:
                for tope in self.alfabeto_pila:
                    for simbolo in self.alfabeto | {"EPS"}:
                        if len(self.transiciones.get(estado, {}).get(simbolo, {}).get(tope, [])) > 1:
                            errores.append(f"Conflicto APD: Transición ({estado}, {simbolo}, {tope}) tiene más de un destino.")
                    
                    trans_eps = self.transiciones.get(estado, {}).get("EPS", {}).get(tope, [])
                    if trans_eps:
                        for simbolo in self.alfabeto:
                            if self.transiciones.get(estado, {}).get(simbolo, {}).get(tope, []):
                                errores.append(f"Conflicto APD: Transición EPS y transición con '{simbolo}' simultáneas en ({estado}, {tope}).")
        
        if errores:
            for error in errores:
                print(f"ERROR: {error}")
            print("Autómata inválido.")
        else:
            print("Autómata cargado y validado correctamente.")

    def mostrar_tabla(self):
        print(f"\n--- Tabla de Transición ({self.tipo}) ---")
        encabezados = sorted(list(self.alfabeto)) + ["EPS"]
        print(f"{'Estado':<10} | {'Tope':<10} | " + " | ".join([f"{simbolo:<25}" for simbolo in encabezados]))
        print("-" * (25 + 28 * len(encabezados)))
        
        for estado in sorted(self.estados):
            for tope in sorted(self.alfabeto_pila):
                fila_vacia = True
                celdas = []
                for simbolo in encabezados:
                    trans = self.transiciones.get(estado, {}).get(simbolo, {}).get(tope, [])
                    if trans:
                        fila_vacia = False
                        txt_trans = " | ".join([f"({d},{r})" for d, r in trans])
                        celdas.append(f"{txt_trans:<25}")
                    else:
                        celdas.append(f"{'Ø':<25}")
                
                if not fila_vacia:
                    print(f"{estado:<10} | {tope:<10} | " + " | ".join(celdas))

    def evaluar_cadena(self, cadena=None):
        if cadena is None:
            cadena = input("Ingrese una cadena (ej: ababa, abab, babab): ")
        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                print(f"Error: el símbolo {simbolo} no pertenece al alfabeto definido")
                return

        print(f"\n==== Ejecución: Simulando Cadena '{cadena}' en {self.tipo} ====")
        
        pila_inicial = [self.inicial_pila]
        cola = deque([(1, "1", self.inicial, cadena, pila_inicial, [], 0)])
        
        aceptada = False
        estado_aceptacion = "N/A"
        limite_pasos = 1000
        estados_visitados = set() 

        while cola:
            paso, rama_id, estado, restante, pila, traza, contador = cola.popleft()
            
            if contador > limite_pasos:
                continue
                
            configuracion_actual = (estado, restante, tuple(pila))
            if configuracion_actual in estados_visitados:
                continue
            estados_visitados.add(configuracion_actual)

            if len(restante) == 0 and estado in self.finales:
                aceptada = True
                estado_aceptacion = estado
                print(f"\n¡Cadena ACEPTADA")
                for linea in traza:
                    print(linea)
                break
                
            if not pila:
                continue
                
            tope_actual = pila[-1]
            trans_posibles = []
            
            if len(restante) > 0:
                simbolo = restante[0]
                for dest, reemplazo in self.transiciones.get(estado, {}).get(simbolo, {}).get(tope_actual, []):
                    trans_posibles.append((simbolo, restante[1:], dest, reemplazo))
                    
            for dest, reemplazo in self.transiciones.get(estado, {}).get("EPS", {}).get(tope_actual, []):
                trans_posibles.append(("EPS", restante, dest, reemplazo))
                
            for i, (simbolo_usado, nueva_entrada, dest, reemplazo) in enumerate(trans_posibles):
                nueva_pila = pila[:-1]
                
                if reemplazo != "EPS":
                    elementos_reemplazo = reemplazo.split(";")
                    nueva_pila.extend(reversed(elementos_reemplazo))
                    
                nuevo_registro = f"Paso {paso} Est: {estado} | Ent: {restante} | Pila_ant: {pila} | Lee: {simbolo_usado} | Desapila: {tope_actual} -> Est: {dest} | Apila: {reemplazo} | Pila_nuev: {nueva_pila}"
                
                cola.append((paso + 1, f"{rama_id}.{i+1}", dest, nueva_entrada, nueva_pila, traza + [nuevo_registro], contador + 1))
                
        if aceptada:
            veredicto = 'Aceptado'
        else:
            veredicto = 'Rechazado'
            print("\nCadena RECHAZADA.")

        print(f"Veredicto final: {veredicto}")

        self.historial_evaluaciones.append({
            "cadena": cadena,
            "estado_final": estado_aceptacion if aceptada else "N/A",
            "veredicto": veredicto
        })

    def evaluar_archivo_cadenas(self):
        ruta = filedialog.askopenfilename()
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()

                if not lineas:
                    print("El archivo está vacío")
                    return

                print(f"\nEvaluando {len(lineas)} cadenas del archivo...")

                for linea in lineas:
                    cadena_limpia = linea.strip()
                    print(f"\n == Evaluando cadena: {cadena_limpia}")
                    self.evaluar_cadena(cadena=cadena_limpia)

        except FileNotFoundError:
            print(f"Error: no se encontró el archivo en la ruta {ruta}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al leer el archivo: {e}")

    def consultar_historial(self):
        print("\n == Historial de evaluaciones ==")

        if not self.historial_evaluaciones:
            print("Aún no hay historial, vuelve pronto")
            return

        for indice, registro in enumerate(self.historial_evaluaciones, start=1):
            cad_formato = registro['cadena'] if registro['cadena'] != "" else "Vacía (Epsilon)"
            print(f"{indice}. Cadena: {cad_formato} | Estado final: {registro['estado_final']} | resultado: {registro['veredicto']}")