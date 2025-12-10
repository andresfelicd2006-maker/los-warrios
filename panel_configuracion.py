# panel_configuracion.py
import tkinter as tk
from tkinter import ttk
from configuracion import Configuracion
from typing import Callable, Dict

class PanelConfiguracion(tk.Frame):
    """Panel para configurar el juego"""
    
    def __init__(self, parent, config: Configuracion, on_config_change: Callable = None, 
                 colores: Dict = None):
        super().__init__(parent)
        self.config = config
        self.on_config_change = on_config_change
        
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
        self.cargar_configuracion_actual()
    
    def configurar_interfaz(self):
        """Configura los elementos de la interfaz del panel de configuración"""
        self.configure(bg=self.colores["fondo_secundario"])
        
        # Título
        titulo_frame = tk.Frame(self, bg=self.colores["verde"], height=40)
        titulo_frame.pack(fill=tk.X)
        titulo_frame.pack_propagate(False)
        
        tk.Label(
            titulo_frame,
            text="⚙️ CONFIGURACIÓN",
            font=("Arial", 13, "bold"),
            fg="white",
            bg=self.colores["verde"]
        ).pack(expand=True)
        
        # Frame principal
        main_frame = tk.Frame(self, bg=self.colores["fondo_secundario"], padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Diccionario para guardar referencias a variables
        self.variables = {}
        
        # Configuración de dificultad
        self.agregar_seccion_dificultad(main_frame)
        
        # Otras configuraciones
        self.agregar_seccion_otras(main_frame)
        
        # Botones de acción
        self.agregar_botones_accion(main_frame)
    
    def agregar_seccion_dificultad(self, parent):
        """Agrega la sección de configuración de dificultad"""
        seccion_dificultad = tk.LabelFrame(
            parent,
            text="🎮 DIFICULTAD",
            font=("Arial", 11, "bold"),
            bg=self.colores["fondo_terciario"],
            fg=self.colores["texto_secundario"],
            padx=15,
            pady=15
        )
        seccion_dificultad.pack(fill=tk.X, pady=(0, 20))
        
        # Variable para los botones de radio
        self.var_dificultad = tk.StringVar(value="MEDIO")
        
        # Botones de radio para dificultad
        dificultades_info = [
            ("FACIL", "🟢 Fácil", "Palabras cortas y comunes\n8 intentos\nPistas generosas", 
             self.colores["verde"]),
            ("MEDIO", "🟡 Medio", "Palabras de longitud media\n6 intentos\nPistas moderadas", 
             self.colores["amarillo"]),
            ("DIFICIL", "🔴 Difícil", "Palabras largas y complejas\n4 intentos\nPistas limitadas", 
             self.colores["rojo"])
        ]
        
        for dificultad, texto, descripcion, color in dificultades_info:
            frame_opcion = tk.Frame(seccion_dificultad, bg=self.colores["fondo_terciario"], 
                                   relief=tk.RIDGE, bd=2)
            frame_opcion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Botón de radio
            rb = tk.Radiobutton(
                frame_opcion,
                text=texto,
                variable=self.var_dificultad,
                value=dificultad,
                font=("Arial", 11, "bold"),
                bg=self.colores["fondo_terciario"],
                fg=color,
                selectcolor=self.colores["fondo_terciario"],
                activebackground=self.colores["fondo_terciario"],
                activeforeground=color,
                command=self.on_cambio_dificultad,
                cursor="hand2"
            )
            rb.pack(pady=(10, 5))
            
            # Descripción
            tk.Label(
                frame_opcion,
                text=descripcion,
                font=("Arial", 9),
                bg=self.colores["fondo_terciario"],
                fg=self.colores["texto_secundario"],
                justify=tk.LEFT,
                wraplength=150
            ).pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)
    
    def agregar_seccion_otras(self, parent):
        """Agrega la sección de otras configuraciones"""
        seccion_otras = tk.LabelFrame(
            parent,
            text="🔧 OTRAS CONFIGURACIONES",
            font=("Arial", 11, "bold"),
            bg=self.colores["fondo_terciario"],
            fg=self.colores["texto_secundario"],
            padx=15,
            pady=15
        )
        seccion_otras.pack(fill=tk.X, pady=(0, 20))
        
        # Frame para controles en dos columnas
        frame_controles = tk.Frame(seccion_otras, bg=self.colores["fondo_terciario"])
        frame_controles.pack(fill=tk.X)
        
        # Columna izquierda
        col_izq = tk.Frame(frame_controles, bg=self.colores["fondo_terciario"])
        col_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Columna derecha
        col_der = tk.Frame(frame_controles, bg=self.colores["fondo_terciario"])
        col_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Configuraciones varias
        configuraciones = [
            ("Número de intentos:", "max_intentos", tk.Spinbox, 
             {"from_": 3, "to": 15, "width": 8, "bg": "#0f3460", "fg": "white"}, col_izq),
            ("Mostrar pistas:", "mostrar_pistas", tk.Checkbutton,
             {"text": "Activar", "bg": self.colores["fondo_terciario"], 
              "fg": self.colores["texto_secundario"], "selectcolor": self.colores["fondo_terciario"]}, col_izq),
            ("Mostrar tiempo:", "mostrar_tiempo", tk.Checkbutton,
             {"text": "Mostrar temporizador", "bg": self.colores["fondo_terciario"],
              "fg": self.colores["texto_secundario"], "selectcolor": self.colores["fondo_terciario"]}, col_izq),
            ("Tiempo límite (0=infinito):", "tiempo_limite", tk.Spinbox,
             {"from_": 0, "to": 600, "increment": 30, "width": 8, "bg": "#0f3460", "fg": "white"}, col_der),
            ("Efectos de sonido:", "sonido_activado", tk.Checkbutton,
             {"text": "Activar sonidos", "bg": self.colores["fondo_terciario"],
              "fg": self.colores["texto_secundario"], "selectcolor": self.colores["fondo_terciario"]}, col_der)
        ]
        
        self.controles = {}
        
        for texto, clave, tipo_widget, opciones, padre in configuraciones:
            frame = tk.Frame(padre, bg=self.colores["fondo_terciario"])
            frame.pack(fill=tk.X, pady=8)
            
            tk.Label(
                frame,
                text=texto,
                font=("Arial", 10),
                bg=self.colores["fondo_terciario"],
                fg=self.colores["texto_secundario"],
                anchor=tk.W
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Crear widget según tipo
            if tipo_widget == tk.Spinbox:
                widget = tk.Spinbox(frame, **opciones, font=("Arial", 10))
                widget.pack(side=tk.RIGHT)
                widget.bind("<KeyRelease>", self.on_cambio_config)
                widget.bind("<<Increment>>", self.on_cambio_config)
                widget.bind("<<Decrement>>", self.on_cambio_config)
                
            elif tipo_widget == tk.Checkbutton:
                var = tk.BooleanVar()
                widget = tk.Checkbutton(
                    frame,
                    variable=var,
                    **opciones,
                    font=("Arial", 10),
                    command=self.on_cambio_config,
                    cursor="hand2"
                )
                widget.pack(side=tk.RIGHT)
                self.controles[clave] = var
                continue  # No añadir a controles dict ya que usamos var
            else:
                continue
            
            self.controles[clave] = widget
    
    def agregar_botones_accion(self, parent):
        """Agrega los botones de acción"""
        seccion_botones = tk.Frame(parent, bg=self.colores["fondo_secundario"])
        seccion_botones.pack(fill=tk.X)
        
        # Botón aplicar cambios
        tk.Button(
            seccion_botones,
            text="💾 Aplicar Cambios",
            font=("Arial", 11, "bold"),
            bg=self.colores["azul"],
            fg="white",
            padx=20,
            pady=10,
            command=self.aplicar_cambios,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Botón restaurar valores por defecto
        tk.Button(
            seccion_botones,
            text="🔄 Restaurar Valores",
            font=("Arial", 11),
            bg=self.colores["fondo_terciario"],
            fg=self.colores["texto_secundario"],
            padx=20,
            pady=10,
            command=self.restaurar_default,
            cursor="hand2"
        ).pack(side=tk.RIGHT, padx=5)
    
    def cargar_configuracion_actual(self):
        """Carga la configuración actual en los controles"""
        # Cargar dificultad
        dificultad_actual = self.config.obtener("dificultad", "MEDIO")
        self.var_dificultad.set(dificultad_actual)
        
        # Cargar otros controles
        for clave, widget in self.controles.items():
            valor = self.config.obtener(clave)
            
            if isinstance(widget, tk.Spinbox):
                widget.delete(0, tk.END)
                widget.insert(0, str(valor))
            elif isinstance(widget, tk.BooleanVar):
                widget.set(valor)
    
    def on_cambio_dificultad(self):
        """Se ejecuta cuando cambia la dificultad"""
        dificultad = self.var_dificultad.get()
        
        # Ajustar intentos según dificultad
        if dificultad == "FACIL":
            self.controles["max_intentos"].delete(0, tk.END)
            self.controles["max_intentos"].insert(0, "8")
        elif dificultad == "MEDIO":
            self.controles["max_intentos"].delete(0, tk.END)
            self.controles["max_intentos"].insert(0, "6")
        else:  # DIFICIL
            self.controles["max_intentos"].delete(0, tk.END)
            self.controles["max_intentos"].insert(0, "4")
    
    def on_cambio_config(self, event=None):
        """Se ejecuta cuando hay cambios en la configuración"""
        pass
    
    def aplicar_cambios(self):
        """Aplica todos los cambios de configuración"""
        try:
            # Aplicar dificultad
            self.config.establecer("dificultad", self.var_dificultad.get())
            
            # Aplicar otros valores
            for clave, widget in self.controles.items():
                if isinstance(widget, tk.Spinbox):
                    valor = widget.get()
                    try:
                        if clave == "max_intentos":
                            self.config.establecer(clave, int(valor))
                        elif clave == "tiempo_limite":
                            self.config.establecer(clave, int(valor))
                    except ValueError:
                        pass
                elif isinstance(widget, tk.BooleanVar):
                    self.config.establecer(clave, widget.get())
            
            # Notificar al callback si existe
            if self.on_config_change:
                self.on_config_change()
            
            # Mostrar mensaje de confirmación
            tk.messagebox.showinfo(
                "✅ Configuración Actualizada",
                "Los cambios se han aplicado correctamente.\n"
                f"Dificultad actual: {self.var_dificultad.get()}"
            )
            
        except Exception as e:
            tk.messagebox.showerror(
                "❌ Error",
                f"No se pudieron aplicar los cambios:\n{e}"
            )
    
    def restaurar_default(self):
        """Restaura los valores por defecto"""
        respuesta = tk.messagebox.askyesno(
            "🔄 Restaurar Valores por Defecto",
            "¿Estás seguro de que quieres restaurar todos los valores a los predeterminados?"
        )
        
        if respuesta:
            self.config.reiniciar_a_default()
            self.cargar_configuracion_actual()
            
            if self.on_config_change:
                self.on_config_change()
            
            tk.messagebox.showinfo(
                "✅ Valores Restaurados",
                "Todos los valores se han restaurado a los predeterminados."
            )