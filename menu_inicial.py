# menu_inicial.py
import tkinter as tk
from tkinter import messagebox, PhotoImage
import sys
import os
from juego_app import JuegoPalabrasApp
from gestor_bd import GestorBaseDatos
from configuracion import Configuracion

class MenuInicial:
    """Clase que maneja el menú inicial del juego"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 DESAFÍO DE PALABRAS - Menú Principal")
        
        # Configurar tamaño y posición
        self.root.geometry("900x700+100+100")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")
        
        # Cargar configuración y base de datos
        self.config = Configuracion()
        self.gestor_db = GestorBaseDatos()
        
        # Cargar estadísticas iniciales
        self.estadisticas = self.gestor_db.obtener_estadisticas()
        
        # Intentar cargar íconos
        self.iconos = {}
        self.cargar_iconos()
        
        # Configurar interfaz
        self.configurar_interfaz()
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Configurar cierre
        self.root.protocol("WM_DELETE_WINDOW", self.salir)
    
    def cargar_iconos(self):
        """Intenta cargar íconos para los botones"""
        # Si hay íconos en la carpeta 'iconos', los carga
        # Si no, usa íconos de texto
        iconos_nombres = {
            'jugar': '🎮',
            'configuracion': '⚙️',
            'estadisticas': '📊',
            'ayuda': '❓',
            'acerca': 'ℹ️',
            'salir': '🚪'
        }
        
        self.iconos = iconos_nombres
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def configurar_interfaz(self):
        """Configura la interfaz del menú inicial"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Encabezado
        self.crear_encabezado(main_frame)
        
        # Panel de estadísticas rápidas
        self.crear_panel_estadisticas(main_frame)
        
        # Panel de botones principales
        self.crear_panel_botones(main_frame)
        
        # Panel inferior
        self.crear_panel_inferior(main_frame)
    
    def crear_encabezado(self, parent):
        """Crea el encabezado del menú"""
        header_frame = tk.Frame(parent, bg="#0f3460", height=150)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Título principal
        titulo = tk.Label(
            header_frame,
            text="🎮 DESAFÍO DE PALABRAS",
            font=("Arial", 36, "bold"),
            fg="#e94560",
            bg="#0f3460"
        )
        titulo.pack(expand=True)
        
        # Subtítulo
        subtitulo = tk.Label(
            header_frame,
            text="El juego definitivo para adivinar palabras",
            font=("Arial", 14, "italic"),
            fg="#f0f0f0",
            bg="#0f3460"
        )
        subtitulo.pack(pady=(0, 20))
    
    def crear_panel_estadisticas(self, parent):
        """Crea el panel de estadísticas rápidas"""
        stats_frame = tk.Frame(parent, bg="#16213e", relief=tk.RAISED, bd=3)
        stats_frame.pack(fill=tk.X, pady=(0, 30), padx=10)
        
        # Título del panel
        tk.Label(
            stats_frame,
            text="📊 TUS ESTADÍSTICAS",
            font=("Arial", 16, "bold"),
            fg="#e94560",
            bg="#16213e",
            pady=10
        ).pack()
        
        # Grid para estadísticas
        stats_grid = tk.Frame(stats_frame, bg="#16213e")
        stats_grid.pack(pady=(0, 15), padx=20)
        
        # Estadísticas en 2 columnas
        stats_data = [
            ("🎮 Partidas totales:", f"{self.estadisticas['partidas_totales']}", "#4cc9f0"),
            ("✅ Victorias:", f"{self.estadisticas['victorias']}", "#4ade80"),
            ("❌ Derrotas:", f"{self.estadisticas['derrotas']}", "#f87171"),
            ("🎯 Promedio intentos:", f"{self.estadisticas['promedio_intentos']}", "#fbbf24"),
        ]
        
        for i, (label, value, color) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            
            frame = tk.Frame(stats_grid, bg="#16213e")
            frame.grid(row=row, column=col, sticky="w", padx=20, pady=10)
            
            tk.Label(
                frame,
                text=label,
                font=("Arial", 11),
                fg="#a5b4cb",
                bg="#16213e"
            ).pack(side=tk.LEFT)
            
            tk.Label(
                frame,
                text=value,
                font=("Arial", 12, "bold"),
                fg=color,
                bg="#16213e"
            ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Dificultad actual
        dif_frame = tk.Frame(stats_frame, bg="#16213e")
        dif_frame.pack(pady=(0, 15), padx=20)
        
        dificultad = self.config.obtener("dificultad", "MEDIO")
        colores_dif = {"FACIL": "#4ade80", "MEDIO": "#fbbf24", "DIFICIL": "#f87171"}
        
        tk.Label(
            dif_frame,
            text="🎯 Dificultad actual:",
            font=("Arial", 11),
            fg="#a5b4cb",
            bg="#16213e"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            dif_frame,
            text=dificultad,
            font=("Arial", 12, "bold"),
            fg=colores_dif.get(dificultad, "#fbbf24"),
            bg="#16213e"
        ).pack(side=tk.LEFT, padx=(10, 0))
    
    def crear_panel_botones(self, parent):
        """Crea el panel con los botones principales"""
        buttons_frame = tk.Frame(parent, bg="#1a1a2e")
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuración de botones
        botones_info = [
            ("🎮 JUGAR", self.iniciar_juego, 
             "Iniciar una nueva partida", "#4ade80", "white"),
            
            ("⚙️ CONFIGURACIÓN", self.abrir_configuracion,
             "Configurar opciones del juego", "#3b82f6", "white"),
            
            ("📊 ESTADÍSTICAS COMPLETAS", self.abrir_estadisticas,
             "Ver estadísticas detalladas", "#8b5cf6", "white"),
            
            ("❓ CÓMO JUGAR", self.mostrar_ayuda,
             "Ver instrucciones del juego", "#f59e0b", "white"),
            
            ("ℹ️ ACERCA DE", self.mostrar_acerca_de,
             "Información sobre el juego", "#10b981", "white"),
            
            ("🚪 SALIR", self.salir,
             "Salir del juego", "#ef4444", "white")
        ]
        
        # Crear botones en grid 2x3
        for i, (texto, comando, tooltip, bg_color, fg_color) in enumerate(botones_info):
            row = i // 3
            col = i % 3
            
            # Frame para el botón
            btn_frame = tk.Frame(buttons_frame, bg="#1a1a2e", padx=10, pady=10)
            btn_frame.grid(row=row, column=col, sticky="nsew")
            
            # Configurar expansión de columnas
            buttons_frame.grid_columnconfigure(col, weight=1)
            buttons_frame.grid_rowconfigure(row, weight=1)
            
            # Botón principal
            btn = tk.Button(
                btn_frame,
                text=texto,
                font=("Arial", 14, "bold"),
                bg=bg_color,
                fg=fg_color,
                padx=20,
                pady=15,
                command=comando,
                cursor="hand2",
                relief=tk.RAISED,
                bd=3,
                width=15
            )
            btn.pack(fill=tk.BOTH, expand=True)
            
            # Tooltip (texto descriptivo)
            tk.Label(
                btn_frame,
                text=tooltip,
                font=("Arial", 9, "italic"),
                fg="#a5b4cb",
                bg="#1a1a2e",
                wraplength=200
            ).pack(pady=(5, 0))
    
    def crear_panel_inferior(self, parent):
        """Crea el panel inferior del menú"""
        footer_frame = tk.Frame(parent, bg="#0f3460", height=80)
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        footer_frame.pack_propagate(False)
        
        # Información de versión
        tk.Label(
            footer_frame,
            text="Desafío de Palabras v2.0 | © 2024",
            font=("Arial", 10),
            fg="#a5b4cb",
            bg="#0f3460"
        ).pack(side=tk.LEFT, padx=20)
        
        # Información de dificultad
        dificultad = self.config.obtener("dificultad", "MEDIO")
        tk.Label(
            footer_frame,
            text=f"Dificultad actual: {dificultad}",
            font=("Arial", 10, "bold"),
            fg="#e94560",
            bg="#0f3460"
        ).pack(side=tk.RIGHT, padx=20)
    
    def iniciar_juego(self):
        """Inicia el juego principal"""
        # Ocultar menú inicial
        self.root.withdraw()
        
        # Crear nueva ventana para el juego
        juego_window = tk.Toplevel(self.root)
        juego_window.title("🎮 DESAFÍO DE PALABRAS - En Juego")
        
        # Configurar juego
        juego_app = JuegoPalabrasApp(juego_window)
        
        # Configurar qué pasa cuando se cierra el juego
        def on_juego_close():
            juego_window.destroy()
            self.actualizar_estadisticas()
            self.root.deiconify()  # Mostrar menú principal nuevamente
        
        juego_window.protocol("WM_DELETE_WINDOW", on_juego_close)
        
        # Centrar ventana del juego
        juego_window.update_idletasks()
        width = juego_window.winfo_width()
        height = juego_window.winfo_height()
        x = (juego_window.winfo_screenwidth() // 2) - (width // 2)
        y = (juego_window.winfo_screenheight() // 2) - (height // 2)
        juego_window.geometry(f'{width}x{height}+{x}+{y}')
    
    def abrir_configuracion(self):
        """Abre la ventana de configuración"""
        config_window = tk.Toplevel(self.root)
        config_window.title("⚙️ Configuración del Juego")
        config_window.geometry("500x600")
        config_window.configure(bg="#1a1a2e")
        config_window.resizable(False, False)
        
        # Centrar ventana
        config_window.update_idletasks()
        width = config_window.winfo_width()
        height = config_window.winfo_height()
        x = (config_window.winfo_screenwidth() // 2) - (width // 2)
        y = (config_window.winfo_screenheight() // 2) - (height // 2)
        config_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Frame principal
        main_frame = tk.Frame(config_window, bg="#1a1a2e", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(
            main_frame,
            text="⚙️ CONFIGURACIÓN DEL JUEGO",
            font=("Arial", 20, "bold"),
            fg="#e94560",
            bg="#1a1a2e"
        ).pack(pady=(0, 20))
        
        # Sección de dificultad
        dif_frame = tk.LabelFrame(
            main_frame,
            text="🎮 NIVEL DE DIFICULTAD",
            font=("Arial", 12, "bold"),
            bg="#16213e",
            fg="#a5b4cb",
            padx=15,
            pady=15
        )
        dif_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Variable para dificultad
        self.var_dificultad = tk.StringVar(value=self.config.obtener("dificultad", "MEDIO"))
        
        # Botones de radio para dificultad
        dificultades = [
            ("🟢 FÁCIL", "FACIL", "#4ade80"),
            ("🟡 MEDIO", "MEDIO", "#fbbf24"),
            ("🔴 DIFÍCIL", "DIFICIL", "#f87171")
        ]
        
        for texto, valor, color in dificultades:
            frame = tk.Frame(dif_frame, bg="#16213e")
            frame.pack(fill=tk.X, pady=5)
            
            rb = tk.Radiobutton(
                frame,
                text=texto,
                variable=self.var_dificultad,
                value=valor,
                font=("Arial", 11, "bold"),
                bg="#16213e",
                fg=color,
                selectcolor="#16213e",
                activebackground="#16213e",
                activeforeground=color,
                cursor="hand2"
            )
            rb.pack(side=tk.LEFT)
            
            # Descripción
            descripciones = {
                "FACIL": "• 8 intentos • Pistas generosas",
                "MEDIO": "• 6 intentos • Pistas moderadas",
                "DIFICIL": "• 4 intentos • Pistas limitadas"
            }
            
            tk.Label(
                frame,
                text=descripciones[valor],
                font=("Arial", 9),
                fg="#a5b4cb",
                bg="#16213e"
            ).pack(side=tk.LEFT, padx=(20, 0))
        
        # Otras configuraciones
        otras_frame = tk.LabelFrame(
            main_frame,
            text="🔧 OTRAS CONFIGURACIONES",
            font=("Arial", 12, "bold"),
            bg="#16213e",
            fg="#a5b4cb",
            padx=15,
            pady=15
        )
        otras_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Número de intentos
        intentos_frame = tk.Frame(otras_frame, bg="#16213e")
        intentos_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            intentos_frame,
            text="Número de intentos:",
            font=("Arial", 11),
            fg="#a5b4cb",
            bg="#16213e",
            width=20,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.spin_intentos = tk.Spinbox(
            intentos_frame,
            from_=3,
            to=15,
            width=10,
            font=("Arial", 11),
            bg="#0f3460",
            fg="white",
            bd=2,
            relief=tk.SUNKEN
        )
        self.spin_intentos.pack(side=tk.LEFT)
        self.spin_intentos.delete(0, tk.END)
        self.spin_intentos.insert(0, str(self.config.obtener("max_intentos", 6)))
        
        # Mostrar pistas
        self.var_pistas = tk.BooleanVar(value=self.config.obtener("mostrar_pistas", True))
        pistas_check = tk.Checkbutton(
            otras_frame,
            text="Mostrar pistas durante el juego",
            variable=self.var_pistas,
            font=("Arial", 11),
            fg="#a5b4cb",
            bg="#16213e",
            selectcolor="#16213e",
            activebackground="#16213e",
            activeforeground="#a5b4cb",
            cursor="hand2"
        )
        pistas_check.pack(anchor=tk.W, pady=5)
        
        # Mostrar tiempo
        self.var_tiempo = tk.BooleanVar(value=self.config.obtener("mostrar_tiempo", True))
        tiempo_check = tk.Checkbutton(
            otras_frame,
            text="Mostrar temporizador",
            variable=self.var_tiempo,
            font=("Arial", 11),
            fg="#a5b4cb",
            bg="#16213e",
            selectcolor="#16213e",
            activebackground="#16213e",
            activeforeground="#a5b4cb",
            cursor="hand2"
        )
        tiempo_check.pack(anchor=tk.W, pady=5)
        
        # Frame para botones
        btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botón aplicar
        tk.Button(
            btn_frame,
            text="💾 APLICAR CAMBIOS",
            font=("Arial", 12, "bold"),
            bg="#4ade80",
            fg="white",
            padx=20,
            pady=10,
            command=self.aplicar_configuracion,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Botón cancelar
        tk.Button(
            btn_frame,
            text="❌ CANCELAR",
            font=("Arial", 12),
            bg="#ef4444",
            fg="white",
            padx=20,
            pady=10,
            command=config_window.destroy,
            cursor="hand2"
        ).pack(side=tk.RIGHT, padx=5)
    
    def aplicar_configuracion(self):
        """Aplica los cambios de configuración"""
        try:
            # Guardar dificultad
            self.config.establecer("dificultad", self.var_dificultad.get())
            
            # Guardar intentos
            intentos = int(self.spin_intentos.get())
            self.config.establecer("max_intentos", intentos)
            
            # Guardar otras configuraciones
            self.config.establecer("mostrar_pistas", self.var_pistas.get())
            self.config.establecer("mostrar_tiempo", self.var_tiempo.get())
            
            # Actualizar estadísticas en pantalla
            self.actualizar_estadisticas()
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "✅ Configuración Guardada",
                "Los cambios se han aplicado correctamente.\n\n"
                f"Dificultad: {self.var_dificultad.get()}\n"
                f"Intentos máximos: {intentos}"
            )
            
            # Cerrar ventana de configuración
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    widget.destroy()
            
        except ValueError:
            messagebox.showerror(
                "❌ Error",
                "Por favor, introduce un número válido para los intentos (3-15)."
            )
    
    def abrir_estadisticas(self):
        """Abre ventana con estadísticas completas"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Estadísticas Completas")
        stats_window.geometry("700x500")
        stats_window.configure(bg="#1a1a2e")
        
        # Centrar ventana
        stats_window.update_idletasks()
        width = stats_window.winfo_width()
        height = stats_window.winfo_height()
        x = (stats_window.winfo_screenwidth() // 2) - (width // 2)
        y = (stats_window.winfo_screenheight() // 2) - (height // 2)
        stats_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()
        
        # Frame principal
        main_frame = tk.Frame(stats_window, bg="#1a1a2e", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(
            main_frame,
            text="📊 ESTADÍSTICAS COMPLETAS",
            font=("Arial", 20, "bold"),
            fg="#e94560",
            bg="#1a1a2e"
        ).pack(pady=(0, 20))
        
        # Frame para estadísticas generales
        gen_frame = tk.LabelFrame(
            main_frame,
            text="📈 ESTADÍSTICAS GENERALES",
            font=("Arial", 12, "bold"),
            bg="#16213e",
            fg="#a5b4cb",
            padx=15,
            pady=15
        )
        gen_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Mostrar estadísticas generales
        stats_text = f"""
        • 🎮 Partidas totales: {self.estadisticas['partidas_totales']}
        • ✅ Victorias: {self.estadisticas['victorias']}
        • ❌ Derrotas: {self.estadisticas['derrotas']}
        • 🎯 Promedio de intentos (victorias): {self.estadisticas['promedio_intentos']:.2f}
        """
        
        tk.Label(
            gen_frame,
            text=stats_text,
            font=("Consolas", 11),
            fg="#a5b4cb",
            bg="#16213e",
            justify=tk.LEFT
        ).pack(anchor=tk.W)
        
        # Frame para estadísticas por dificultad
        dif_frame = tk.LabelFrame(
            main_frame,
            text="🎮 ESTADÍSTICAS POR DIFICULTAD",
            font=("Arial", 12, "bold"),
            bg="#16213e",
            fg="#a5b4cb",
            padx=15,
            pady=15
        )
        dif_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Mostrar estadísticas por dificultad
        dif_text = ""
        for dificultad, datos in self.estadisticas["por_dificultad"].items():
            if datos['total'] > 0:
                porcentaje = datos['porcentaje']
                dif_text += f"\n• {dificultad.upper()}: {datos['victorias']}/{datos['total']} ({porcentaje}%)"
            else:
                dif_text += f"\n• {dificultad.upper()}: Sin partidas jugadas"
        
        tk.Label(
            dif_frame,
            text=dif_text.strip(),
            font=("Consolas", 11),
            fg="#a5b4cb",
            bg="#16213e",
            justify=tk.LEFT
        ).pack(anchor=tk.W)
        
        # Botón cerrar
        tk.Button(
            main_frame,
            text="CERRAR",
            font=("Arial", 12, "bold"),
            bg="#ef4444",
            fg="white",
            padx=30,
            pady=10,
            command=stats_window.destroy,
            cursor="hand2"
        ).pack(pady=10)
    
    def mostrar_ayuda(self):
        """Muestra las instrucciones del juego"""
        ayuda_texto = """
        🎮 CÓMO JUGAR A DESAFÍO DE PALABRAS 🎮

        OBJETIVO:
        Adivinar la palabra secreta antes de agotar todos los intentos.

        INSTRUCCIONES:
        1. Selecciona "JUGAR" en el menú principal
        2. Elige una letra en el teclado
        3. Si la letra está en la palabra, se revelará
        4. Si no está, perderás un intento
        5. Adivina todas las letras para ganar

        DIFICULTADES:
        • 🟢 FÁCIL: 8 intentos, palabras cortas
        • 🟡 MEDIO: 6 intentos, palabras medias
        • 🔴 DIFÍCIL: 4 intentos, palabras largas

        CONSEJOS:
        • Empieza con vocales (A, E, I, O, U)
        • Sigue con consonantes comunes
        • Usa las pistas estratégicamente
        • Practica en diferentes dificultades

        ¡DIVIÉRTETE Y MEJORA TU VOCABULARIO! 📚
        """
        
        messagebox.showinfo("❓ Cómo Jugar", ayuda_texto)
    
    def mostrar_acerca_de(self):
        """Muestra información acerca del juego"""
        acerca_texto = """
        🎮 DESAFÍO DE PALABRAS v2.0

        DESCRIPCIÓN:
        Juego educativo diseñado para mejorar el vocabulario
        mientras te diviertes adivinando palabras secretas.

        CARACTERÍSTICAS:
        ✅ 3 niveles de dificultad
        ✅ Sistema de estadísticas
        ✅ Ranking de mejores jugadores
        ✅ Configuración personalizable
        ✅ Interfaz moderna y amigable

        DESARROLLADO CON:
        • Python 3.x
        • Tkinter para la interfaz
        • SQLite para la base de datos

        CRÉDITOS:
        Desarrollado como proyecto educativo
        para mejorar habilidades de programación.

        © 2024 - Todos los derechos reservados

        ¡GRACIAS POR JUGAR! 🎉
        """
        
        messagebox.showinfo("ℹ️ Acerca de", acerca_texto)
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas desde la base de datos"""
        self.estadisticas = self.gestor_db.obtener_estadisticas()
    
    def salir(self):
        """Sale del juego con confirmación"""
        respuesta = messagebox.askyesno(
            "👋 Salir del Juego",
            "¿Estás seguro de que quieres salir de Desafío de Palabras?\n\n"
            "Tu progreso y estadísticas se guardarán automáticamente."
        )
        
        if respuesta:
            # Guardar configuración
            self.config.guardar_configuracion()
            
            # Cerrar base de datos
            self.gestor_db.cerrar()
            
            # Cerrar aplicación
            self.root.quit()
            self.root.destroy()