import random

class PalabraJuego:
    def __init__(self):
        self.palabras = [
            "computador", "programacion", "python", "pantalla", "teclado",
            "ventana", "interfaz", "algoritmo", "variable", "funcion",
            "clase", "objeto", "herencia", "polimorfismo", "encapsulamiento"
        ]
        self.seleccionar_palabra()
    
    def seleccionar_palabra(self):
        self.palabra = random.choice(self.palabras).upper()
        self.progreso = ["_"] * len(self.palabra)