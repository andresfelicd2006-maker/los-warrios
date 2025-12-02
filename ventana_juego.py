import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random
from palabra_juego import PalabraJuego

class VentanaJuego(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Ocultar la ventana principal temporalmente
        parent.withdraw()
        
        # Inicializar juego
        self.juego = PalabraJuego()
        
        # Configuración de colores
        self.COLOR_FONDO = "#0d1117"
        self.COLOR_TARJETA = "#161b22"
        self.COLOR_PRIMARIO = "#238636"
        self.COLOR_SECUNDARIO = "#f78166"
        self.COLOR_ACENTO = "#58a6ff"
        self.COLOR_TEXTO = "#c9d1d9"
        self.COLOR_TEXTO_SECUNDARIO = "#8b949e"
        self.COLOR_EXITO = "#3fb950"
        self.COLOR_ERROR = "#f85149"
        self.COLOR_ADVERTENCIA = "#d29922"
        self.COLOR_BORDE = "#30363d"
        
        # Configuración ventana
        self.ANCHO = 1200
        self.ALTO = 800
        self.title("🎮 Word Challenge - Juego en Curso")
        
        # Centrar ventana
        self.centrar_ventana()
        
        self.geometry(f"{self.ANCHO}x{self.ALTO}+{self.x}+{self.y}")
        self.resizable(False, False)
        self.configure(bg=self.COLOR_FONDO)
        
        # Crear fondo
        self.create_background()
        
        # Frame principal
        self.main_frame = tk.Frame(self, bg=self.COLOR_FONDO)
        self.main_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        # Crear interfaz
        self.crear_cabecera()
        self.crear_seccion_palabra()
        self.crear_seccion_progreso()
        self.crear_seccion_entrada()
        self.crear_seccion_estadisticas()
        self.crear_seccion_controles()
        
        # Configurar eventos
        self.bind("<Return>", lambda e: self.verificar_letra())
        self.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana(parent))
        
        # Inicializar interfaz
        self.actualizar_interfaz()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        self.x = (pantalla_ancho // 2) - (self.ANCHO // 2)
        self.y = (pantalla_alto // 2) - (self.ALTO // 2)
    
    def create_background(self):
        """Crea un fondo para el juego"""
        try:
            # Crear fondo programáticamente
            bg_img = Image.new('RGB', (self.ANCHO, self.ALTO), color=self.COLOR_FONDO)
            draw = ImageDraw.Draw(bg_img)
            
            # Patrón sutil
            for i in range(0, self.ANCHO, 100):
                for j in range(0, self.ALTO, 100):
                    # Puntos de conexión
                    draw.ellipse([i+40, j+40, i+45, j+45], fill=(86, 169, 253, 30))
            
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            
            # Mostrar fondo
            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
        except Exception as e:
            print(f"Error creando fondo: {e}")
            self.configure(bg=self.COLOR_FONDO)
    
    def crear_cabecera(self):
        """Crea la cabecera del juego"""
        header_frame = tk.Frame(self.main_frame, bg=self.COLOR_TARJETA)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título
        title_frame = tk.Frame(header_frame, bg=self.COLOR_TARJETA)
        title_frame.pack(side="left", padx=30, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="🎮 WORD CHALLENGE",
            font=("Arial Black", 28, "bold"),
            fg=self.COLOR_ACENTO,
            bg=self.COLOR_TARJETA
        )
        title_label.pack(anchor="w")
        
        subtitle_label = tk.Label(
            title_frame,
            text="Juego en curso",
            font=("Segoe UI", 14),
            fg=self.COLOR_TEXTO_SECUNDARIO,
            bg=self.COLOR_TARJETA
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Contador de intentos
        attempts_frame = tk.Frame(header_frame, bg=self.COLOR_TARJETA)
        attempts_frame.pack(side="right", padx=30, pady=15)
        
        self.lbl_intentos = tk.Label(
            attempts_frame,
            text="",
            font=("Segoe UI", 20, "bold"),
            fg=self.COLOR_TEXTO,
            bg=self.COLOR_TARJETA
        )
        self.lbl_intentos.pack()
    
    def crear_seccion_palabra(self):
        """Crea la sección donde se muestra la palabra"""
        word_frame = tk.Frame(self.main_frame, bg=self.COLOR_FONDO)
        word_frame.pack(fill="x", pady=20)
        
        # Frame para las letras
        self.letters_container = tk.Frame(word_frame, bg=self.COLOR_FONDO)
        self.letters_container.pack()
        
        # Indicador de longitud
        self.lbl_longitud = tk.Label(
            word_frame,
            text="",
            font=("Segoe UI", 14),
            fg=self.COLOR_TEXTO_SECUNDARIO,
            bg=self.COLOR_FONDO
        )
        self.lbl_longitud.pack(pady=(20, 0))
        
        # Inicializar lista de labels de letras
        self.letra_labels = []
    
    def crear_seccion_progreso(self):
        """Crea la barra de progreso"""
        progress_frame = tk.Frame(self.main_frame, bg=self.COLOR_FONDO)
        progress_frame.pack(fill="x", pady=10)
        
        # Texto de progreso
        self.lbl_progreso_texto = tk.Label(
            progress_frame,
            text="Progreso: 0%",
            font=("Segoe UI", 12),
            fg=self.COLOR_TEXTO_SECUNDARIO,
            bg=self.COLOR_FONDO
        )
        self.lbl_progreso_texto.pack(anchor="w", pady=(0, 5))
        
        # Contenedor de la barra de progreso
        self.progress_container = tk.Frame(
            progress_frame,
            bg=self.COLOR_BORDE,
            height=10,
            relief="flat"
        )
        self.progress_container.pack(fill="x")
        
        # Barra de progreso (inicialmente vacía)
        self.progress_bar = tk.Frame(
            self.progress_container,
            bg=self.COLOR_PRIMARIO,
            height=10
        )
        self.progress_bar.place(x=0, y=0, width=0)
    
    def crear_seccion_entrada(self):
        """Crea la sección de entrada de letras"""
        input_frame = tk.Frame(self.main_frame, bg=self.COLOR_FONDO)
        input_frame.pack(fill="x", pady=30)
        
        # Frame para centrar
        input_center = tk.Frame(input_frame, bg=self.COLOR_FONDO)
        input_center.pack()
        
        tk.Label(
            input_center,
            text="INGRESA UNA LETRA:",
            font=("Segoe UI", 14, "bold"),
            fg=self.COLOR_TEXTO_SECUNDARIO,
            bg=self.COLOR_FONDO
        ).pack(pady=(0, 15))
        
        # Frame para entrada y botón
        entry_container = tk.Frame(input_center, bg=self.COLOR_FONDO)
        entry_container.pack()
        
        # Entrada de letra
        self.entry_letra = tk.Entry(
            entry_container,
            font=("Segoe UI", 36, "bold"),
            width=3,
            justify="center",
            bd=0,
            relief="flat",
            fg=self.COLOR_TEXTO,
            bg=self.COLOR_TARJETA,
            insertbackground=self.COLOR_ACENTO,
            highlightthickness=2,
            highlightbackground=self.COLOR_BORDE,
            highlightcolor=self.COLOR_PRIMARIO
        )
        self.entry_letra.pack(side="left", padx=(0, 20))
        self.entry_letra.focus_set()
        
        # Botón verificar
        self.btn_verificar = tk.Button(
            entry_container,
            text="✓ VERIFICAR",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg=self.COLOR_PRIMARIO,
            activeforeground="white",
            activebackground=self.COLOR_ACENTO,
            command=self.verificar_letra,
            width=14,
            height=1,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=20
        )
        self.btn_verificar.pack(side="left")
        
        # Efecto hover
        self.btn_verificar.bind("<Enter>", 
            lambda e: self.btn_verificar.config(bg=self.COLOR_ACENTO))
        self.btn_verificar.bind("<Leave>", 
            lambda e: self.btn_verificar.config(bg=self.COLOR_PRIMARIO))
    
    def crear_seccion_estadisticas(self):
        """Crea la sección de estadísticas"""
        stats_frame = tk.Frame(self.main_frame, bg=self.COLOR_FONDO)
        stats_frame.pack(fill="x", pady=20)
        
        # Frame para estadísticas en grid
        stats_grid = tk.Frame(stats_frame, bg=self.COLOR_FONDO)
        stats_grid.pack()
        
        # Letras usadas (columna izquierda)
        letters_card = tk.Frame(
            stats_grid,
            bg=self.COLOR_TARJETA,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDE,
            padx=20,
            pady=15
        )
        letters_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        tk.Label(
            letters_card,
            text="📝 LETRAS USADAS",
            font=("Segoe UI", 12, "bold"),
            fg=self.COLOR_TEXTO_SECUNDARIO,
            bg=self.COLOR_TARJETA
        ).pack(anchor="w", pady=(0, 10))
        
        self.lbl_usadas = tk.Label(
            letters_card,
            text="Ninguna",
            font=("Segoe UI", 14),
            fg=self.COLOR_TEXTO_SECUNDARIO,
            bg=self.COLOR_TARJETA,
            wraplength=300,
            justify="left"
        )
        self.lbl_usadas.pack(anchor="w")
        
        # Mensajes (columna central)
        message_card = tk.Frame(
            stats_grid,
            bg=self.COLOR_TARJETA,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDE,
            padx=20,
            pady=15
        )
        message_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        tk.Label(
            message_card,
            text="💡 MENSAJE",
            font=("Segoe UI", 12, "bold"),
            fg=self.COLOR_TEXTO_SECUNDARIO,
            bg=self.COLOR_TARJETA
        ).pack(anchor="w", pady=(0, 10))
        
        self.lbl_mensaje = tk.Label(
            message_card,
            text="¡Comienza adivinando!",
            font=("Segoe UI", 14),
            fg=self.COLOR_EXITO,
            bg=self.COLOR_TARJETA,
            wraplength=300,
            justify="left"
        )
        self.lbl_mensaje.pack(anchor="w")
        
        # Estadísticas (columna derecha)
        stats_card = tk.Frame(
            stats_grid,
            bg=self.COLOR_TARJETA,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDE,
            padx=20,
            pady=15
        )
        stats_card.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        tk.Label(
            stats_card,
            text="📊 ESTADÍSTICAS",
            font=("Segoe UI", 12, "bold"),
            fg=self.COLOR_TEXTO_SECUNDARIO,
            bg=self.COLOR_TARJETA
        ).pack(anchor="w", pady=(0, 10))
        
        self.lbl_estadisticas = tk.Label(
            stats_card,
            text="",
            font=("Segoe UI", 13),
            fg=self.COLOR_TEXTO,
            bg=self.COLOR_TARJETA,
            justify="left"
        )
        self.lbl_estadisticas.pack(anchor="w")
    
    def crear_seccion_controles(self):
        """Crea la sección de controles"""
        controls_frame = tk.Frame(self.main_frame, bg=self.COLOR_FONDO)
        controls_frame.pack(fill="x", pady=(30, 0))
        
        # Botón reiniciar (oculto inicialmente)
        self.btn_reiniciar = tk.Button(
            controls_frame,
            text="🔄 JUGAR DE NUEVO",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg=self.COLOR_SECUNDARIO,
            activeforeground="white",
            activebackground="#e86955",
            command=self.reiniciar_juego,
            width=20,
            height=2,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=20
        )
        # Se mostrará cuando termine el juego
        
        # Botón volver al menú
        self.btn_volver_menu = tk.Button(
            controls_frame,
            text="← VOLVER AL MENÚ",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg=self.COLOR_BORDE,
            activeforeground="white",
            activebackground=self.COLOR_TEXTO_SECUNDARIO,
            command=lambda: self.cerrar_ventana(self.master),
            width=18,
            height=1,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=15
        )
        self.btn_volver_menu.pack(side="left", padx=10)
        
        # Efecto hover
        self.btn_volver_menu.bind("<Enter>", 
            lambda e: self.btn_volver_menu.config(bg=self.COLOR_TEXTO_SECUNDARIO))
        self.btn_volver_menu.bind("<Leave>", 
            lambda e: self.btn_volver_menu.config(bg=self.COLOR_BORDE))
    
    def actualizar_display_palabra(self):
        """Actualiza el display visual de la palabra"""
        # Limpiar frame de letras
        for widget in self.letters_container.winfo_children():
            widget.destroy()
        
        self.letra_labels = []
        
        # Crear un cuadro para cada letra
        for i, letra in enumerate(self.juego.progreso):
            if letra == "_":
                # Cuadro vacío
                cuadro = tk.Frame(
                    self.letters_container,
                    width=60,
                    height=70,
                    bg=self.COLOR_TARJETA,
                    highlightthickness=2,
                    highlightbackground=self.COLOR_BORDE
                )
                cuadro.pack(side="left", padx=5, pady=5)
                cuadro.pack_propagate(False)
                
                lbl = tk.Label(
                    cuadro,
                    text="",
                    font=("Segoe UI", 24, "bold"),
                    fg=self.COLOR_TEXTO,
                    bg=self.COLOR_TARJETA
                )
                lbl.pack(expand=True)
            else:
                # Cuadro con letra adivinada
                cuadro = tk.Frame(
                    self.letters_container,
                    width=60,
                    height=70,
                    bg=self.COLOR_PRIMARIO,
                    highlightthickness=2,
                    highlightbackground=self.COLOR_PRIMARIO
                )
                cuadro.pack(side="left", padx=5, pady=5)
                cuadro.pack_propagate(False)
                
                lbl = tk.Label(
                    cuadro,
                    text=letra,
                    font=("Segoe UI", 24, "bold"),
                    fg="white",
                    bg=self.COLOR_PRIMARIO
                )
                lbl.pack(expand=True)
            
            self.letra_labels.append(lbl)
    
    def actualizar_interfaz(self):
        """Actualiza todos los elementos de la interfaz"""
        # Actualizar display de palabra
        self.actualizar_display_palabra()
        
        # Actualizar información
        self.lbl_longitud.config(text=f"📏 Palabra de {self.juego.get_longitud()} letras")
        
        intentos = self.juego.get_intentos_restantes()
        total_intentos = self.juego.get_intentos_totales()
        self.lbl_intentos.config(text=f"❤️  {intentos}/{total_intentos} INTENTOS")
        
        # Actualizar barra de progreso
        porcentaje = self.juego.get_progreso_porcentaje()
        self.lbl_progreso_texto.config(text=f"Progreso: {porcentaje}%")
        
        # Actualizar ancho de barra de progreso
        if self.progress_container.winfo_width() > 0:
            ancho_total = self.progress_container.winfo_width()
            ancho_progreso = (ancho_total * porcentaje) // 100
            self.progress_bar.config(width=ancho_progreso)
        
        # Actualizar estadísticas
        self.lbl_usadas.config(
            text=self.juego.get_letras_usadas() or "Ninguna",
            fg=self.COLOR_TEXTO if self.juego.letras_usadas else self.COLOR_TEXTO_SECUNDARIO
        )
        
        # Actualizar estadísticas rápidas
        estadisticas_texto = f"""
        • Letras adivinadas: {sum(1 for l in self.juego.progreso if l != '_')}
        • Letras restantes: {self.juego.progreso.count('_')}
        • Intentos usados: {total_intentos - intentos}
        • Porcentaje: {porcentaje}%
        """
        self.lbl_estadisticas.config(text=estadisticas_texto.strip())
        
        # Habilitar controles
        self.entry_letra.config(state="normal", fg=self.COLOR_TEXTO)
        self.btn_verificar.config(state="normal", bg=self.COLOR_PRIMARIO)
        self.entry_letra.focus_set()
        
        # Ocultar botón reiniciar
        self.btn_reiniciar.place_forget()
    
    def verificar_letra(self):
        """Verifica la letra ingresada por el jugador"""
        if self.juego.intentos <= 0:
            self.lbl_mensaje.config(text="El juego terminó. ¡Reinicia!", fg=self.COLOR_ERROR)
            return
        
        letra = self.entry_letra.get()
        self.entry_letra.delete(0, tk.END)
        
        if not letra:
            self.lbl_mensaje.config(text="Por favor, ingresa una letra", fg=self.COLOR_ADVERTENCIA)
            return
        
        # Usar la lógica del juego
        acierto, mensaje, es_ganador = self.juego.comprobar_letra(letra)
        
        # Actualizar mensaje
        if "ya fue usada" in mensaje or "Ingresa solo" in mensaje:
            color = self.COLOR_ADVERTENCIA
        elif acierto:
            color = self.COLOR_EXITO
        else:
            color = self.COLOR_ERROR
        
        self.lbl_mensaje.config(text=mensaje, fg=color)
        
        # Actualizar interfaz
        self.actualizar_interfaz()
        
        # Verificar fin del juego
        if es_ganador:
            self.finalizar_juego(victoria=True)
        elif self.juego.intentos == 0:
            self.finalizar_juego(victoria=False)
    
    def finalizar_juego(self, victoria):
        """Finaliza el juego y muestra el resultado"""
        # Deshabilitar controles
        self.entry_letra.config(state="disabled", fg=self.COLOR_TEXTO_SECUNDARIO)
        self.btn_verificar.config(state="disabled", bg=self.COLOR_TEXTO_SECUNDARIO)
        
        # Mostrar mensaje final
        if victoria:
            mensaje_final = f"🎉 ¡FELICIDADES! 🎉\nHas adivinado la palabra:\n{self.juego.get_palabra()}"
            color_final = self.COLOR_EXITO
            
            # Efecto visual: cambiar todos los cuadros a color de éxito
            for lbl in self.letra_labels:
                lbl.master.config(bg=self.COLOR_EXITO, highlightbackground=self.COLOR_EXITO)
                lbl.config(bg=self.COLOR_EXITO, fg="white")
        else:
            mensaje_final = f"💀 ¡GAME OVER! 💀\nLa palabra era:\n{self.juego.get_palabra()}"
            color_final = self.COLOR_ERROR
            
            # Mostrar palabra completa en rojo
            self.actualizar_display_palabra()
            for i, lbl in enumerate(self.letra_labels):
                letra_correcta = self.juego.palabra[i]
                lbl.config(text=letra_correcta)
                lbl.master.config(bg=self.COLOR_ERROR, highlightbackground=self.COLOR_ERROR)
                lbl.config(bg=self.COLOR_ERROR, fg="white")
        
        self.lbl_mensaje.config(text=mensaje_final, fg=color_final)
        
        # Mostrar botón reiniciar centrado
        self.btn_reiniciar.place(relx=0.5, rely=0.97, anchor="center")
        
        # Efecto hover para botón reiniciar
        self.btn_reiniciar.bind("<Enter>", 
            lambda e: self.btn_reiniciar.config(bg="#e86955"))
        self.btn_reiniciar.bind("<Leave>", 
            lambda e: self.btn_reiniciar.config(bg=self.COLOR_SECUNDARIO))
    
    def reiniciar_juego(self):
        """Reinicia el juego completamente"""
        self.juego.seleccionar_palabra()
        self.actualizar_interfaz()
        self.lbl_mensaje.config(text="¡Nuevo juego! Ingresa tu primera letra.", fg=self.COLOR_EXITO)
    
    def cerrar_ventana(self, parent):
        """Cierra la ventana del juego y muestra el menú principal"""
        parent.deiconify()  # Mostrar ventana principal
        self.destroy()  # Cerrar ventana del juego