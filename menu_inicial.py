import tkinter as tk
from ventana_juego import VentanaJuego

class MenuInicial(tk.Tk):
    def __init__(self):
        super().__init__()

        # Ventana principal
        self.title("Menú Principal")
        self.ANCHO = 1024
        self.ALTO = 576

        # Centrar ventana
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (self.ANCHO // 2)
        y = (pantalla_alto // 2) - (self.ALTO // 2)

        self.geometry(f"{self.ANCHO}x{self.ALTO}+{x}+{y}")
        self.resizable(False, False)

        # Widgets
        label_titulo = tk.Label(self, text="Juego de Adivinar Palabras", font=("Arial", 30))
        label_titulo.pack(pady=40)

        btn_jugar = tk.Button(self, text="Jugar", font=("Arial", 22),
                              command=self.iniciar_juego)
        btn_jugar.pack(pady=10)

        btn_salir = tk.Button(self, text="Salir", font=("Arial", 22), command=self.quit)
        btn_salir.pack(pady=10)

    def iniciar_juego(self):
        VentanaJuego(self)   # 🔥 abrir como ventana hija sin cerrar el menú
