import random

class PalabraJuego:
    def __init__(self):
        self.palabras = ["computador", "programacion", "python", "pantalla", "teclado"]
        self.seleccionar_palabra()

    def seleccionar_palabra(self):
        self.palabra = random.choice(self.palabras)
        self.progreso = ["_"] * len(self.palabra)

    def comprobar_letra(self, letra):
        acierto = False
        for i, char in enumerate(self.palabra):
            if char == letra:
                self.progreso[i] = letra
                acierto = True
        return acierto

    def mostrar_progreso(self):
        return " ".join(self.progreso)

    def esta_completa(self):
        return "_" not in self.progreso
