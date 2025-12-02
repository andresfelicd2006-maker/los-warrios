import random

class PalabraJuego:
    def __init__(self):
        # Palabras ampliadas para mayor variedad
        self.palabras = [
            "computador", "programacion", "python", "pantalla", "teclado",
            "ventana", "interfaz", "algoritmo", "variable", "funcion",
            "clase", "objeto", "herencia", "polimorfismo", "encapsulamiento",
            "desarrollo", "software", "hardware", "memoria", "procesador",
            "internet", "navegador", "aplicacion", "sistema", "archivo",
            "carpeta", "documento", "proyecto", "codigo", "lenguaje"
        ]
        self.seleccionar_palabra()
        self.letras_usadas = []
        self.intentos_maximos = 6
        self.intentos = self.intentos_maximos

    def seleccionar_palabra(self):
        """Selecciona una nueva palabra aleatoria"""
        self.palabra = random.choice(self.palabras).upper()
        self.progreso = ["_"] * len(self.palabra)
        self.letras_usadas = []
        self.intentos = self.intentos_maximos

    def comprobar_letra(self, letra):
        """
        Comprueba si la letra está en la palabra
        Retorna: (acierto, mensaje, es_ganador)
        """
        letra = letra.upper()
        
        # Validaciones
        if len(letra) != 1 or not letra.isalpha():
            return False, "Ingresa solo UNA letra", False
        
        if letra in self.letras_usadas:
            return False, f"'{letra}' ya fue usada", False
        
        # Agregar a letras usadas
        self.letras_usadas.append(letra)
        
        # Verificar si está en la palabra
        acierto = False
        for i, char in enumerate(self.palabra):
            if char == letra:
                self.progreso[i] = letra
                acierto = True
        
        # Verificar si ganó
        es_ganador = "_" not in self.progreso
        
        if acierto:
            mensaje = f"¡Correcto! '{letra}' está en la palabra"
            return True, mensaje, es_ganador
        else:
            self.intentos -= 1
            mensaje = f"'{letra}' no está en la palabra"
            es_perdedor = self.intentos == 0
            return False, mensaje, es_ganador

    def mostrar_progreso(self, con_espacios=True):
        """Retorna el progreso actual formateado"""
        if con_espacios:
            return "  ".join(self.progreso)
        return " ".join(self.progreso)

    def esta_completa(self):
        """Verifica si la palabra ha sido completada"""
        return "_" not in self.progreso
    
    def get_letras_usadas(self):
        """Retorna las letras usadas formateadas"""
        return ", ".join(self.letras_usadas) if self.letras_usadas else "Ninguna"
    
    def get_intentos_restantes(self):
        """Retorna los intentos restantes"""
        return self.intentos
    
    def get_intentos_totales(self):
        """Retorna el total de intentos"""
        return self.intentos_maximos
    
    def get_palabra(self):
        """Retorna la palabra secreta"""
        return self.palabra
    
    def get_longitud(self):
        """Retorna la longitud de la palabra"""
        return len(self.palabra)
    
    def get_progreso_porcentaje(self):
        """Retorna el porcentaje de avance"""
        letras_adivinadas = sum(1 for letra in self.progreso if letra != "_")
        return int((letras_adivinadas / len(self.palabra)) * 100)