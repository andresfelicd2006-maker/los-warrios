# juego_app.py
import tkinter as tk
from tkinter import messagebox, Menu
import sys
import os

# Importar las otras clases
from gestor_bd import GestorBaseDatos
from configuracion import Configuracion
from juego_logica import JuegoLogica
from panel_juego import PanelJuego
from panel_estadisticas import PanelEstadisticas
from panel_configuracion import PanelConfiguracion

class JuegoPalabrasApp:
    """Clase principal que coordina todas las partes del juego"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 DESAFÍO DE PALABRAS - En Juego")
        
        # Configurar tamaño inicial de ventana
        self.root.geometry("1100x750")
        self.root.minsize(1000, 650)
        
        # Configurar colores del menú inicial
        self.colores = {
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
        
        # Configurar ícono de ventana
        try:
            self.root.iconbitmap(default="icon.ico")
        except:
            pass
        
        # Inicializar componentes principales
        self.gestor_db = GestorBaseDatos()
        self.config = Configuracion()
        self.juego_logica = JuegoLogica(self.gestor_db, self.config)
        
        # Configurar interfaz
        self.configurar_menu()
        self.configurar_interfaz()
        
        # Centrar foco en entrada
        self.root.after(100, self.panel_juego.focus_entrada)
        
        # Configurar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.salir)
        
        # Centrar ventana
        self.centrar_ventana()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def configurar_menu(self):
        """Configura la barra de menú de la aplicación"""
        menubar = Menu(self.root, bg=self.colores["fondo_secundario"], fg=self.colores["texto_principal"])
        self.root.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = Menu(menubar, tearoff=0, bg=self.colores["fondo_secundario"], 
                           fg=self.colores["texto_principal"], activebackground=self.colores["acento_principal"])
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nuevo Juego", command=self.nuevo_juego, accelerator="Ctrl+N")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Volver al Menú Principal", command=self.volver_menu_principal)
        menu_archivo.add_command(label="Salir", command=self.salir, accelerator="Ctrl+Q")
        
        # Menú Juego
        menu_juego = Menu(menubar, tearoff=0, bg=self.colores["fondo_secundario"], 
                         fg=self.colores["texto_principal"], activebackground=self.colores["acento_principal"])
        menubar.add_cascade(label="Juego", menu=menu_juego)
        
        # Submenú Dificultad
        menu_dificultad = Menu(menu_juego, tearoff=0, bg=self.colores["fondo_secundario"], 
                              fg=self.colores["texto_principal"], activebackground=self.colores["acento_principal"])
        menu_juego.add_cascade(label="Cambiar Dificultad", menu=menu_dificultad)
        
        self.var_dificultad_menu = tk.StringVar(value=self.config.obtener("dificultad"))
        dificultades = [("🟢 Fácil", "FACIL"), ("🟡 Medio", "MEDIO"), ("🔴 Difícil", "DIFICIL")]
        
        for texto, valor in dificultades:
            menu_dificultad.add_radiobutton(
                label=texto, 
                variable=self.var_dificultad_menu,
                value=valor, 
                command=lambda v=valor: self.cambiar_dificultad(v)
            )
        
        menu_juego.add_separator()
        menu_juego.add_command(label="Ver Ranking", command=self.mostrar_ranking)
        menu_juego.add_command(label="Estadísticas Completas", command=self.mostrar_estadisticas_completas)
        
        # Menú Ayuda
        menu_ayuda = Menu(menubar, tearoff=0, bg=self.colores["fondo_secundario"], 
                         fg=self.colores["texto_principal"], activebackground=self.colores["acento_principal"])
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Cómo Jugar", command=self.mostrar_ayuda)
        menu_ayuda.add_command(label="Reglas del Juego", command=self.mostrar_reglas)
        menu_ayuda.add_separator()
        menu_ayuda.add_command(label="Acerca de...", command=self.mostrar_acerca_de)
        
        # Atajos de teclado
        self.root.bind("<Control-n>", lambda e: self.nuevo_juego())
        self.root.bind("<Control-N>", lambda e: self.nuevo_juego())
        self.root.bind("<Control-q>", lambda e: self.salir())
        self.root.bind("<Control-Q>", lambda e: self.salir())
        self.root.bind("<F1>", lambda e: self.mostrar_ayuda())
        self.root.bind("<F2>", lambda e: self.nuevo_juego())
        self.root.bind("<Escape>", lambda e: self.volver_menu_principal())
    
    def configurar_interfaz(self):
        """Configura la interfaz principal de la aplicación"""
        # Configurar color de fondo
        self.root.configure(bg=self.colores["fondo_principal"])
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colores["fondo_principal"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame superior (cabecera)
        header_frame = tk.Frame(main_frame, bg=self.colores["fondo_terciario"], height=100)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Título principal
        titulo_label = tk.Label(
            header_frame,
            text="🎮 DESAFÍO DE PALABRAS",
            font=("Arial", 28, "bold"),
            fg=self.colores["acento_principal"],
            bg=self.colores["fondo_terciario"]
        )
        titulo_label.pack(expand=True)
        
        # Subtítulo
        self.subtitulo_label = tk.Label(
            header_frame,
            text=f"En juego | Dificultad: {self.config.obtener('dificultad')}",
            font=("Arial", 11, "italic"),
            fg=self.colores["texto_secundario"],
            bg=self.colores["fondo_terciario"]
        )
        self.subtitulo_label.pack(pady=(0, 10))
        
        # Frame para contenido principal (2 columnas)
        content_frame = tk.Frame(main_frame, bg=self.colores["fondo_principal"])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda (75%) - Juego
        left_frame = tk.Frame(content_frame, bg=self.colores["fondo_principal"])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Panel de juego
        game_container = tk.Frame(left_frame, bg=self.colores["fondo_secundario"], 
                                 relief=tk.RAISED, bd=3)
        game_container.pack(fill=tk.BOTH, expand=True)
        
        self.panel_juego = PanelJuego(game_container, self.juego_logica, 
                                     self.procesar_intento_jugador, self.colores)
        self.panel_juego.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Columna derecha (25%) - Paneles laterales
        right_frame = tk.Frame(content_frame, bg=self.colores["fondo_principal"], width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        # Panel de estadísticas (ahora más grande)
        stats_container = tk.LabelFrame(
            right_frame,
            text="📊 PANEL DE ESTADÍSTICAS",
            font=("Arial", 11, "bold"),
            bg=self.colores["fondo_secundario"],
            fg=self.colores["texto_secundario"],
            padx=10,
            pady=10,
            relief=tk.RAISED,
            bd=2
        )
        stats_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Hacer el panel de estadísticas más alto
        stats_container.pack_propagate(False)
        stats_container.config(height=400)

        self.panel_estadisticas = PanelEstadisticas(stats_container, self.gestor_db, self.colores)
        self.panel_estadisticas.pack(fill=tk.BOTH, expand=True)
        
        # Panel de configuración
        config_container = tk.LabelFrame(
            right_frame,
            text="⚙️ Configuración",
            font=("Arial", 11, "bold"),
            bg=self.colores["fondo_secundario"],
            fg=self.colores["texto_secundario"],
            padx=10,
            pady=10
        )
        config_container.pack(fill=tk.BOTH, expand=True)
        
        self.panel_configuracion = PanelConfiguracion(
            config_container,
            self.config,
            self.on_configuracion_cambiada,
            self.colores
        )
        self.panel_configuracion.pack(fill=tk.BOTH, expand=True)
        
        # Frame inferior (botones de control)
        control_frame = tk.Frame(main_frame, bg=self.colores["fondo_principal"], height=60)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        control_frame.pack_propagate(False)
        
        # Botones de control
        botones_info = [
            ("🔄 NUEVO JUEGO", self.nuevo_juego, self.colores["verde"], "white"),
            ("🏠 MENÚ PRINCIPAL", self.volver_menu_principal, self.colores["azul"], "white"),
            ("🏆 RANKING", self.mostrar_ranking, self.colores["amarillo"], "#212529"),
            ("📈 ESTADÍSTICAS", self.mostrar_estadisticas_completas, self.colores["acento_secundario"], "white"),
            ("❓ AYUDA", self.mostrar_ayuda, self.colores["morado"], "white"),
            ("❌ SALIR", self.salir, self.colores["rojo"], "white")
        ]
        
        for texto, comando, bg_color, fg_color in botones_info:
            btn = tk.Button(
                control_frame,
                text=texto,
                font=("Arial", 10, "bold"),
                bg=bg_color,
                fg=fg_color,
                padx=15,
                pady=8,
                command=comando,
                cursor="hand2",
                relief=tk.RAISED,
                bd=2,
                activebackground=bg_color,
                activeforeground=fg_color
            )
            btn.pack(side=tk.LEFT, padx=5, pady=10)
    
    def procesar_intento_jugador(self, entrada: str):
        """Procesa un intento del jugador"""
        resultado = self.juego_logica.procesar_intento(entrada)
        
        # Actualizar panel de juego
        self.panel_juego.actualizar_panel()
        
        # Manejar resultados especiales
        if resultado["estado"] == "victoria":
            messagebox.showinfo("🎉 ¡VICTORIA!", resultado["mensaje"])
            self.panel_estadisticas.actualizar_estadisticas()
            self.actualizar_subtitulo(victoria=True)
            
        elif resultado["estado"] == "derrota":
            messagebox.showerror("💀 ¡FIN DEL JUEGO!", 
                               f"{resultado['mensaje']}\n\n"
                               f"Intentos usados: {resultado['intentos']}\n"
                               f"Tiempo: {resultado['tiempo']} segundos")
            self.panel_estadisticas.actualizar_estadisticas()
            self.actualizar_subtitulo(victoria=False)
            
        elif resultado["estado"] == "error":
            messagebox.showwarning("⚠️ Atención", resultado["mensaje"])
    
    def nuevo_juego(self):
        """Inicia un nuevo juego"""
        self.juego_logica.reiniciar_juego()
        self.panel_juego.actualizar_panel()
        self.actualizar_subtitulo()
        self.panel_juego.focus_entrada()
        
        # Actualizar dificultad en menú
        self.var_dificultad_menu.set(self.config.obtener("dificultad"))
    
    def on_configuracion_cambiada(self):
        """Se ejecuta cuando cambia la configuración"""
        # Actualizar la lógica del juego con nueva configuración
        self.juego_logica.max_intentos = self.config.obtener("max_intentos")
        self.juego_logica.cambiar_dificultad(self.config.obtener("dificultad"))
        
        # Actualizar subtítulo
        self.actualizar_subtitulo()
        
        # Actualizar dificultad en menú
        self.var_dificultad_menu.set(self.config.obtener("dificultad"))
        
        # Si hay un juego en curso, preguntar si reiniciar
        if not self.juego_logica.game_over:
            respuesta = messagebox.askyesno(
                "🔄 Reiniciar Juego",
                "La configuración ha cambiado.\n"
                "¿Quieres comenzar un nuevo juego con la nueva configuración?"
            )
            if respuesta:
                self.nuevo_juego()
    
    def cambiar_dificultad(self, dificultad: str):
        """Cambia la dificultad del juego"""
        self.config.establecer_dificultad(dificultad)
        self.panel_configuracion.var_dificultad.set(dificultad)
        self.on_configuracion_cambiada()
    
    def actualizar_subtitulo(self, victoria: bool = None):
        """Actualiza el subtítulo según el estado del juego"""
        dificultad = self.config.obtener("dificultad")
        texto_base = f"En juego | Dificultad: {dificultad}"
        
        if victoria is True:
            texto_extra = " | ¡ÚLTIMA PARTIDA: VICTORIA! 🎉"
        elif victoria is False:
            texto_extra = " | ¡ÚLTIMA PARTIDA: DERROTA! 💀"
        else:
            texto_extra = ""
        
        self.subtitulo_label.config(text=texto_base + texto_extra)
    
    def volver_menu_principal(self):
        """Vuelve al menú principal"""
        respuesta = messagebox.askyesno(
            "🏠 Volver al Menú Principal",
            "¿Quieres volver al menú principal?\n\n"
            "Tu juego actual se perderá."
        )
        
        if respuesta:
            self.root.destroy()
    
    def mostrar_ayuda(self):
        """Muestra la ayuda del juego"""
        ayuda_texto = """
        🎮 CÓMO JUGAR A DESAFÍO DE PALABRAS 🎮

        OBJETIVO:
        Adivinar la palabra secreta antes de agotar todos los intentos.

        MECÁNICA DE JUEGO:
        1. Introduce una letra en el campo de texto y presiona "ADIVINAR" o Enter
        2. Si la letra está en la palabra, se revelará en su posición
        3. Si la letra NO está, perderás un intento
        4. Adivina todas las letras antes de agotar los intentos para ganar

        DIFICULTADES:
        • 🟢 FÁCIL: Palabras cortas, 8 intentos, pistas generosas
        • 🟡 MEDIO: Palabras medias, 6 intentos, pistas moderadas
        • 🔴 DIFÍCIL: Palabras largas, 4 intentos, pistas limitadas

        PISTAS:
        • Las pistas aparecen automáticamente después de varios intentos
        • Incluyen: longitud, categoría, primera/última letra, etc.
        • Puedes desactivarlas en Configuración

        CONSEJOS:
        • Empieza con vocales comunes (A, E, I, O, U)
        • Luego prueba consonantes comunes (R, S, T, L, N)
        • Observa las letras incorrectas para descartar opciones
        • Usa las pistas estratégicamente

        ¡DIVIÉRTETE Y MEJORA TU VOCABULARIO! 📚
        """
        messagebox.showinfo("🎮 Ayuda del Juego", ayuda_texto)
    
    def mostrar_reglas(self):
        """Muestra las reglas completas del juego"""
        reglas_texto = """
        📜 REGLAS COMPLETAS DEL JUEGO 📜

        1. CONFIGURACIÓN INICIAL:
           • Selecciona la dificultad (Fácil, Medio, Difícil)
           • Configura el número máximo de intentos (3-15)
           • Ajusta otras opciones en el panel de Configuración

        2. DESARROLLO DEL JUEGO:
           • Se te asignará una palabra secreta según la dificultad
           • Solo puedes ingresar una letra por intento
           • Las letras incorrectas se mostrarán en rojo
           • Cada letra incorrecta consume un intento

        3. CONDICIONES DE VICTORIA:
           • Adivinar todas las letras de la palabra secreta
           • Debes hacerlo antes de agotar los intentos máximos

        4. CONDICIONES DE DERROTA:
           • Agotar todos los intentos sin adivinar la palabra
           • El juego termina automáticamente

        5. PUNTUACIÓN Y ESTADÍSTICAS:
           • Menos intentos = mejor puntuación
           • Menos tiempo = mejor puntuación
           • Las victorias se registran en el ranking
           • Puedes ver tus estadísticas en tiempo real

        6. CARACTERÍSTICAS ESPECIALES:
           • Sistema de pistas progresivas
           • Temporizador opcional
           • Ranking de mejores partidas
           • Estadísticas por dificultad
           • Personalización completa

        🏆 EL RANKING SE CALCULA POR:
        1. Menor número de intentos
        2. Menor tiempo de resolución
        3. Mayor dificultad (bonificación)

        ¡BUENA SUERTE Y QUE GANE EL MEJOR! 🍀
        """
        messagebox.showinfo("📜 Reglas del Juego", reglas_texto)
    
    def mostrar_acerca_de(self):
        """Muestra información acerca del juego"""
        acerca_texto = f"""
        🎮 DESAFÍO DE PALABRAS
        Versión 2.0 - El Juego Definitivo
        
        DESCRIPCIÓN:
        Juego educativo y entretenido diseñado para mejorar
        el vocabulario mientras te diviertes adivinando palabras.
        
        CARACTERÍSTICAS PRINCIPALES:
        ✅ 3 niveles de dificultad (Fácil, Medio, Difícil)
        ✅ Estadísticas en tiempo real
        ✅ Base de datos con +60 palabras
        
        COLORES DEL TEMA:
        • Fondo principal: {self.colores['fondo_principal']}
        • Fondo secundario: {self.colores['fondo_secundario']}
        • Color de acento: {self.colores['acento_principal']}
        • Color secundario: {self.colores['acento_secundario']}
        
        DESARROLLADO CON:
        • Python 3.x
        • Tkinter (Interfaz gráfica)
        • SQLite (Base de datos)
        • JSON (Configuración)
        
        CRÉDITOS:
        Product owner: Breyler Emanuel Correa Ruiz
        Scrum Master: Andrés Felipe Contreras Delgado
        Develop team: Abril Ariadna Meneses Duran


        📚 Diccionario: Palabras comunes y técnicas
        
        LICENCIA:
        © 2025 Juego de Palabras
        Software educativo de código abierto
        
        ¡GRACIAS POR JUGAR! 🎉
        """
        messagebox.showinfo("ℹ️ Acerca de Desafío de Palabras", acerca_texto)
    
    def mostrar_ranking(self):
        """Muestra el ranking de mejores partidas"""
        self.panel_estadisticas.mostrar_ranking()
    
    def mostrar_estadisticas_completas(self):
        """Muestra estadísticas completas en una ventana aparte"""
        try:
            stats = self.gestor_db.obtener_estadisticas()
            
            # Crear texto detallado
            texto_estadisticas = f"""
            📊 ESTADÍSTICAS COMPLETAS DEL JUEGO
            
            ESTADÍSTICAS GENERALES:
            • ✅ Victorias totales: {stats['victorias']}
            • ❌ Derrotas totales: {stats['derrotas']}
            • 🎮 Partidas jugadas: {stats['partidas_totales']}
            • 🎯 Promedio de intentos (victorias): {stats['promedio_intentos']:.2f}
            
            ESTADÍSTICAS POR DIFICULTAD:
            """
            
            for dificultad, datos in stats["por_dificultad"].items():
                if datos['total'] > 0:
                    porcentaje = datos['porcentaje']
                    texto_estadisticas += f"""
            • {dificultad.upper()}:
              - Victorias: {datos['victorias']}/{datos['total']}
              - Porcentaje de éxito: {porcentaje}%
              - Ratio: {datos['victorias']}:{datos['total']-datos['victorias']}
                    """
                else:
                    texto_estadisticas += f"""
            • {dificultad.upper()}:
              - Aún no se han jugado partidas
                    """
            
            texto_estadisticas += f"""
            
            RENDIMIENTO GENERAL:
            • Porcentaje total de victorias: {(stats['victorias']/stats['partidas_totales']*100) if stats['partidas_totales'] > 0 else 0:.1f}%
            • Mejor dificultad: {max(stats['por_dificultad'].items(), key=lambda x: x[1]['porcentaje'])[0].upper() if any(d['total'] > 0 for d in stats['por_dificultad'].values()) else 'N/A'}
            
            CONSEJOS:
            • Juega más partidas para mejorar tus estadísticas
            • Intenta diferentes dificultades
            • Revisa el ranking para ver los mejores resultados
            """
            
            messagebox.showinfo("📈 Estadísticas Completas", texto_estadisticas)
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudieron cargar las estadísticas:\n{e}")
    
    def salir(self):
        """Cierra la aplicación con confirmación"""
        respuesta = messagebox.askyesno(
            "👋 Salir del Juego",
            "¿Estás seguro de que quieres salir de Desafío de Palabras?\n\n"
            "Tu progreso se perderá, pero las estadísticas se guardarán."
        )
        
        if respuesta:
            self.root.quit()
            self.root.destroy()