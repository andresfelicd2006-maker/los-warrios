import tkinter as tk
from PIL import Image, ImageDraw
from ventana_juego import VentanaJuego

class MenuInicial(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración de estilo
        self.estilo = {
            "bg_color": "#0d1117",
            "card_color": "#161b22",
            "primary": "#238636",
            "accent": "#f78166",
            "text_color": "#c9d1d9",
            "border_color": "#30363d"
        }
        
        # Ventana principal
        self.title("🧠 Word Challenge Pro")
        self.ANCHO = 1100
        self.ALTO = 650
        
        # Centrar ventana
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (self.ANCHO // 2)
        y = (pantalla_alto // 2) - (self.ALTO // 2)
        
        self.geometry(f"{self.ANCHO}x{self.ALTO}+{x}+{y}")
        self.resizable(False, False)
        self.configure(bg=self.estilo["bg_color"])
        
        # Crear imágenes personalizadas
        self.crear_imagenes()
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_imagenes(self):
        """Crea imágenes personalizadas para el menú"""
        try:
            # Crear icono de cerebro
            brain_img = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
            draw = ImageDraw.Draw(brain_img)
            
            # Dibujar cerebro simplificado
            draw.ellipse([20, 20, 60, 60], fill=(248, 129, 102, 255))
            draw.ellipse([10, 30, 40, 60], fill=(248, 129, 102, 255))
            draw.ellipse([40, 30, 70, 60], fill=(248, 129, 102, 255))
            
            self.brain_icon = tk.PhotoImage(data=self.image_to_tk(brain_img))
            
            # Crear icono de play
            play_img = Image.new('RGBA', (40, 40), (0, 0, 0, 0))
            draw = ImageDraw.Draw(play_img)
            
            # Triángulo de play
            points = [(5, 5), (5, 35), (30, 20)]
            draw.polygon(points, fill=(35, 134, 54, 255))
            
            self.play_icon = tk.PhotoImage(data=self.image_to_tk(play_img))
            
            # Crear icono de exit
            exit_img = Image.new('RGBA', (40, 40), (0, 0, 0, 0))
            draw = ImageDraw.Draw(exit_img)
            
            # Cruz de salida
            draw.line([10, 10, 30, 30], fill=(255, 107, 107, 255), width=3)
            draw.line([30, 10, 10, 30], fill=(255, 107, 107, 255), width=3)
            
            self.exit_icon = tk.PhotoImage(data=self.image_to_tk(exit_img))
            
        except Exception as e:
            print(f"Error creando imágenes: {e}")
            # Usar texto como fallback
            self.brain_icon = None
            self.play_icon = None
            self.exit_icon = None
    
    def image_to_tk(self, pil_image):
        """Convierte una imagen PIL a formato compatible con Tkinter"""
        import io
        import base64
        
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Convertir a base64
        b64_data = base64.b64encode(buffer.getvalue()).decode()
        return b64_data
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        # Frame principal
        main_container = tk.Frame(self, bg=self.estilo["bg_color"])
        main_container.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Columna izquierda (Título y descripción)
        left_frame = tk.Frame(main_container, bg=self.estilo["bg_color"])
        left_frame.pack(side="left", expand=True, fill="both", padx=(0, 40))
        
        # Título con icono
        title_frame = tk.Frame(left_frame, bg=self.estilo["bg_color"])
        title_frame.pack(anchor="w", pady=(50, 10))
        
        if hasattr(self, 'brain_icon') and self.brain_icon:
            brain_label = tk.Label(
                title_frame,
                image=self.brain_icon,
                bg=self.estilo["bg_color"]
            )
            brain_label.pack(side="left", padx=(0, 20))
        
        title_text = tk.Label(
            title_frame,
            text="WORD\nCHALLENGE",
            font=("Arial Black", 60, "bold"),
            fg=self.estilo["accent"],
            bg=self.estilo["bg_color"],
            justify="left"
        )
        title_text.pack(side="left")
        
        # Subtítulo
        subtitle_label = tk.Label(
            left_frame,
            text="EL DESAFÍO DEFINITIVO DE PALABRAS",
            font=("Segoe UI", 18),
            fg="#8b949e",
            bg=self.estilo["bg_color"]
        )
        subtitle_label.pack(anchor="w", pady=(0, 30))
        
        # Descripción
        desc_text = """🔥 Desafía tu mente y vocabulario

• Adivina palabras secretas
• Pistas inteligentes
• Múltiples niveles
• Estadísticas en tiempo real
• Modo competitivo"""
        
        desc_label = tk.Label(
            left_frame,
            text=desc_text,
            font=("Segoe UI", 16),
            fg="#8b949e",
            bg=self.estilo["bg_color"],
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(30, 0))
        
        # Columna derecha (Botones)
        right_frame = tk.Frame(main_container, bg=self.estilo["bg_color"])
        right_frame.pack(side="right", expand=True, fill="both")
        
        # Tarjeta para botones
        card = tk.Frame(
            right_frame,
            bg=self.estilo["card_color"],
            relief="flat",
            highlightthickness=2,
            highlightbackground=self.estilo["border_color"]
        )
        card.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Contenido de la tarjeta
        card_content = tk.Frame(card, bg=self.estilo["card_color"], padx=40, pady=40)
        card_content.pack(expand=True, fill="both")
        
        # Icono grande
        if hasattr(self, 'brain_icon') and self.brain_icon:
            icon_label = tk.Label(
                card_content,
                image=self.brain_icon,
                bg=self.estilo["card_color"]
            )
            icon_label.pack(pady=(20, 40))
        else:
            # Fallback con texto
            icon_label = tk.Label(
                card_content,
                text="🧠",
                font=("Arial", 80),
                bg=self.estilo["card_color"],
                fg=self.estilo["accent"]
            )
            icon_label.pack(pady=(20, 40))
        
        # Botón Jugar
        btn_jugar_frame = tk.Frame(card_content, bg=self.estilo["card_color"])
        btn_jugar_frame.pack(pady=15)
        
        if hasattr(self, 'play_icon') and self.play_icon:
            play_img_label = tk.Label(
                btn_jugar_frame,
                image=self.play_icon,
                bg=self.estilo["card_color"]
            )
            play_img_label.pack(side="left", padx=(0, 15))
        
        self.btn_jugar = tk.Button(
            btn_jugar_frame,
            text="▶ COMENZAR",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg=self.estilo["primary"],
            activeforeground="white",
            activebackground=self.estilo["accent"],
            command=self.iniciar_juego,
            width=20,
            height=2,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=20
        )
        self.btn_jugar.pack(side="left")
        
        # Botón Salir
        btn_salir_frame = tk.Frame(card_content, bg=self.estilo["card_color"])
        btn_salir_frame.pack(pady=15)
        
        if hasattr(self, 'exit_icon') and self.exit_icon:
            exit_img_label = tk.Label(
                btn_salir_frame,
                image=self.exit_icon,
                bg=self.estilo["card_color"]
            )
            exit_img_label.pack(side="left", padx=(0, 15))
        
        self.btn_salir = tk.Button(
            btn_salir_frame,
            text="SALIR",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#d33",
            activeforeground="white",
            activebackground="#f55",
            command=self.quit,
            width=20,
            height=2,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=20
        )
        self.btn_salir.pack(side="left")
        
        # Efectos hover
        self.configurar_hover(self.btn_jugar, self.estilo["accent"], self.estilo["primary"])
        self.configurar_hover(self.btn_salir, "#f55", "#d33")
        
        # Footer
        footer = tk.Frame(self, bg=self.estilo["bg_color"], height=40)
        footer.pack(side="bottom", fill="x")
        
        footer_label = tk.Label(
            footer,
            text="© 2024 Word Challenge Pro | Desarrollado con Python",
            font=("Segoe UI", 10),
            fg="#666666",
            bg=self.estilo["bg_color"]
        )
        footer_label.pack(pady=10)
        
        # Animación del título
        self.animate_title(title_text)
    
    def configurar_hover(self, boton, color_hover, color_normal):
        """Configura efectos hover para los botones"""
        boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
        boton.bind("<Leave>", lambda e: boton.config(bg=color_normal))
    
    def animate_title(self, title_label):
        """Anima el título con efecto de brillo"""
        colors = [self.estilo["accent"], "#ff6b6b", "#ff8e53", "#ffd166"]
        self.title_color_index = 0
        
        def change_color():
            if self.title_color_index < len(colors):
                color = colors[self.title_color_index]
                title_label.config(fg=color)
                self.title_color_index += 1
            else:
                self.title_color_index = 0
            self.after(1000, change_color)
        
        change_color()
    
    def iniciar_juego(self):
        """Inicia el juego"""
        VentanaJuego(self)