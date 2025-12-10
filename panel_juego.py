# panel_juego.py
import tkinter as tk
from tkinter import font
from typing import Callable, Optional, Dict

class PanelJuego(tk.Frame):
    """Panel principal del juego donde se muestra la palabra y se reciben intentos"""
    
    def __init__(self, parent, juego_logica, on_intento: Callable = None, colores: Dict = None):
        super().__init__(parent)
        self.juego_logica = juego_logica
        self.on_intento = on_intento
        
        # Colores del menú inicial
        self.colores = colores or {
            "fondo_principal": "#1a1a2e",
            "fondo_secundario": "#16213e",
            "fondo_terciario": "#0f3460",
            "acento_principal": "#e94560",
            "acento_secundario": "#4cc9f0",
            "texto_principal": "#ffffff",
            "texto_secundario": "#a5b4cb",
            "verde": "#4ade80",
            "amarillo": "#fbbf24",
            "rojo": "#f87171",
            "azul": "#3b82f6",
            "morado": "#8b5cf6"
        }
        
        self.configurar_interfaz()
        self.actualizar_panel()
    
    def configurar_interfaz(self):
        """Configura los elementos de la interfaz del panel de juego"""
        # Configurar fondo
        self.configure(bg=self.colores["fondo_secundario"])
        
        # Frame para información de partida
        frame_info_partida = tk.Frame(self, bg=self.colores["fondo_terciario"], 
                                     relief=tk.RIDGE, bd=2)
        frame_info_partida.pack(pady=(10, 5), padx=10, fill=tk.X)
        
        # Dificultad actual
        self.label_dificultad = tk.Label(
            frame_info_partida,
            font=("Arial", 10, "bold"),
            bg=self.colores["fondo_terciario"],
            fg=self.colores["texto_secundario"]
        )
        self.label_dificultad.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Modo de juego
        self.label_modo = tk.Label(
            frame_info_partida,
            text="Modo: Letra Individual",
            font=("Arial", 9, "italic"),
            bg=self.colores["fondo_terciario"],
            fg=self.colores["texto_secundario"]
        )
        self.label_modo.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Frame para la palabra (centrado)
        frame_palabra = tk.Frame(self, bg="#1a1a2e", relief=tk.SUNKEN, bd=3)
        frame_palabra.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Etiqueta de la palabra oculta
        self.label_palabra = tk.Label(
            frame_palabra,
            font=("Consolas", 40, "bold"),
            bg="#1a1a2e",
            fg=self.colores["texto_principal"],
            height=2,
            justify=tk.CENTER
        )
        self.label_palabra.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Frame para estadísticas en tiempo real
        frame_stats = tk.Frame(self, bg=self.colores["fondo_secundario"])
        frame_stats.pack(pady=10, fill=tk.X, padx=20)
        
        # Columna izquierda: Intentos
        frame_intentos = tk.Frame(frame_stats, bg=self.colores["fondo_secundario"])
        frame_intentos.pack(side=tk.LEFT, expand=True)
        
        tk.Label(
            frame_intentos,
            text="🎯 INTENTOS",
            font=("Arial", 10, "bold"),
            bg=self.colores["fondo_secundario"],
            fg=self.colores["rojo"]
        ).pack()
        
        self.label_intentos = tk.Label(
            frame_intentos,
            font=("Arial", 14, "bold"),
            bg=self.colores["fondo_secundario"],
            fg=self.colores["rojo"]
        )
        self.label_intentos.pack()
        
        # Columna central: Tiempo
        frame_tiempo = tk.Frame(frame_stats, bg=self.colores["fondo_secundario"])
        frame_tiempo.pack(side=tk.LEFT, expand=True)
        
        tk.Label(
            frame_tiempo,
            text="⏱️ TIEMPO",
            font=("Arial", 10, "bold"),
            bg=self.colores["fondo_secundario"],
            fg=self.colores["acento_secundario"]
        ).pack()
        
        self.label_tiempo = tk.Label(
            frame_tiempo,
            font=("Arial", 14, "bold"),
            bg=self.colores["fondo_secundario"],
            fg=self.colores["acento_secundario"]
        )
        self.label_tiempo.pack()
        
        # Columna derecha: Letras incorrectas
        frame_incorrectas = tk.Frame(frame_stats, bg=self.colores["fondo_secundario"])
        frame_incorrectas.pack(side=tk.LEFT, expand=True)
        
        tk.Label(
            frame_incorrectas,
            text="❌ INCORRECTAS",
            font=("Arial", 10, "bold"),
            bg=self.colores["fondo_secundario"],
            fg=self.colores["texto_secundario"]
        ).pack()
        
        self.label_incorrectas = tk.Label(
            frame_incorrectas,
            font=("Arial", 12),
            bg=self.colores["fondo_secundario"],
            fg=self.colores["texto_secundario"]
        )
        self.label_incorrectas.pack()
        
        # Frame para entrada de usuario
        frame_entrada = tk.Frame(self, bg=self.colores["fondo_secundario"])
        frame_entrada.pack(pady=20)
        
        tk.Label(
            frame_entrada,
            text="🔤 INTRODUCE UNA LETRA:",
            font=("Arial", 11, "bold"),
            bg=self.colores["fondo_secundario"],
            fg=self.colores["texto_principal"]
        ).pack(pady=(0, 10))
        
        # Frame para el campo de entrada
        frame_campo = tk.Frame(frame_entrada, bg=self.colores["fondo_secundario"])
        frame_campo.pack()
        
        self.entrada_letra = tk.Entry(
            frame_campo,
            font=("Arial", 24),
            width=6,
            justify=tk.CENTER,
            bd=3,
            relief=tk.SUNKEN,
            bg="#0f3460",
            fg=self.colores["texto_principal"],
            insertbackground=self.colores["texto_principal"]
        )
        self.entrada_letra.pack(side=tk.LEFT, padx=5)
        self.entrada_letra.bind("<Return>", self.enviar_intento)
        
        # Botón para adivinar
        self.boton_intento = tk.Button(
            frame_campo,
            text="ADIVINAR",
            font=("Arial", 12, "bold"),
            bg=self.colores["verde"],
            fg="white",
            padx=25,
            pady=8,
            command=self.enviar_intento,
            cursor="hand2",
            activebackground=self.colores["verde"],
            activeforeground="white"
        )
        self.boton_intento.pack(side=tk.LEFT, padx=5)
        
        # Frame para pistas
        self.frame_pistas = tk.Frame(self, bg="#2a2a4e", relief=tk.GROOVE, bd=2)
        
        # Título de pistas
        tk.Label(
            self.frame_pistas,
            text="💡 PISTAS DISPONIBLES",
            font=("Arial", 10, "bold"),
            bg="#2a2a4e",
            fg=self.colores["amarillo"]
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Área para mostrar pistas
        self.lista_pistas = tk.Label(
            self.frame_pistas,
            font=("Arial", 10),
            justify=tk.LEFT,
            bg="#2a2a4e",
            fg=self.colores["amarillo"],
            wraplength=400
        )
        self.lista_pistas.pack(anchor=tk.W, padx=20, pady=(0, 10), fill=tk.BOTH)
    
    def enviar_intento(self, event=None):
        """Envía el intento del jugador"""
        letra = self.entrada_letra.get().strip()
        if letra and self.on_intento:
            self.on_intento(letra)
            self.entrada_letra.delete(0, tk.END)
            self.entrada_letra.focus()
    
    def actualizar_panel(self):
        """Actualiza toda la información en el panel"""
        estado = self.juego_logica.obtener_estado_actual()
        
        # Actualizar dificultad
        dificultad = estado["dificultad"]
        colores_dificultad = {
            "FACIL": self.colores["verde"],
            "MEDIO": self.colores["amarillo"],
            "DIFICIL": self.colores["rojo"]
        }
        self.label_dificultad.config(
            text=f"Dificultad: {dificultad}",
            fg=colores_dificultad.get(dificultad, self.colores["texto_secundario"])
        )
        
        # Actualizar palabra oculta
        self.label_palabra.config(text=estado["oculta"])
        
        # Cambiar color según estado del juego
        if estado["game_over"]:
            if estado["victoria"]:
                self.label_palabra.config(fg=self.colores["verde"])  # Verde para victoria
                self.label_palabra.config(bg="#1a3a1a")  # Fondo verde oscuro
            else:
                self.label_palabra.config(fg=self.colores["rojo"])  # Rojo para derrota
                self.label_palabra.config(bg="#3a1a1a")  # Fondo rojo oscuro
        else:
            self.label_palabra.config(fg=self.colores["texto_principal"])  # Blanco normal
            self.label_palabra.config(bg="#1a1a2e")  # Fondo oscuro
        
        # Actualizar intentos
        self.label_intentos.config(
            text=f"{estado['intentos']}/{estado['max_intentos']}"
        )
        
        # Actualizar tiempo si está habilitado
        if self.juego_logica.config.obtener("mostrar_tiempo", True):
            self.label_tiempo.config(text=f"{estado['tiempo']}s")
        else:
            self.label_tiempo.config(text="--")
        
        # Actualizar letras incorrectas
        if estado["letras_incorrectas"]:
            incorrectas_texto = " ".join(sorted(estado["letras_incorrectas"]))
            self.label_incorrectas.config(text=incorrectas_texto)
        else:
            self.label_incorrectas.config(text="---")
        
        # Actualizar pistas
        pistas = self.juego_logica.obtener_pistas()
        if pistas:
            pistas_texto = "\n".join(f"• {pista}" for pista in pistas)
            self.lista_pistas.config(text=pistas_texto)
            self.frame_pistas.pack(pady=15, padx=20, fill=tk.X)
        else:
            self.frame_pistas.pack_forget()
        
        # Cambiar estado del botón si el juego terminó
        if estado["game_over"]:
            self.boton_intento.config(
                text="JUEGO TERMINADO",
                bg=self.colores["fondo_terciario"],
                state=tk.DISABLED
            )
            self.entrada_letra.config(state=tk.DISABLED)
        else:
            self.boton_intento.config(
                text="ADIVINAR",
                bg=self.colores["verde"],
                state=tk.NORMAL
            )
            self.entrada_letra.config(state=tk.NORMAL)
    
    def focus_entrada(self):
        """Pone el foco en la entrada de texto"""
        self.entrada_letra.focus()