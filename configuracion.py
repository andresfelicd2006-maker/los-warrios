# configuracion.py
import json
import os
from typing import Dict, Any

class Configuracion:
    """Clase para manejar la configuración del juego"""
    
    def __init__(self, config_file="config_juego.json"):
        self.config_file = config_file
        self.config = self.cargar_configuracion()
    
    def cargar_configuracion(self) -> Dict[str, Any]:
        """Carga la configuración desde archivo JSON"""
        config_default = {
            "dificultad": "MEDIO",           # FACIL, MEDIO, DIFICIL
            "max_intentos": 6,               # 3-15 intentos
            "mostrar_pistas": True,          # Mostrar pistas durante el juego
            "sonido_activado": False,        # Efectos de sonido
            "tema_color": "azul",            # azul, verde, oscuro
            "tiempo_limite": 0,              # 0 = sin límite (segundos)
            "tamano_fuente": 12,             # Tamaño de fuente general
            "mostrar_tiempo": True,          # Mostrar temporizador
            "animaciones": True,             # Animaciones en interfaz
            "palabra_completa": False        # Permitir adivinar palabra completa
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Asegurar que todas las claves existan
                    for key in config_default:
                        if key not in loaded_config:
                            loaded_config[key] = config_default[key]
                    return loaded_config
        except Exception as e:
            print(f"⚠️ Error cargando configuración: {e}")
        
        return config_default
    
    def guardar_configuracion(self):
        """Guarda la configuración en archivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error guardando configuración: {e}")
    
    def obtener(self, clave: str, default=None):
        """Obtiene un valor de configuración"""
        return self.config.get(clave, default)
    
    def establecer(self, clave: str, valor):
        """Establece un valor de configuración"""
        self.config[clave] = valor
        self.guardar_configuracion()
    
    def establecer_dificultad(self, dificultad: str):
        """Establece la dificultad y ajusta configuración relacionada"""
        dificultad = dificultad.upper()
        if dificultad in ["FACIL", "MEDIO", "DIFICIL"]:
            self.establecer("dificultad", dificultad)
            
            # Ajustar intentos según dificultad
            if dificultad == "FACIL":
                self.establecer("max_intentos", 8)
            elif dificultad == "MEDIO":
                self.establecer("max_intentos", 6)
            else:  # DIFICIL
                self.establecer("max_intentos", 4)
    
    def obtener_todas(self) -> Dict[str, Any]:
        """Obtiene toda la configuración"""
        return self.config.copy()
    
    def reiniciar_a_default(self):
        """Reinicia la configuración a los valores por defecto"""
        config_default = {
            "dificultad": "MEDIO",
            "max_intentos": 6,
            "mostrar_pistas": True,
            "sonido_activado": False,
            "tema_color": "azul",
            "tiempo_limite": 0,
            "tamano_fuente": 12,
            "mostrar_tiempo": True,
            "animaciones": True,
            "palabra_completa": False
        }
        self.config = config_default
        self.guardar_configuracion()