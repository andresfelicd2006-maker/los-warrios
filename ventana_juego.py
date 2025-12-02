import tkinter as tk
import random

class VentanaJuego(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Configuración ventana
        self.ANCHO = 1024
        self.ALTO = 576

        self.title("Juego de Adivinar Palabras")

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (self.ANCHO // 2)
        y = (pantalla_alto // 2) - (self.ALTO // 2)

        self.geometry(f"{self.ANCHO}x{self.ALTO}+{x}+{y}")
        self.resizable(False, False)

        # Palabras
        self.PALABRAS = ["python", "programa", "juego", "computador", "teclado", "pantalla"]

        # UI
        self.lbl_titulo = tk.Label(self, text="Adivina la Palabra", font=("Arial", 30))
        self.lbl_titulo.pack(pady=20)

        self.lbl_palabra = tk.Label(self, text="", font=("Arial", 34))
        self.lbl_palabra.pack(pady=10)

        self.entry_letra = tk.Entry(self, font=("Arial", 24), width=5)
        self.entry_letra.pack()

        self.btn_verificar = tk.Button(self, text="Verificar", font=("Arial", 22),
                                       command=self.verificar_letra)
        self.btn_verificar.pack(pady=10)

        # Enter activa verificar
        self.bind("<Return>", lambda e: self.verificar_letra())

        self.lbl_usadas = tk.Label(self, text="Letras usadas: ", font=("Arial", 20))
        self.lbl_usadas.pack(pady=10)

        self.lbl_intentos = tk.Label(self, text="", font=("Arial", 22))
        self.lbl_intentos.pack(pady=10)

        self.lbl_mensaje = tk.Label(self, text="", font=("Arial", 22), fg="blue")
        self.lbl_mensaje.pack(pady=10)

        # Botón reiniciar oculto al inicio
        self.btn_reiniciar = tk.Button(self, text="Reiniciar", font=("Arial", 22),
                                       command=self.reiniciar)

        # Iniciar juego
        self.iniciar_juego()

    # --------------------------------------------------

    def iniciar_juego(self):
        self.palabra_secreta = random.choice(self.PALABRAS)
        self.progreso = ["_"] * len(self.palabra_secreta)
        self.intentos = 6
        self.letras_usadas = []

        self.lbl_palabra.config(text=" ".join(self.progreso))
        self.lbl_intentos.config(text=f"Intentos restantes: {self.intentos}")
        self.lbl_usadas.config(text="Letras usadas: ")
        self.lbl_mensaje.config(text="")

        self.entry_letra.delete(0, tk.END)

        # Habilitar entrada y botón
        self.entry_letra.config(state="normal")
        self.btn_verificar.config(state="normal")

        self.btn_reiniciar.place_forget()

    # --------------------------------------------------

    def verificar_letra(self):
        # 🔥 Si ya perdió NO DEJAR escribir más
        if self.intentos <= 0:
            self.lbl_mensaje.config(text="No puedes jugar, ya perdiste.")
            return

        letra = self.entry_letra.get().lower()
        self.entry_letra.delete(0, tk.END)

        # Validar solo 1 letra
        if len(letra) != 1 or not letra.isalpha():
            self.lbl_mensaje.config(text="Ingresa solo UNA letra válida.")
            return

        # Si ya uso esa letra
        if letra in self.letras_usadas:
            self.lbl_mensaje.config(text=f"La letra '{letra}' ya la usaste.")
            return

        self.letras_usadas.append(letra)
        self.lbl_usadas.config(text=f"Letras usadas: {', '.join(self.letras_usadas)}")

        # Letra correcta
        if letra in self.palabra_secreta:
            for i, l in enumerate(self.palabra_secreta):
                if l == letra:
                    self.progreso[i] = letra

            self.lbl_palabra.config(text=" ".join(self.progreso))
            self.lbl_mensaje.config(text=f"¡Bien! La letra '{letra}' está.")

            # GANÓ
            if "_" not in self.progreso:
                self.lbl_mensaje.config(text="¡Ganaste! 🎉")
                self.fin_del_juego()
            return

        # Letra incorrecta
        self.intentos -= 1
        self.lbl_intentos.config(text=f"Intentos restantes: {self.intentos}")
        self.lbl_mensaje.config(text=f"La letra '{letra}' NO está.")

        # PERDIÓ
        if self.intentos == 0:
            self.lbl_mensaje.config(text=f"Perdiste 😢 La palabra era: {self.palabra_secreta}")
            self.fin_del_juego()

    # --------------------------------------------------

    def fin_del_juego(self):
        # Bloquear entrada y botón
        self.entry_letra.config(state="disabled")
        self.btn_verificar.config(state="disabled")

        # Mostrar botón reiniciar
        self.btn_reiniciar.place(x=self.ANCHO//2 - 80, y=self.ALTO - 120)

    def reiniciar(self):
        self.iniciar_juego()
