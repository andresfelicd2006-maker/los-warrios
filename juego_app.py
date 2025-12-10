# juego_app.py - MODIFICACIONES
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
            "morado": "#8b5cf6",
            "cyan": "#06b6d4",
            "rosa": "#ec4899"
        }
        
        # Variable para controlar si ya se mostraron opciones post-partida
        self.mostrando_opciones = False
        
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
        
        # Configurar ventana de opciones post-partida (inicialmente oculta)
        self.configurar_ventana_opciones()
    
    def configurar_ventana_opciones(self):
        """Configura la ventana de opciones que aparece después de ganar/perder"""
        # Crear ventana flotante (inicialmente oculta)
        self.ventana_opciones = tk.Toplevel(self.root)
        self.ventana_opciones.title("🎮 ¿Qué quieres hacer ahora?")
        self.ventana_opciones.geometry("500x400")
        self.ventana_opciones.configure(bg=self.colores["fondo_principal"])
        self.ventana_opciones.resizable(False, False)
        self.ventana_opciones.overrideredirect(True)  # Sin bordes
        self.ventana_opciones.withdraw()  # Ocultar inicialmente
        
        # Hacer que la ventana sea modal (bloquee interacción con la ventana principal)
        self.ventana_opciones.transient(self.root)
        self.ventana_opciones.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(self.ventana_opciones, bg=self.colores["fondo_principal"], 
                             padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título según resultado
        self.label_titulo_opciones = tk.Label(
            main_frame,
            text="",
            font=("Arial", 20, "bold"),
            bg=self.colores["fondo_principal"],
            fg=self.colores["texto_principal"],
            pady=20
        )
        self.label_titulo_opciones.pack()
        
        # Mensaje de resultado
        self.label_mensaje_opciones = tk.Label(
            main_frame,
            text="",
            font=("Arial", 12),
            bg=self.colores["fondo_principal"],
            fg=self.colores["texto_secundario"],
            wraplength=400,
            pady=10
        )
        self.label_mensaje_opciones.pack()
        
        # Frame para estadísticas de la partida
        self.frame_stats_partida = tk.Frame(main_frame, bg=self.colores["fondo_secundario"], 
                                           relief=tk.RAISED, bd=2, padx=20, pady=15)
        self.frame_stats_partida.pack(fill=tk.X, pady=20)
        
        # Labels para estadísticas
        self.label_palabra = tk.Label(
            self.frame_stats_partida,
            text="",
            font=("Arial", 14, "bold"),
            bg=self.colores["fondo_secundario"],
            fg=self.colores["acento_principal"]
        )
        self.label_palabra.pack()
        
        self.label_intentos_stats = tk.Label(
            self.frame_stats_partida,
            text="",
            font=("Arial", 12),
            bg=self.colores["fondo_secundario"],
            fg=self.colores["texto_secundario"]
        )
        self.label_intentos_stats.pack()
        
        self.label_tiempo_stats = tk.Label(
            self.frame_stats_partida,
            text="",
            font=("Arial", 12),
            bg=self.colores["fondo_secundario"],
            fg=self.colores["texto_secundario"]
        )
        self.label_tiempo_stats.pack()
        
        # Frame para botones de opciones
        frame_botones = tk.Frame(main_frame, bg=self.colores["fondo_principal"])
        frame_botones.pack(fill=tk.X, pady=20)
        
        # Botones de opciones
        botones_opciones = [
            {
                "text": "🔄 JUGAR DE NUEVO",
                "command": self.opcion_nuevo_juego,
                "color": self.colores["verde"],
                "tooltip": "Jugar otra partida con la misma dificultad"
            },
            {
                "text": "🎮 CAMBIAR DIFICULTAD",
                "command": self.opcion_cambiar_dificultad,
                "color": self.colores["azul"],
                "tooltip": "Cambiar dificultad y jugar"
            },
            {
                "text": "📊 VER ESTADÍSTICAS",
                "command": self.opcion_ver_estadisticas,
                "color": self.colores["amarillo"],
                "tooltip": "Ver estadísticas detalladas"
            },
            {
                "text": "🏠 VOLVER AL MENÚ",
                "command": self.opcion_volver_menu,
                "color": self.colores["morado"],
                "tooltip": "Volver al menú principal"
            }
        ]
        
        for boton_info in botones_opciones:
            # Frame para cada botón
            btn_frame = tk.Frame(frame_botones, bg=self.colores["fondo_principal"])
            btn_frame.pack(fill=tk.X, pady=8)
            
            # Botón
            btn = tk.Button(
                btn_frame,
                text=boton_info["text"],
                font=("Arial", 11, "bold"),
                bg=boton_info["color"],
                fg="white",
                padx=20,
                pady=12,
                command=boton_info["command"],
                cursor="hand2",
                relief=tk.RAISED,
                bd=2,
                width=25
            )
            btn.pack()
            
            # Tooltip
            tk.Label(
                btn_frame,
                text=boton_info["tooltip"],
                font=("Arial", 8, "italic"),
                bg=self.colores["fondo_principal"],
                fg=self.colores["texto_secundario"]
            ).pack(pady=(2, 0))
    
    def mostrar_opciones_post_partida(self, resultado: dict):
        """Muestra la ventana de opciones después de ganar/perder"""
        if self.mostrando_opciones:
            return
        
        self.mostrando_opciones = True
        
        # Configurar título y mensaje según resultado
        if resultado["estado"] == "victoria":
            self.label_titulo_opciones.config(
                text="🎉 ¡FELICIDADES! ¡HAS GANADO!",
                fg=self.colores["verde"]
            )
            self.label_mensaje_opciones.config(
                text="¡Excelente trabajo! Adivinaste la palabra correctamente."
            )
        else:  # derrota
            self.label_titulo_opciones.config(
                text="💀 ¡FIN DEL JUEGO!",
                fg=self.colores["rojo"]
            )
            self.label_mensaje_opciones.config(
                text="No te rindas, ¡inténtalo de nuevo!"
            )
        
        # Actualizar estadísticas de la partida
        self.label_palabra.config(
            text=f"Palabra: {resultado.get('palabra', '')}"
        )
        self.label_intentos_stats.config(
            text=f"Intentos usados: {resultado.get('intentos', 0)}"
        )
        self.label_tiempo_stats.config(
            text=f"Tiempo: {resultado.get('tiempo', 0)} segundos"
        )
        
        # Posicionar ventana en el centro de la pantalla
        self.ventana_opciones.update_idletasks()
        width = self.ventana_opciones.winfo_width()
        height = self.ventana_opciones.winfo_height()
        
        # Obtener posición de la ventana principal
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        
        # Calcular posición centrada dentro de la ventana principal
        x = main_x + (main_width // 2) - (width // 2)
        y = main_y + (main_height // 2) - (height // 2)
        
        self.ventana_opciones.geometry(f"{width}x{height}+{x}+{y}")
        
        # Mostrar ventana
        self.ventana_opciones.deiconify()
        
        # Traer al frente
        self.ventana_opciones.lift()
        self.ventana_opciones.focus_force()
    
    def ocultar_opciones_post_partida(self):
        """Oculta la ventana de opciones"""
        self.mostrando_opciones = False
        self.ventana_opciones.withdraw()
    
    def opcion_nuevo_juego(self):
        """Opción: Jugar de nuevo con misma dificultad"""
        self.ocultar_opciones_post_partida()
        self.nuevo_juego()
    
    def opcion_cambiar_dificultad(self):
        """Opción: Cambiar dificultad antes de jugar"""
        self.ocultar_opciones_post_partida()
        self.mostrar_selector_dificultad()
    
    def opcion_ver_estadisticas(self):
        """Opción: Ver estadísticas detalladas"""
        self.ocultar_opciones_post_partida()
        self.panel_estadisticas.mostrar_detalles_completos()
    
    def opcion_volver_menu(self):
        """Opción: Volver al menú principal"""
        self.ocultar_opciones_post_partida()
        self.volver_menu_principal()
    
    def mostrar_selector_dificultad(self):
        """Muestra un selector de dificultad antes de nuevo juego"""
        # Crear ventana emergente para seleccionar dificultad
        selector_window = tk.Toplevel(self.root)
        selector_window.title("🎮 Seleccionar Dificultad")
        selector_window.geometry("400x300")
        selector_window.configure(bg=self.colores["fondo_principal"])
        selector_window.resizable(False, False)
        
        # Centrar ventana
        selector_window.update_idletasks()
        width = selector_window.winfo_width()
        height = selector_window.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        selector_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Frame principal
        main_frame = tk.Frame(selector_window, bg=self.colores["fondo_principal"], 
                             padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(
            main_frame,
            text="🎮 SELECCIONAR DIFICULTAD",
            font=("Arial", 16, "bold"),
            fg=self.colores["acento_principal"],
            bg=self.colores["fondo_principal"],
            pady=10
        ).pack()
        
        tk.Label(
            main_frame,
            text="Elige la dificultad para la próxima partida:",
            font=("Arial", 11),
            fg=self.colores["texto_secundario"],
            bg=self.colores["fondo_principal"],
            pady=10
        ).pack()
        
        # Variable para dificultad seleccionada
        dificultad_seleccionada = tk.StringVar(value=self.config.obtener("dificultad"))
        
        # Frame para opciones de dificultad
        frame_opciones = tk.Frame(main_frame, bg=self.colores["fondo_principal"], pady=20)
        frame_opciones.pack()
        
        dificultades = [
            ("FACIL", "🟢 FÁCIL", "Palabras cortas\n8 intentos\nPistas generosas", 
             self.colores["verde"]),
            ("MEDIO", "🟡 MEDIO", "Palabras medias\n6 intentos\nPistas moderadas", 
             self.colores["amarillo"]),
            ("DIFICIL", "🔴 DIFÍCIL", "Palabras largas\n4 intentos\nPistas limitadas", 
             self.colores["rojo"])
        ]
        
        for valor, texto, descripcion, color in dificultades:
            # Frame para cada opción
            opcion_frame = tk.Frame(frame_opciones, bg=self.colores["fondo_principal"])
            opcion_frame.pack(fill=tk.X, pady=8)
            
            # Radio button
            rb = tk.Radiobutton(
                opcion_frame,
                text=texto,
                variable=dificultad_seleccionada,
                value=valor,
                font=("Arial", 12, "bold"),
                bg=self.colores["fondo_principal"],
                fg=color,
                selectcolor=self.colores["fondo_principal"],
                activebackground=self.colores["fondo_principal"],
                activeforeground=color,
                cursor="hand2"
            )
            rb.pack(side=tk.LEFT)
            
            # Descripción
            tk.Label(
                opcion_frame,
                text=descripcion,
                font=("Arial", 9),
                bg=self.colores["fondo_principal"],
                fg=self.colores["texto_secundario"],
                justify=tk.LEFT
            ).pack(side=tk.LEFT, padx=(20, 0))
        
        # Frame para botones
        frame_botones = tk.Frame(main_frame, bg=self.colores["fondo_principal"], pady=20)
        frame_botones.pack()
        
        # Botón aceptar
        tk.Button(
            frame_botones,
            text="✅ ACEPTAR Y JUGAR",
            font=("Arial", 11, "bold"),
            bg=self.colores["verde"],
            fg="white",
            padx=20,
            pady=10,
            command=lambda: self.aplicar_dificultad_y_jugar(
                dificultad_seleccionada.get(), selector_window
            ),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)
        
        # Botón cancelar
        tk.Button(
            frame_botones,
            text="❌ CANCELAR",
            font=("Arial", 11),
            bg=self.colores["rojo"],
            fg="white",
            padx=20,
            pady=10,
            command=selector_window.destroy,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)
    
    def aplicar_dificultad_y_jugar(self, dificultad: str, ventana_selector):
        """Aplica la dificultad seleccionada y comienza nuevo juego"""
        # Cambiar dificultad
        self.config.establecer_dificultad(dificultad)
        self.juego_logica.cambiar_dificultad(dificultad)
        
        # Cerrar ventana de selector
        ventana_selector.destroy()
        
        # Iniciar nuevo juego
        self.nuevo_juego()
    
    def procesar_intento_jugador(self, entrada: str):
        """Procesa un intento del jugador"""
        resultado = self.juego_logica.procesar_intento(entrada)
        
        # Actualizar panel de juego
        self.panel_juego.actualizar_panel()
        
        # Manejar resultados especiales
        if resultado["estado"] == "victoria":
            # Actualizar estadísticas
            self.panel_estadisticas.actualizar_estadisticas()
            self.actualizar_subtitulo(victoria=True)
            
            # Mostrar opciones post-partida después de un breve delay
            self.root.after(800, lambda: self.mostrar_opciones_post_partida(resultado))
            
        elif resultado["estado"] == "derrota":
            # Actualizar estadísticas
            self.panel_estadisticas.actualizar_estadisticas()
            self.actualizar_subtitulo(victoria=False)
            
            # Mostrar opciones post-partida después de un breve delay
            self.root.after(800, lambda: self.mostrar_opciones_post_partida(resultado))
            
        elif resultado["estado"] == "error":
            # Solo mostrar error, no opciones
            pass
    
    # Resto del código permanece igual...
    def nuevo_juego(self):
        """Inicia un nuevo juego"""
        # Ocultar ventana de opciones si está visible
        if self.mostrando_opciones:
            self.ocultar_opciones_post_partida()
        
        # Reiniciar juego
        self.juego_logica.reiniciar_juego()
        self.panel_juego.actualizar_panel()
        self.actualizar_subtitulo()
        self.panel_juego.focus_entrada()
        
        # Actualizar dificultad en menú
        if hasattr(self, 'var_dificultad_menu'):
            self.var_dificultad_menu.set(self.config.obtener("dificultad"))
    
    # Resto del código sigue igual...