import tkinter as tk
import random

class VentanaJuego(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configuración de estilo
        self.estilo = {
            "bg_color": "#0d1117",
            "card_color": "#161b22",
            "primary": "#238636",
            "accent": "#f78166",
            "text_color": "#c9d1d9",
            "border_color": "#30363d",
            "exito": "#3fb950",
            "error": "#f85149",
            "advertencia": "#d29922"
        }
        
        # Configuración ventana
        self.title("🎮 Word Challenge - Juego en Curso")
        self.ANCHO = 1200
        self.ALTO = 800
        
        # Centrar ventana
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (self.ANCHO // 2)
        y = (pantalla_alto // 2) - (self.ALTO // 2)
        
        self.geometry(f"{self.ANCHO}x{self.ALTO}+{x}+{y}")
        self.resizable(False, False)
        self.configure(bg=self.estilo["bg_color"])
        
        # Frame principal
        self.main_frame = tk.Frame(self, bg=self.estilo["bg_color"])
        self.main_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        # Palabras del juego
        self.palabras = [
            "PYTHON", "PROGRAMACION", "COMPUTADORA", "ALGORITMO", "VARIABLE",
            "FUNCION", "OBJETO", "HERENCIA", "INTERFAZ", "DATABASE",
            "INTERNET", "SISTEMA", "APLICACION", "DESARROLLO", "LENGUAJE",
            "FRAMEWORK", "BIBLIOTECA", "MODULO", "CLASE", "METODO"
        ]
        
        # Inicializar juego
        self.iniciar_juego()
        
        # Crear interfaz
        self.crear_cabecera()
        self.crear_seccion_palabra()
        self.crear_seccion_progreso()
        self.crear_seccion_entrada()
        self.crear_seccion_estadisticas()
        self.crear_seccion_controles()
        
        # Configurar eventos
        self.bind("<Return>", lambda e: self.verificar_letra())
        
        # Dar foco a la ventana
        self.focus_set()
    
    def iniciar_juego(self):
        """Inicializa un nuevo juego"""
        self.palabra_secreta = random.choice(self.palabras)
        self.progreso = ["_"] * len(self.palabra_secreta)
        self.intentos = 6
        self.intentos_totales = 6
        self.letras_usadas = []
        self.juego_activo = True
    
    def crear_cabecera(self):
        """Crea la cabecera del juego"""
        header_frame = tk.Frame(self.main_frame, bg=self.estilo["card_color"])
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título
        title_frame = tk.Frame(header_frame, bg=self.estilo["card_color"])
        title_frame.pack(side="left", padx=30, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="🎮 WORD CHALLENGE",
            font=("Arial Black", 28, "bold"),
            fg=self.estilo["accent"],
            bg=self.estilo["card_color"]
        )
        title_label.pack(anchor="w")
        
        subtitle_label = tk.Label(
            title_frame,
            text="Juego en curso - Adivina la palabra",
            font=("Segoe UI", 14),
            fg=self.estilo["text_color"],
            bg=self.estilo["card_color"]
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Contador de intentos
        attempts_frame = tk.Frame(header_frame, bg=self.estilo["card_color"])
        attempts_frame.pack(side="right", padx=30, pady=15)
        
        self.lbl_intentos = tk.Label(
            attempts_frame,
            text=f"❤️  {self.intentos}/{self.intentos_totales} INTENTOS",
            font=("Segoe UI", 20, "bold"),
            fg=self.estilo["text_color"],
            bg=self.estilo["card_color"]
        )
        self.lbl_intentos.pack()
    
    def crear_seccion_palabra(self):
        """Crea la sección donde se muestra la palabra"""
        word_frame = tk.Frame(self.main_frame, bg=self.estilo["bg_color"])
        word_frame.pack(fill="x", pady=30)
        
        # Frame para las letras
        self.letters_container = tk.Frame(word_frame, bg=self.estilo["bg_color"])
        self.letters_container.pack()
        
        # Crear display de letras
        self.actualizar_display_palabra()
        
        # Indicador de longitud
        self.lbl_longitud = tk.Label(
            word_frame,
            text=f"📏 Palabra de {len(self.palabra_secreta)} letras",
            font=("Segoe UI", 14),
            fg=self.estilo["text_color"],
            bg=self.estilo["bg_color"]
        )
        self.lbl_longitud.pack(pady=(20, 0))
    
    def crear_seccion_progreso(self):
        """Crea la barra de progreso"""
        progress_frame = tk.Frame(self.main_frame, bg=self.estilo["bg_color"])
        progress_frame.pack(fill="x", pady=20)
        
        # Texto de progreso
        self.lbl_progreso = tk.Label(
            progress_frame,
            text="Progreso: 0%",
            font=("Segoe UI", 12),
            fg=self.estilo["text_color"],
            bg=self.estilo["bg_color"]
        )
        self.lbl_progreso.pack(anchor="w", pady=(0, 8))
        
        # Contenedor de la barra
        progress_bg = tk.Frame(
            progress_frame,
            bg=self.estilo["border_color"],
            height=10,
            relief="flat"
        )
        progress_bg.pack(fill="x")
        
        # Barra de progreso
        self.progress_bar = tk.Frame(
            progress_bg,
            bg=self.estilo["primary"],
            height=10
        )
        self.progress_bar.place(x=0, y=0, width=0)
    
    def crear_seccion_entrada(self):
        """Crea la sección de entrada de letras"""
        input_frame = tk.Frame(self.main_frame, bg=self.estilo["bg_color"])
        input_frame.pack(fill="x", pady=30)
        
        # Frame para centrar
        input_center = tk.Frame(input_frame, bg=self.estilo["bg_color"])
        input_center.pack()
        
        # Etiqueta
        tk.Label(
            input_center,
            text="INGRESA UNA LETRA:",
            font=("Segoe UI", 16, "bold"),
            fg=self.estilo["text_color"],
            bg=self.estilo["bg_color"]
        ).pack(pady=(0, 15))
        
        # Frame para entrada y botón
        entry_frame = tk.Frame(input_center, bg=self.estilo["bg_color"])
        entry_frame.pack()
        
        # Entrada de letra
        self.entry_letra = tk.Entry(
            entry_frame,
            font=("Segoe UI", 36, "bold"),
            width=3,
            justify="center",
            bd=0,
            relief="flat",
            fg=self.estilo["text_color"],
            bg=self.estilo["card_color"],
            insertbackground=self.estilo["accent"],
            highlightthickness=2,
            highlightbackground=self.estilo["border_color"],
            highlightcolor=self.estilo["primary"]
        )
        self.entry_letra.pack(side="left", padx=(0, 20))
        self.entry_letra.focus_set()
        
        # Validar que solo se ingrese una letra
        self.entry_letra.bind('<KeyRelease>', self.validar_entrada)
        
        # Botón verificar
        self.btn_verificar = tk.Button(
            entry_frame,
            text="✓ VERIFICAR",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg=self.estilo["primary"],
            activeforeground="white",
            activebackground=self.estilo["accent"],
            command=self.verificar_letra,
            width=15,
            height=1,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=25
        )
        self.btn_verificar.pack(side="left")
        
        # Efecto hover
        self.btn_verificar.bind("<Enter>", 
            lambda e: self.btn_verificar.config(bg=self.estilo["accent"]))
        self.btn_verificar.bind("<Leave>", 
            lambda e: self.btn_verificar.config(bg=self.estilo["primary"]))
    
    def validar_entrada(self, event=None):
        """Valida que solo se ingrese una letra"""
        texto = self.entry_letra.get().upper()
        if len(texto) > 1:
            # Mantener solo el último carácter
            self.entry_letra.delete(0, tk.END)
            self.entry_letra.insert(0, texto[-1])
        elif texto and not texto.isalpha():
            # Si no es letra, limpiar
            self.entry_letra.delete(0, tk.END)
    
    def crear_seccion_estadisticas(self):
        """Crea la sección de estadísticas"""
        stats_frame = tk.Frame(self.main_frame, bg=self.estilo["bg_color"])
        stats_frame.pack(fill="x", pady=20)
        
        # Crear 3 columnas
        for i, (titulo, variable) in enumerate([
            ("📝 LETRAS USADAS", "lbl_usadas"),
            ("💡 MENSAJE", "lbl_mensaje"),
            ("📊 ESTADÍSTICAS", "lbl_detalles")
        ]):
            card = tk.Frame(
                stats_frame,
                bg=self.estilo["card_color"],
                relief="flat",
                highlightthickness=1,
                highlightbackground=self.estilo["border_color"],
                padx=15,
                pady=15
            )
            card.pack(side="left", expand=True, fill="both", padx=5)
            
            # Título de la tarjeta
            tk.Label(
                card,
                text=titulo,
                font=("Segoe UI", 12, "bold"),
                fg=self.estilo["text_color"],
                bg=self.estilo["card_color"]
            ).pack(anchor="w", pady=(0, 8))
            
            # Contenido de la tarjeta
            if i == 0:  # Letras usadas
                self.lbl_usadas = tk.Label(
                    card,
                    text="Ninguna",
                    font=("Segoe UI", 13),
                    fg=self.estilo["text_color"],
                    bg=self.estilo["card_color"],
                    wraplength=250,
                    justify="left"
                )
                self.lbl_usadas.pack(anchor="w")
            
            elif i == 1:  # Mensaje
                self.lbl_mensaje = tk.Label(
                    card,
                    text="¡Comienza adivinando!",
                    font=("Segoe UI", 13),
                    fg=self.estilo["exito"],
                    bg=self.estilo["card_color"],
                    wraplength=250,
                    justify="left"
                )
                self.lbl_mensaje.pack(anchor="w")
            
            elif i == 2:  # Estadísticas
                self.lbl_detalles = tk.Label(
                    card,
                    text="",
                    font=("Segoe UI", 12),
                    fg=self.estilo["text_color"],
                    bg=self.estilo["card_color"],
                    justify="left"
                )
                self.lbl_detalles.pack(anchor="w")
    
    def crear_seccion_controles(self):
        """Crea la sección de controles"""
        controls_frame = tk.Frame(self.main_frame, bg=self.estilo["bg_color"])
        controls_frame.pack(fill="x", pady=(30, 0))
        
        # Botón volver al menú
        self.btn_volver = tk.Button(
            controls_frame,
            text="← VOLVER AL MENÚ",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg=self.estilo["border_color"],
            activeforeground="white",
            activebackground=self.estilo["text_color"],
            command=self.destroy,
            width=18,
            height=1,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=20
        )
        self.btn_volver.pack(side="left", padx=10)
        
        # Botón reiniciar (inicialmente oculto)
        self.btn_reiniciar = tk.Button(
            controls_frame,
            text="🔄 JUGAR DE NUEVO",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg=self.estilo["accent"],
            activeforeground="white",
            activebackground="#e86955",
            command=self.reiniciar_juego,
            width=18,
            height=1,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=20
        )
        
        # Efectos hover
        self.btn_volver.bind("<Enter>", 
            lambda e: self.btn_volver.config(bg=self.estilo["text_color"]))
        self.btn_volver.bind("<Leave>", 
            lambda e: self.btn_volver.config(bg=self.estilo["border_color"]))
        
        self.btn_reiniciar.bind("<Enter>", 
            lambda e: self.btn_reiniciar.config(bg="#e86955"))
        self.btn_reiniciar.bind("<Leave>", 
            lambda e: self.btn_reiniciar.config(bg=self.estilo["accent"]))
    
    def actualizar_display_palabra(self):
        """Actualiza el display visual de la palabra"""
        # Limpiar frame de letras
        for widget in self.letters_container.winfo_children():
            widget.destroy()
        
        # Crear un cuadro para cada letra
        for i, letra in enumerate(self.progreso):
            if letra == "_":
                # Cuadro vacío
                cuadro = tk.Frame(
                    self.letters_container,
                    width=65,
                    height=75,
                    bg=self.estilo["card_color"],
                    highlightthickness=2,
                    highlightbackground=self.estilo["border_color"]
                )
                cuadro.pack(side="left", padx=5, pady=5)
                cuadro.pack_propagate(False)
                
                tk.Label(
                    cuadro,
                    text="",
                    font=("Segoe UI", 26, "bold"),
                    fg=self.estilo["text_color"],
                    bg=self.estilo["card_color"]
                ).pack(expand=True)
            else:
                # Cuadro con letra adivinada
                cuadro = tk.Frame(
                    self.letters_container,
                    width=65,
                    height=75,
                    bg=self.estilo["primary"],
                    highlightthickness=2,
                    highlightbackground=self.estilo["primary"]
                )
                cuadro.pack(side="left", padx=5, pady=5)
                cuadro.pack_propagate(False)
                
                tk.Label(
                    cuadro,
                    text=letra,
                    font=("Segoe UI", 26, "bold"),
                    fg="white",
                    bg=self.estilo["primary"]
                ).pack(expand=True)
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas del juego"""
        # Calcular progreso
        letras_adivinadas = sum(1 for l in self.progreso if l != '_')
        total_letras = len(self.palabra_secreta)
        porcentaje = int((letras_adivinadas / total_letras) * 100) if total_letras > 0 else 0
        
        # Actualizar barra de progreso
        self.lbl_progreso.config(text=f"Progreso: {porcentaje}%")
        
        # Actualizar ancho de barra
        if self.progress_bar.master.winfo_width() > 0:
            ancho_total = self.progress_bar.master.winfo_width()
            ancho_actual = (ancho_total * porcentaje) // 100
            self.progress_bar.config(width=ancho_actual)
        
        # Actualizar detalles
        detalles = f"""• Letras: {letras_adivinadas}/{total_letras}
• Restantes: {self.progreso.count('_')}
• Intentos usados: {self.intentos_totales - self.intentos}
• Progreso: {porcentaje}%"""
        
        self.lbl_detalles.config(text=detalles)
        
        # Actualizar letras usadas
        if self.letras_usadas:
            self.lbl_usadas.config(
                text=", ".join(self.letras_usadas),
                fg=self.estilo["text_color"]
            )
        else:
            self.lbl_usadas.config(
                text="Ninguna",
                fg=self.estilo["text_color"]
            )
    
    def verificar_letra(self):
        """Verifica la letra ingresada por el jugador"""
        if not self.juego_activo:
            return
        
        letra = self.entry_letra.get().upper().strip()
        self.entry_letra.delete(0, tk.END)
        
        # Validaciones
        if not letra:
            self.lbl_mensaje.config(text="Por favor, ingresa una letra", 
                                   fg=self.estilo["advertencia"])
            return
        
        if len(letra) != 1:
            self.lbl_mensaje.config(text="Ingresa solo UNA letra", 
                                   fg=self.estilo["advertencia"])
            return
        
        if not letra.isalpha():
            self.lbl_mensaje.config(text="Ingresa una letra válida", 
                                   fg=self.estilo["advertencia"])
            return
        
        if letra in self.letras_usadas:
            self.lbl_mensaje.config(text=f"'{letra}' ya fue usada", 
                                   fg=self.estilo["advertencia"])
            return
        
        # Procesar la letra
        self.letras_usadas.append(letra)
        
        # Verificar si está en la palabra
        if letra in self.palabra_secreta:
            # Actualizar progreso
            aciertos = 0
            for i, l in enumerate(self.palabra_secreta):
                if l == letra:
                    self.progreso[i] = letra
                    aciertos += 1
            
            # Actualizar display
            self.actualizar_display_palabra()
            self.lbl_mensaje.config(
                text=f"¡Correcto! '{letra}' aparece {aciertos} vez{'es' if aciertos > 1 else ''}",
                fg=self.estilo["exito"]
            )
            
            # Verificar victoria
            if "_" not in self.progreso:
                self.finalizar_juego(victoria=True)
                return
        else:
            # Letra incorrecta
            self.intentos -= 1
            self.lbl_intentos.config(text=f"❤️  {self.intentos}/{self.intentos_totales} INTENTOS")
            self.lbl_mensaje.config(text=f"'{letra}' no está en la palabra", 
                                   fg=self.estilo["error"])
            
            # Verificar derrota
            if self.intentos == 0:
                self.finalizar_juego(victoria=False)
                return
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()
        self.entry_letra.focus_set()
    
    def finalizar_juego(self, victoria):
        """Finaliza el juego y muestra el resultado"""
        self.juego_activo = False
        
        # Deshabilitar controles
        self.entry_letra.config(state="disabled")
        self.btn_verificar.config(state="disabled")
        
        # Mostrar resultado
        if victoria:
            # Mostrar palabra completa en verde
            self.actualizar_display_palabra()
            for widget in self.letters_container.winfo_children():
                widget.config(bg=self.estilo["exito"], 
                            highlightbackground=self.estilo["exito"])
                widget.winfo_children()[0].config(bg=self.estilo["exito"], 
                                                fg="white")
            
            self.lbl_mensaje.config(
                text=f"🎉 ¡FELICIDADES! 🎉\nPalabra: {self.palabra_secreta}",
                fg=self.estilo["exito"]
            )
        else:
            # Mostrar palabra completa en rojo
            for i, widget in enumerate(self.letters_container.winfo_children()):
                letra = self.palabra_secreta[i]
                widget.config(bg=self.estilo["error"], 
                            highlightbackground=self.estilo["error"])
                label = widget.winfo_children()[0]
                label.config(text=letra, bg=self.estilo["error"], fg="white")
            
            self.lbl_mensaje.config(
                text=f"💀 ¡GAME OVER! 💀\nPalabra: {self.palabra_secreta}",
                fg=self.estilo["error"]
            )
        
        # Mostrar botón reiniciar
        self.btn_reiniciar.pack(side="right", padx=10)
        
        # Actualizar estadísticas finales
        self.actualizar_estadisticas()
    
    def reiniciar_juego(self):
        """Reinicia el juego completamente"""
        # Reinicializar juego
        self.iniciar_juego()
        
        # Habilitar controles
        self.entry_letra.config(state="normal")
        self.btn_verificar.config(state="normal")
        
        # Actualizar interfaz
        self.lbl_intentos.config(text=f"❤️  {self.intentos}/{self.intentos_totales} INTENTOS")
        self.lbl_mensaje.config(text="¡Nuevo juego! Ingresa tu primera letra.", 
                               fg=self.estilo["exito"])
        
        # Actualizar display
        self.actualizar_display_palabra()
        self.actualizar_estadisticas()
        
        # Ocultar botón reiniciar
        self.btn_reiniciar.pack_forget()
        
        # Dar foco a la entrada
        self.entry_letra.focus_set()
        self.juego_activo = True