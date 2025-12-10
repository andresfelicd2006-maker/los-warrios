# panel_estadisticas.py
import tkinter as tk
from tkinter import ttk, messagebox, font
from gestor_bd import GestorBaseDatos
from typing import Dict
import math

class PanelEstadisticas(tk.Frame):
    """Panel que muestra las estadísticas del juego con mejor visualización"""
    
    def __init__(self, parent, gestor_db: GestorBaseDatos, colores: Dict = None):
        super().__init__(parent)
        self.gestor_db = gestor_db
        
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
            "morado": "#8b5cf6",
            "cyan": "#06b6d4",
            "rosa": "#ec4899"
        }
        
        # Configurar fuente para mejor legibilidad
        self.fuente_titulo = ("Arial", 12, "bold")
        self.fuente_normal = ("Arial", 10)
        self.fuente_negrita = ("Arial", 10, "bold")
        self.fuente_grande = ("Arial", 11, "bold")
        
        self.configurar_interfaz()
        self.actualizar_estadisticas()
    
    def configurar_interfaz(self):
        """Configura los elementos de la interfaz del panel de estadísticas"""
        self.configure(bg=self.colores["fondo_secundario"])
        
        # Frame principal con scroll
        main_container = tk.Frame(self, bg=self.colores["fondo_secundario"])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para scroll
        self.canvas = tk.Canvas(main_container, bg=self.colores["fondo_secundario"], 
                               highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", 
                                 command=self.canvas.yview)
        scrollable_frame = tk.Frame(self.canvas, bg=self.colores["fondo_secundario"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Contenido dentro del frame scrollable
        self.contenido_principal = scrollable_frame
        self.crear_contenido_estadisticas()
    
    def _on_mousewheel(self, event):
        """Permite scroll con rueda del mouse"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def crear_contenido_estadisticas(self):
        """Crea el contenido de las estadísticas"""
        # Título principal
        titulo_frame = tk.Frame(self.contenido_principal, bg=self.colores["morado"], height=45)
        titulo_frame.pack(fill=tk.X, pady=(0, 15), padx=2)
        titulo_frame.pack_propagate(False)
        
        tk.Label(
            titulo_frame,
            text="📊 PANEL DE ESTADÍSTICAS",
            font=("Arial", 14, "bold"),
            fg="white",
            bg=self.colores["morado"]
        ).pack(expand=True)
        
        tk.Label(
            titulo_frame,
            text="Datos actualizados en tiempo real",
            font=("Arial", 9, "italic"),
            fg="white",
            bg=self.colores["morado"]
        ).pack()
        
        # Sección 1: Resumen General
        self.crear_seccion_resumen()
        
        # Separador
        self.crear_separador("📈 ESTADÍSTICAS DETALLADAS")
        
        # Sección 2: Estadísticas por Dificultad
        self.crear_seccion_dificultad()
        
        # Separador
        self.crear_separador("🎯 RENDIMIENTO")
        
        # Sección 3: Métricas de Rendimiento
        self.crear_seccion_rendimiento()
        
        # Sección 4: Botones de Acción
        self.crear_seccion_botones()
        
        # Espacio final
        tk.Frame(self.contenido_principal, height=20, 
                bg=self.colores["fondo_secundario"]).pack()
    
    def crear_seccion_resumen(self):
        """Crea la sección de resumen general"""
        seccion_frame = tk.LabelFrame(
            self.contenido_principal,
            text="🏆 RESUMEN GENERAL",
            font=self.fuente_titulo,
            bg=self.colores["fondo_terciario"],
            fg=self.colores["texto_principal"],
            padx=20,
            pady=15,
            relief=tk.RAISED,
            bd=2
        )
        seccion_frame.pack(fill=tk.X, padx=10, pady=(0, 15))
        
        # Grid para estadísticas generales (3x2)
        grid_frame = tk.Frame(seccion_frame, bg=self.colores["fondo_terciario"])
        grid_frame.pack(fill=tk.X, expand=True)
        
        # Definir métricas con íconos y colores
        metricas = [
            {
                "key": "partidas_totales",
                "label": "🎮 PARTIDAS TOTALES",
                "color": self.colores["morado"],
                "desc": "Total de partidas jugadas"
            },
            {
                "key": "victorias",
                "label": "✅ VICTORIAS",
                "color": self.colores["verde"],
                "desc": "Partidas ganadas"
            },
            {
                "key": "derrotas",
                "label": "❌ DERROTAS",
                "color": self.colores["rojo"],
                "desc": "Partidas perdidas"
            },
            {
                "key": "promedio_intentos",
                "label": "🎯 INTENTOS PROMEDIO",
                "color": self.colores["amarillo"],
                "desc": "Por victoria"
            },
            {
                "key": "porcentaje_victorias",
                "label": "📊 % DE VICTORIAS",
                "color": self.colores["cyan"],
                "desc": "Efectividad"
            },
            {
                "key": "mejor_racha",
                "label": "🔥 MEJOR RACHA",
                "color": self.colores["rosa"],
                "desc": "Victorias consecutivas"
            }
        ]
        
        self.labels_stats = {}
        
        for i, metrica in enumerate(metricas):
            row = i // 3
            col = i % 3
            
            # Frame para cada métrica
            metrica_frame = tk.Frame(grid_frame, bg=self.colores["fondo_terciario"], 
                                    relief=tk.GROOVE, bd=1)
            metrica_frame.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
            grid_frame.grid_columnconfigure(col, weight=1)
            grid_frame.grid_rowconfigure(row, weight=1)
            
            # Etiqueta del título
            tk.Label(
                metrica_frame,
                text=metrica["label"],
                font=("Arial", 9, "bold"),
                bg=self.colores["fondo_terciario"],
                fg=metrica["color"],
                wraplength=120
            ).pack(pady=(10, 5))
            
            # Valor de la métrica
            label_valor = tk.Label(
                metrica_frame,
                text="0",
                font=("Arial", 16, "bold"),
                bg=self.colores["fondo_terciario"],
                fg="white",
                height=2
            )
            label_valor.pack()
            
            # Descripción
            tk.Label(
                metrica_frame,
                text=metrica["desc"],
                font=("Arial", 8),
                bg=self.colores["fondo_terciario"],
                fg=self.colores["texto_secundario"]
            ).pack(pady=(0, 10))
            
            self.labels_stats[metrica["key"]] = label_valor
    
    def crear_seccion_dificultad(self):
        """Crea la sección de estadísticas por dificultad"""
        seccion_frame = tk.LabelFrame(
            self.contenido_principal,
            text="🎮 RENDIMIENTO POR DIFICULTAD",
            font=self.fuente_titulo,
            bg=self.colores["fondo_terciario"],
            fg=self.colores["texto_principal"],
            padx=20,
            pady=15,
            relief=tk.RAISED,
            bd=2
        )
        seccion_frame.pack(fill=tk.X, padx=10, pady=(0, 15))
        
        # Frame para las barras de progreso
        self.frame_barras = tk.Frame(seccion_frame, bg=self.colores["fondo_terciario"])
        self.frame_barras.pack(fill=tk.X, pady=(10, 0))
        
        # Labels para estadísticas por dificultad
        self.labels_dificultad = {}
        self.barras_progreso = {}
        self.frames_dificultad = {}
        
        dificultades = [
            ("FACIL", "🟢 FÁCIL", self.colores["verde"], "Palabras cortas, 8 intentos"),
            ("MEDIO", "🟡 MEDIO", self.colores["amarillo"], "Palabras medias, 6 intentos"),
            ("DIFICIL", "🔴 DIFÍCIL", self.colores["rojo"], "Palabras largas, 4 intentos")
        ]
        
        for dificultad, texto, color, desc in dificultades:
            # Frame para cada dificultad
            dif_frame = tk.Frame(self.frame_barras, bg=self.colores["fondo_terciario"])
            dif_frame.pack(fill=tk.X, pady=12, padx=5)
            
            # Encabezado de dificultad
            header_frame = tk.Frame(dif_frame, bg=self.colores["fondo_terciario"])
            header_frame.pack(fill=tk.X)
            
            # Nombre de dificultad
            tk.Label(
                header_frame,
                text=texto,
                font=("Arial", 11, "bold"),
                bg=self.colores["fondo_terciario"],
                fg=color,
                width=15,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            # Descripción
            tk.Label(
                header_frame,
                text=desc,
                font=("Arial", 9, "italic"),
                bg=self.colores["fondo_terciario"],
                fg=self.colores["texto_secundario"]
            ).pack(side=tk.LEFT, padx=(10, 0))
            
            # Frame para estadísticas
            stats_frame = tk.Frame(dif_frame, bg=self.colores["fondo_terciario"])
            stats_frame.pack(fill=tk.X, pady=(5, 0))
            
            # Barra de progreso
            barra_frame = tk.Frame(stats_frame, bg="#2a2a4e", height=20, 
                                  relief=tk.SUNKEN, bd=1)
            barra_frame.pack(fill=tk.X, pady=5)
            barra_frame.pack_propagate(False)
            
            # Barra de color (inicialmente vacía)
            barra_progreso = tk.Frame(barra_frame, bg=color, width=0)
            barra_progreso.pack(side=tk.LEFT, fill=tk.Y)
            
            # Label para porcentaje
            label_porcentaje = tk.Label(
                barra_frame,
                text="0%",
                font=("Arial", 9, "bold"),
                bg="#2a2a4e",
                fg="white"
            )
            label_porcentaje.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            # Frame para números detallados
            nums_frame = tk.Frame(stats_frame, bg=self.colores["fondo_terciario"])
            nums_frame.pack(fill=tk.X, pady=(5, 0))
            
            # Labels para números
            label_ratio = tk.Label(
                nums_frame,
                text="Victorias: 0/0",
                font=("Arial", 10),
                bg=self.colores["fondo_terciario"],
                fg=self.colores["texto_secundario"]
            )
            label_ratio.pack(side=tk.LEFT)
            
            label_porcentaje_det = tk.Label(
                nums_frame,
                text="(0%)",
                font=("Arial", 10, "bold"),
                bg=self.colores["fondo_terciario"],
                fg=color
            )
            label_porcentaje_det.pack(side=tk.LEFT, padx=(10, 0))
            
            # Guardar referencias
            self.frames_dificultad[dificultad.lower()] = {
                "frame": dif_frame,
                "barra": barra_progreso,
                "porcentaje_barra": label_porcentaje,
                "ratio": label_ratio,
                "porcentaje": label_porcentaje_det
            }
    
    def crear_seccion_rendimiento(self):
        """Crea la sección de métricas de rendimiento"""
        seccion_frame = tk.LabelFrame(
            self.contenido_principal,
            text="📈 ANÁLISIS DE RENDIMIENTO",
            font=self.fuente_titulo,
            bg=self.colores["fondo_terciario"],
            fg=self.colores["texto_principal"],
            padx=20,
            pady=15,
            relief=tk.RAISED,
            bd=2
        )
        seccion_frame.pack(fill=tk.X, padx=10, pady=(0, 15))
        
        # Frame para métricas
        metrics_frame = tk.Frame(seccion_frame, bg=self.colores["fondo_terciario"])
        metrics_frame.pack(fill=tk.X, pady=10)
        
        # Métricas de rendimiento (2 columnas)
        metricas_rendimiento = [
            {
                "key": "eficiencia",
                "label": "⚡ EFICIENCIA",
                "color": self.colores["verde"],
                "desc": "Victorias por intento"
            },
            {
                "key": "consistencia",
                "label": "📅 CONSISTENCIA",
                "color": self.colores["azul"],
                "desc": "Rendimiento estable"
            },
            {
                "key": "mejor_dificultad",
                "label": "🏆 MEJOR DIFICULTAD",
                "color": self.colores["amarillo"],
                "desc": "Mayor porcentaje de éxito"
            },
            {
                "key": "ultimas_partidas",
                "label": "🔄 ÚLTIMAS 10 PARTIDAS",
                "color": self.colores["rosa"],
                "desc": "Rendimiento reciente"
            }
        ]
        
        self.labels_rendimiento = {}
        
        for i, metrica in enumerate(metricas_rendimiento):
            row = i // 2
            col = i % 2
            
            frame = tk.Frame(metrics_frame, bg=self.colores["fondo_terciario"])
            frame.grid(row=row, column=col, sticky="nsew", padx=10, pady=8)
            metrics_frame.grid_columnconfigure(col, weight=1)
            metrics_frame.grid_rowconfigure(row, weight=1)
            
            # Título
            tk.Label(
                frame,
                text=metrica["label"],
                font=("Arial", 9, "bold"),
                bg=self.colores["fondo_terciario"],
                fg=metrica["color"]
            ).pack(anchor=tk.W)
            
            # Valor
            label_valor = tk.Label(
                frame,
                text="--",
                font=("Arial", 11, "bold"),
                bg=self.colores["fondo_terciario"],
                fg="white"
            )
            label_valor.pack(anchor=tk.W, pady=(5, 0))
            
            # Descripción
            tk.Label(
                frame,
                text=metrica["desc"],
                font=("Arial", 8),
                bg=self.colores["fondo_terciario"],
                fg=self.colores["texto_secundario"]
            ).pack(anchor=tk.W)
            
            self.labels_rendimiento[metrica["key"]] = label_valor
    
    def crear_seccion_botones(self):
        """Crea la sección de botones de acción"""
        seccion_frame = tk.Frame(self.contenido_principal, 
                                bg=self.colores["fondo_secundario"])
        seccion_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # Frame para botones en grid
        botones_frame = tk.Frame(seccion_frame, bg=self.colores["fondo_secundario"])
        botones_frame.pack(fill=tk.X)
        
        # Botones (2 filas x 2 columnas)
        botones_info = [
            {
                "text": "🔄 ACTUALIZAR",
                "command": self.actualizar_estadisticas,
                "color": self.colores["azul"],
                "tooltip": "Actualizar estadísticas"
            },
            {
                "text": "🏆 VER RANKING",
                "command": self.mostrar_ranking,
                "color": self.colores["amarillo"],
                "tooltip": "Ver top 10 mejores partidas"
            },
            {
                "text": "📊 DETALLES COMPLETOS",
                "command": self.mostrar_detalles_completos,
                "color": self.colores["morado"],
                "tooltip": "Ver estadísticas detalladas"
            },
            {
                "text": "🗑️ RESETEAR",
                "command": self.resetear_estadisticas,
                "color": self.colores["rojo"],
                "tooltip": "Borrar todas las estadísticas"
            }
        ]
        
        for i, boton_info in enumerate(botones_info):
            row = i // 2
            col = i % 2
            
            frame = tk.Frame(botones_frame, bg=self.colores["fondo_secundario"])
            frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            botones_frame.grid_columnconfigure(col, weight=1)
            botones_frame.grid_rowconfigure(row, weight=1)
            
            btn = tk.Button(
                frame,
                text=boton_info["text"],
                font=("Arial", 10, "bold"),
                bg=boton_info["color"],
                fg="white",
                padx=15,
                pady=10,
                command=boton_info["command"],
                cursor="hand2",
                relief=tk.RAISED,
                bd=2,
                wraplength=120
            )
            btn.pack(fill=tk.BOTH, expand=True)
            
            # Tooltip
            tk.Label(
                frame,
                text=boton_info["tooltip"],
                font=("Arial", 8, "italic"),
                bg=self.colores["fondo_secundario"],
                fg=self.colores["texto_secundario"]
            ).pack(pady=(2, 0))
    
    def crear_separador(self, texto):
        """Crea un separador con texto"""
        separador_frame = tk.Frame(self.contenido_principal, 
                                  bg=self.colores["fondo_secundario"], 
                                  height=40)
        separador_frame.pack(fill=tk.X, pady=10)
        separador_frame.pack_propagate(False)
        
        # Línea izquierda
        tk.Frame(separador_frame, height=2, bg=self.colores["acento_principal"]).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(20, 10), pady=19
        )
        
        # Texto
        tk.Label(
            separador_frame,
            text=texto,
            font=("Arial", 11, "bold"),
            bg=self.colores["fondo_secundario"],
            fg=self.colores["acento_principal"]
        ).pack(side=tk.LEFT, pady=10)
        
        # Línea derecha
        tk.Frame(separador_frame, height=2, bg=self.colores["acento_principal"]).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 20), pady=19
        )
    
    def actualizar_estadisticas(self):
        """Actualiza todas las estadísticas mostradas"""
        try:
            stats = self.gestor_db.obtener_estadisticas()
            
            # Calcular métricas adicionales
            total_partidas = stats["partidas_totales"]
            victorias = stats["victorias"]
            derrotas = stats["derrotas"]
            
            # Porcentaje de victorias
            porcentaje_victorias = 0
            if total_partidas > 0:
                porcentaje_victorias = (victorias / total_partidas) * 100
            
            # Eficiencia (victorias por intento promedio)
            eficiencia = 0
            if victorias > 0 and stats["promedio_intentos"] > 0:
                eficiencia = victorias / stats["promedio_intentos"]
            
            # Mejor dificultad
            mejor_dificultad = "N/A"
            mejor_porcentaje = 0
            for dif, datos in stats["por_dificultad"].items():
                if datos['total'] > 0:
                    porcentaje = datos['porcentaje']
                    if porcentaje > mejor_porcentaje:
                        mejor_porcentaje = porcentaje
                        mejor_dificultad = dif.upper()
            
            # Actualizar estadísticas generales
            self.labels_stats["partidas_totales"].config(text=str(total_partidas))
            self.labels_stats["victorias"].config(text=str(victorias))
            self.labels_stats["derrotas"].config(text=str(derrotas))
            self.labels_stats["promedio_intentos"].config(
                text=f"{stats['promedio_intentos']:.1f}"
            )
            self.labels_stats["porcentaje_victorias"].config(
                text=f"{porcentaje_victorias:.1f}%"
            )
            
            # Calcular mejor racha (simulación)
            mejor_racha = min(victorias, 10)  # Esto es una simulación
            self.labels_stats["mejor_racha"].config(text=f"{mejor_racha}")
            
            # Actualizar estadísticas por dificultad
            for dificultad, datos in stats["por_dificultad"].items():
                if dificultad in self.frames_dificultad:
                    frame_info = self.frames_dificultad[dificultad]
                    total = datos['total']
                    victorias_dif = datos['victorias']
                    porcentaje = datos['porcentaje']
                    
                    # Actualizar barra de progreso
                    ancho_barra = int(porcentaje * 2)  # 100% = 200px
                    frame_info["barra"].config(width=ancho_barra)
                    
                    # Actualizar porcentaje en barra
                    frame_info["porcentaje_barra"].config(text=f"{porcentaje:.1f}%")
                    
                    # Actualizar números
                    frame_info["ratio"].config(
                        text=f"Victorias: {victorias_dif}/{total}"
                    )
                    frame_info["porcentaje"].config(
                        text=f"({porcentaje:.1f}%)"
                    )
            
            # Actualizar métricas de rendimiento
            self.labels_rendimiento["eficiencia"].config(
                text=f"{eficiencia:.2f}" if eficiencia > 0 else "--"
            )
            
            self.labels_rendimiento["consistencia"].config(
                text=f"{porcentaje_victorias:.0f}%" if total_partidas > 0 else "--"
            )
            
            self.labels_rendimiento["mejor_dificultad"].config(
                text=mejor_dificultad
            )
            
            # Calcular rendimiento últimas 10 partidas
            ultimas_10 = "0/0"
            try:
                ranking = self.gestor_db.obtener_ranking(10)
                if ranking:
                    victorias_ultimas = len([r for r in ranking if r[0]])
                    ultimas_10 = f"{victorias_ultimas}/10"
            except:
                ultimas_10 = "N/A"
            
            self.labels_rendimiento["ultimas_partidas"].config(
                text=ultimas_10
            )
            
            # Mostrar mensaje de éxito
            self.mostrar_notificacion("✅ Estadísticas actualizadas")
            
        except Exception as e:
            print(f"⚠️ Error actualizando estadísticas: {e}")
            self.mostrar_notificacion("❌ Error al cargar estadísticas", error=True)
    
    def mostrar_notificacion(self, mensaje: str, error: bool = False):
        """Muestra una notificación temporal"""
        # Crear ventana de notificación
        notif = tk.Toplevel(self)
        notif.overrideredirect(True)  # Sin bordes
        notif.geometry("300x60+200+200")
        
        # Configurar color según tipo
        if error:
            bg_color = self.colores["rojo"]
        else:
            bg_color = self.colores["verde"]
        
        notif.configure(bg=bg_color)
        
        # Mensaje
        tk.Label(
            notif,
            text=mensaje,
            font=("Arial", 10, "bold"),
            bg=bg_color,
            fg="white",
            pady=20
        ).pack(expand=True)
        
        # Auto-cerrar después de 2 segundos
        notif.after(2000, notif.destroy)
        
        # Posicionar en centro
        notif.update_idletasks()
        x = self.winfo_rootx() + self.winfo_width() // 2 - notif.winfo_width() // 2
        y = self.winfo_rooty() + self.winfo_height() // 2 - notif.winfo_height() // 2
        notif.geometry(f"+{x}+{y}")
    
    def mostrar_detalles_completos(self):
        """Muestra estadísticas detalladas en ventana aparte"""
        try:
            stats = self.gestor_db.obtener_estadisticas()
            
            # Crear ventana emergente
            detalles_window = tk.Toplevel(self)
            detalles_window.title("📊 Estadísticas Detalladas")
            detalles_window.geometry("700x600")
            detalles_window.configure(bg=self.colores["fondo_principal"])
            detalles_window.resizable(True, True)
            
            # Centrar ventana
            detalles_window.update_idletasks()
            width = detalles_window.winfo_width()
            height = detalles_window.winfo_height()
            x = (detalles_window.winfo_screenwidth() // 2) - (width // 2)
            y = (detalles_window.winfo_screenheight() // 2) - (height // 2)
            detalles_window.geometry(f'{width}x{height}+{x}+{y}')
            
            # Frame principal con scroll
            main_frame = tk.Frame(detalles_window, bg=self.colores["fondo_principal"])
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(
                main_frame,
                text="📊 ESTADÍSTICAS DETALLADAS",
                font=("Arial", 18, "bold"),
                fg=self.colores["acento_principal"],
                bg=self.colores["fondo_principal"]
            ).pack(pady=(0, 20))
            
            # Crear secciones detalladas
            secciones = [
                ("📈 RESUMEN GENERAL", self.crear_texto_resumen(stats)),
                ("🎮 POR DIFICULTAD", self.crear_texto_dificultad(stats)),
                ("📅 HISTORIAL", self.crear_texto_historial()),
                ("💡 RECOMENDACIONES", self.crear_texto_recomendaciones(stats))
            ]
            
            for titulo, contenido in secciones:
                # Frame de sección
                seccion_frame = tk.LabelFrame(
                    main_frame,
                    text=titulo,
                    font=("Arial", 12, "bold"),
                    bg=self.colores["fondo_secundario"],
                    fg=self.colores["texto_principal"],
                    padx=15,
                    pady=15,
                    relief=tk.RAISED,
                    bd=2
                )
                seccion_frame.pack(fill=tk.X, pady=(0, 15))
                
                # Contenido
                tk.Label(
                    seccion_frame,
                    text=contenido,
                    font=("Consolas", 10),
                    bg=self.colores["fondo_secundario"],
                    fg=self.colores["texto_secundario"],
                    justify=tk.LEFT,
                    anchor=tk.W
                ).pack(fill=tk.X)
            
            # Botón cerrar
            tk.Button(
                main_frame,
                text="CERRAR",
                font=("Arial", 11, "bold"),
                bg=self.colores["rojo"],
                fg="white",
                command=detalles_window.destroy,
                padx=30,
                pady=10
            ).pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los detalles:\n{e}")
    
    def crear_texto_resumen(self, stats):
        """Crea texto para resumen general"""
        total = stats["partidas_totales"]
        victorias = stats["victorias"]
        derrotas = stats["derrotas"]
        promedio = stats["promedio_intentos"]
        
        if total > 0:
            porcentaje = (victorias / total) * 100
            texto = f"""
            • Partidas totales: {total}
            • Victorias: {victorias} ({porcentaje:.1f}%)
            • Derrotas: {derrotas}
            • Promedio de intentos: {promedio:.2f}
            • Ratio V/D: {victorias}:{derrotas}
            • Eficiencia: {(victorias/promedio if promedio > 0 else 0):.2f}
            """
        else:
            texto = "Aún no hay partidas registradas."
        
        return texto
    
    def crear_texto_dificultad(self, stats):
        """Crea texto para estadísticas por dificultad"""
        texto = ""
        for dificultad, datos in stats["por_dificultad"].items():
            if datos['total'] > 0:
                porcentaje = datos['porcentaje']
                texto += f"""
            • {dificultad.upper()}:
              - Partidas: {datos['total']}
              - Victorias: {datos['victorias']} ({porcentaje:.1f}%)
              - Derrotas: {datos['total'] - datos['victorias']}
            """
            else:
                texto += f"\n            • {dificultad.upper()}: Sin partidas"
        
        return texto if texto else "Sin datos por dificultad"
    
    def crear_texto_historial(self):
        """Crea texto para historial reciente"""
        try:
            ranking = self.gestor_db.obtener_ranking(5)
            if ranking:
                texto = "Últimas 5 victorias:\n"
                for i, (palabra, intentos, tiempo, fecha, dificultad) in enumerate(ranking, 1):
                    texto += f"            {i}. {palabra} ({intentos} intentos, {tiempo}s, {dificultad})\n"
            else:
                texto = "No hay victorias recientes."
        except:
            texto = "No se pudo cargar el historial."
        
        return texto
    
    def crear_texto_recomendaciones(self, stats):
        """Crea texto de recomendaciones"""
        total = stats["partidas_totales"]
        
        if total == 0:
            return "¡Comienza a jugar para obtener recomendaciones!"
        
        # Analizar datos para recomendaciones
        mejor_dif = max(stats["por_dificultad"].items(), 
                       key=lambda x: x[1]['porcentaje'] if x[1]['total'] > 0 else 0)
        
        porcentaje_victorias = (stats["victorias"] / total) * 100 if total > 0 else 0
        
        recomendaciones = []
        
        if porcentaje_victorias < 30:
            recomendaciones.append("• Prueba con la dificultad FÁCIL para ganar confianza")
        elif porcentaje_victorias > 70:
            recomendaciones.append("• Intenta con la dificultad DIFÍCIL para un mayor desafío")
        
        if stats["promedio_intentos"] > 5:
            recomendaciones.append("• Intenta usar más pistas estratégicamente")
        
        if mejor_dif[1]['total'] > 0 and mejor_dif[1]['porcentaje'] > 50:
            recomendaciones.append(f"• Tu mejor rendimiento es en {mejor_dif[0].upper()}, ¡sigue así!")
        
        if not recomendaciones:
            recomendaciones.append("• ¡Sigue practicando para mejorar tus habilidades!")
        
        return "\n".join(recomendaciones)
    
    def mostrar_ranking(self):
        """Muestra el ranking de mejores partidas (versión mejorada)"""
        try:
            ranking = self.gestor_db.obtener_ranking(15)  # Mostrar 15 en lugar de 10
            
            if ranking:
                # Crear ventana emergente más grande
                ventana_ranking = tk.Toplevel(self)
                ventana_ranking.title("🏆 RANKING - Top 15 Mejores Partidas")
                ventana_ranking.geometry("800x550")
                ventana_ranking.configure(bg=self.colores["fondo_principal"])
                ventana_ranking.resizable(True, True)
                
                # Centrar ventana
                ventana_ranking.update_idletasks()
                width = ventana_ranking.winfo_width()
                height = ventana_ranking.winfo_height()
                x = (ventana_ranking.winfo_screenwidth() // 2) - (width // 2)
                y = (ventana_ranking.winfo_screenheight() // 2) - (height // 2)
                ventana_ranking.geometry(f'{width}x{height}+{x}+{y}')
                
                # Frame principal
                main_frame = tk.Frame(ventana_ranking, bg=self.colores["fondo_principal"], 
                                     padx=20, pady=20)
                main_frame.pack(fill=tk.BOTH, expand=True)
                
                # Título con medallas
                titulo_frame = tk.Frame(main_frame, bg=self.colores["amarillo"], height=70)
                titulo_frame.pack(fill=tk.X, pady=(0, 20))
                titulo_frame.pack_propagate(False)
                
                tk.Label(
                    titulo_frame,
                    text="🏆 TOP 15 MEJORES PARTIDAS 🏆",
                    font=("Arial", 18, "bold"),
                    fg="white",
                    bg=self.colores["amarillo"]
                ).pack(expand=True, pady=10)
                
                # Explicación
                tk.Label(
                    main_frame,
                    text="Ordenadas por: 1) Menor número de intentos 2) Menor tiempo 3) Mayor dificultad",
                    font=("Arial", 9, "italic"),
                    fg=self.colores["texto_secundario"],
                    bg=self.colores["fondo_principal"]
                ).pack(pady=(0, 15))
                
                # Frame para tabla con scroll
                frame_contenedor = tk.Frame(main_frame, bg=self.colores["fondo_principal"])
                frame_contenedor.pack(fill=tk.BOTH, expand=True)
                
                # Canvas para scroll
                canvas = tk.Canvas(frame_contenedor, bg=self.colores["fondo_principal"], 
                                 highlightthickness=0)
                scrollbar = ttk.Scrollbar(frame_contenedor, orient="vertical", 
                                         command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg=self.colores["fondo_principal"])
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
                # Crear tabla manualmente para mejor control
                headers = ["POS", "PALABRA", "INTENTOS", "TIEMPO", "DIFICULTAD", "FECHA"]
                
                # Encabezados
                header_frame = tk.Frame(scrollable_frame, bg=self.colores["fondo_terciario"])
                header_frame.pack(fill=tk.X, pady=(0, 5))
                
                for i, header in enumerate(headers):
                    tk.Label(
                        header_frame,
                        text=header,
                        font=("Arial", 11, "bold"),
                        bg=self.colores["fondo_terciario"],
                        fg=self.colores["texto_principal"],
                        padx=10,
                        pady=8,
                        width=12 if i > 0 else 6
                    ).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
                    header_frame.grid_columnconfigure(i, weight=1)
                
                # Filas de datos
                for idx, (palabra, intentos, tiempo, fecha, dificultad) in enumerate(ranking, 1):
                    # Determinar color de fondo según posición
                    if idx == 1:
                        bg_color = "#ffd700"  # Oro
                        fg_color = "black"
                    elif idx == 2:
                        bg_color = "#c0c0c0"  # Plata
                        fg_color = "black"
                    elif idx == 3:
                        bg_color = "#cd7f32"  # Bronce
                        fg_color = "black"
                    else:
                        if idx % 2 == 0:
                            bg_color = self.colores["fondo_secundario"]
                        else:
                            bg_color = "#2a2a4e"
                        fg_color = self.colores["texto_principal"]
                    
                    # Frame para la fila
                    row_frame = tk.Frame(scrollable_frame, bg=bg_color)
                    row_frame.pack(fill=tk.X, pady=1)
                    
                    # Datos
                    datos = [
                        f"{idx}°",
                        palabra,
                        str(intentos),
                        f"{tiempo}s",
                        dificultad,
                        fecha[:10]
                    ]
                    
                    for i, dato in enumerate(datos):
                        tk.Label(
                            row_frame,
                            text=dato,
                            font=("Arial", 10, "bold" if idx <= 3 else "normal"),
                            bg=bg_color,
                            fg=fg_color,
                            padx=10,
                            pady=6,
                            width=12 if i > 0 else 6
                        ).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
                        row_frame.grid_columnconfigure(i, weight=1)
                
                # Botón cerrar
                tk.Button(
                    main_frame,
                    text="CERRAR",
                    font=("Arial", 11, "bold"),
                    bg=self.colores["rojo"],
                    fg="white",
                    command=ventana_ranking.destroy,
                    padx=30,
                    pady=10
                ).pack(pady=20)
                
            else:
                messagebox.showinfo(
                    "Ranking Vacío",
                    "🎮 Aún no hay partidas ganadas registradas.\n¡Juega y gana algunas partidas para aparecer en el ranking!"
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"⚠️ No se pudo cargar el ranking:\n{e}")
    
    def resetear_estadisticas(self):
        """Pregunta al usuario si quiere resetear las estadísticas"""
        respuesta = messagebox.askyesno(
            "⚠️ Confirmar Reseteo de Estadísticas",
            "¿Estás seguro de que quieres RESETEAR TODAS LAS ESTADÍSTICAS?\n\n"
            "⚠️ ADVERTENCIA:\n"
            "• Se eliminarán TODOS los registros de partidas\n"
            "• Se borrará el COMPLETO historial de ranking\n"
            "• Se perderán TODAS las métricas acumuladas\n"
            "• Esta acción NO SE PUEDE DESHACER\n\n"
            "¿Realmente deseas continuar?"
        )
        
        if respuesta:
            # Preguntar confirmación adicional
            confirmacion = messagebox.askyesno(
                "⚠️ ÚLTIMA CONFIRMACIÓN",
                "¿ESTÁS ABSOLUTAMENTE SEGURO?\n\n"
                "Esta eliminará permanentemente:\n"
                "✅ Todas tus victorias\n"
                "✅ Todas tus derrotas\n"
                "✅ Todo tu progreso\n"
                "✅ Todo el ranking\n\n"
                "¿CONFIRMAR ELIMINACIÓN TOTAL?"
            )
            
            if confirmacion:
                try:
                    self.gestor_db.cursor.execute("DELETE FROM estadisticas")
                    self.gestor_db.conn.commit()
                    self.actualizar_estadisticas()
                    
                    messagebox.showinfo(
                        "✅ Estadísticas Reseteadas",
                        "Todas las estadísticas han sido eliminadas correctamente.\n\n"
                        "El panel se ha actualizado y ahora está vacío.\n"
                        "¡Comienza de nuevo y construye tu historial!"
                    )
                    
                except Exception as e:
                    messagebox.showerror(
                        "❌ Error al Resetear",
                        f"No se pudieron resetear las estadísticas:\n\n{e}"
                    )