import tkinter as tk
from ventana_juego import VentanaJuego

class MenuInicial(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración de estilo moderno
        self.estilo = {
            "bg_color": "#0d1117",
            "card_color": "#161b22",
            "primary": "#238636",
            "accent": "#f78166",
            "text_color": "#c9d1d9",
            "border_color": "#30363d"
        }
        
        # Configuración ventana
        self.title("🎮 Word Challenge Pro")
        self.ANCHO = 1100
        self.ALTO = 700
        
        # Centrar ventana
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (self.ANCHO // 2)
        y = (pantalla_alto // 2) - (self.ALTO // 2)
        
        self.geometry(f"{self.ANCHO}x{self.ALTO}+{x}+{y}")
        self.resizable(False, False)
        self.configure(bg=self.estilo["bg_color"])
        
        # Frame principal
        main_frame = tk.Frame(self, bg=self.estilo["bg_color"])
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Título con efecto
        title_frame = tk.Frame(main_frame, bg=self.estilo["bg_color"])
        title_frame.pack(pady=(0, 40))
        
        # Título principal
        self.lbl_titulo = tk.Label(
            title_frame,
            text="WORD CHALLENGE",
            font=("Arial Black", 52, "bold"),
            fg=self.estilo["accent"],
            bg=self.estilo["bg_color"]
        )
        self.lbl_titulo.pack()
        
        # Subtítulo
        self.lbl_subtitulo = tk.Label(
            title_frame,
            text="El desafío definitivo de palabras",
            font=("Segoe UI", 20),
            fg=self.estilo["text_color"],
            bg=self.estilo["bg_color"]
        )
        self.lbl_subtitulo.pack(pady=(10, 0))
        
        # Frame de contenido
        content_frame = tk.Frame(main_frame, bg=self.estilo["card_color"])
        content_frame.pack(expand=True, fill="both")
        
        # Panel izquierdo - Características
        left_panel = tk.Frame(content_frame, bg=self.estilo["card_color"], padx=40, pady=40)
        left_panel.pack(side="left", expand=True, fill="both")
        
        # Icono
        icon_label = tk.Label(
            left_panel,
            text="🧠",
            font=("Arial", 80),
            fg=self.estilo["accent"],
            bg=self.estilo["card_color"]
        )
        icon_label.pack(pady=(0, 30))
        
        # Características
        features = [
            "🎯 Adivina palabras secretas",
            "🧠 Mejora tu vocabulario",
            "📊 Estadísticas en tiempo real",
            "⚡ Dificultad progresiva",
            "🏆 Modo desafío",
            "💡 Pistas inteligentes"
        ]
        
        for feature in features:
            lbl = tk.Label(
                left_panel,
                text=feature,
                font=("Segoe UI", 16),
                fg=self.estilo["text_color"],
                bg=self.estilo["card_color"],
                anchor="w"
            )
            lbl.pack(anchor="w", pady=10, padx=20)
        
        # Separador vertical
        separator = tk.Frame(content_frame, bg=self.estilo["border_color"], width=2)
        separator.pack(side="left", fill="y", padx=20)
        
        # Panel derecho - Botones
        right_panel = tk.Frame(content_frame, bg=self.estilo["card_color"], padx=40, pady=40)
        right_panel.pack(side="right", expand=True, fill="both")
        
        # Título del panel
        panel_title = tk.Label(
            right_panel,
            text="COMENZAR JUEGO",
            font=("Segoe UI", 28, "bold"),
            fg=self.estilo["primary"],
            bg=self.estilo["card_color"]
        )
        panel_title.pack(pady=(20, 50))
        
        # Botón Jugar
        self.btn_jugar = tk.Button(
            right_panel,
            text="▶  INICIAR PARTIDA",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg=self.estilo["primary"],
            activeforeground="white",
            activebackground=self.estilo["accent"],
            command=self.iniciar_juego,
            width=22,
            height=2,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=20
        )
        self.btn_jugar.pack(pady=20)
        
        # Botón Salir
        self.btn_salir = tk.Button(
            right_panel,
            text="⏹  SALIR DEL JUEGO",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#d33",
            activeforeground="white",
            activebackground="#f55",
            command=self.quit,
            width=22,
            height=2,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=20
        )
        self.btn_salir.pack(pady=10)
        
        # Efectos hover
        self.btn_jugar.bind("<Enter>", lambda e: self.btn_jugar.config(bg=self.estilo["accent"]))
        self.btn_jugar.bind("<Leave>", lambda e: self.btn_jugar.config(bg=self.estilo["primary"]))
        
        self.btn_salir.bind("<Enter>", lambda e: self.btn_salir.config(bg="#f55"))
        self.btn_salir.bind("<Leave>", lambda e: self.btn_salir.config(bg="#d33"))
        
        # Footer
        footer = tk.Frame(self, bg=self.estilo["bg_color"], height=40)
        footer.pack(side="bottom", fill="x")
        
        footer_label = tk.Label(
            footer,
            text="© 2024 Word Challenge Pro | Desarrollado con Python y Tkinter",
            font=("Segoe UI", 10),
            fg="#666666",
            bg=self.estilo["bg_color"]
        )
        footer_label.pack(pady=10)
        
        # Animación del título
        self.animar_titulo()
    
    def animar_titulo(self):
        """Anima el título con cambio de colores"""
        colores = [self.estilo["accent"], "#ff6b6b", "#ff8e53", "#ffd166", "#4ecdc4"]
        self.indice_color = 0
        
        def cambiar_color():
            color = colores[self.indice_color % len(colores)]
            self.lbl_titulo.config(fg=color)
            self.indice_color += 1
            self.after(1500, cambiar_color)
        
        cambiar_color()
    
    def iniciar_juego(self):
        """Inicia el juego"""
        VentanaJuego(self)