# gestor_bd.py
import sqlite3
from datetime import datetime
from typing import Dict, List, Tuple

class GestorBaseDatos:
    """Clase para manejar la base de datos SQLite del juego"""
    
    def __init__(self, nombre_db="juego_palabras.db"):
        self.conn = sqlite3.connect(nombre_db)
        self.cursor = self.conn.cursor()
        self.crear_tablas()
    
    def crear_tablas(self):
        """Crea las tablas necesarias si no existen"""
        # Tabla de estadísticas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS estadisticas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                palabra TEXT NOT NULL,
                intentos INTEGER NOT NULL,
                victoria INTEGER NOT NULL,
                tiempo_segundos INTEGER,
                dificultad TEXT NOT NULL
            )
        ''')
        
        # Tabla de palabras por dificultad
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS palabras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                palabra TEXT UNIQUE NOT NULL,
                dificultad TEXT NOT NULL,
                categoria TEXT NOT NULL
            )
        ''')
        
        # Verificar si hay palabras
        self.cursor.execute("SELECT COUNT(*) FROM palabras")
        if self.cursor.fetchone()[0] == 0:
            self.insertar_palabras_por_defecto()
        
        self.conn.commit()
    
    def insertar_palabras_por_defecto(self):
        """Inserta palabras iniciales en la base de datos"""
        palabras_facil = [
            ("SOL", "FACIL", "NATURALEZA"),
            ("LUNA", "FACIL", "NATURALEZA"),
            ("MESA", "FACIL", "OBJETOS"),
            ("SILLA", "FACIL", "OBJETOS"),
            ("CASA", "FACIL", "LUGARES"),
            ("PERRO", "FACIL", "ANIMALES"),
            ("GATO", "FACIL", "ANIMALES"),
            ("AGUA", "FACIL", "ELEMENTOS"),
            ("FUEGO", "FACIL", "ELEMENTOS"),
            ("LIBRO", "FACIL", "OBJETOS"),
            ("LAPIZ", "FACIL", "OBJETOS"),
            ("FLOR", "FACIL", "NATURALEZA"),
            ("ARBOL", "FACIL", "NATURALEZA"),
            ("RIO", "FACIL", "NATURALEZA"),
            ("PLAYA", "FACIL", "LUGARES"),
            ("CIELO", "FACIL", "NATURALEZA"),
            ("ESTRELLA", "FACIL", "NATURALEZA"),
            ("MANO", "FACIL", "CUERPO"),
            ("PIE", "FACIL", "CUERPO"),
            ("CABEZA", "FACIL", "CUERPO")
        ]
        
        palabras_medio = [
            ("PYTHON", "MEDIO", "PROGRAMACION"),
            ("JAVA", "MEDIO", "PROGRAMACION"),
            ("HTML", "MEDIO", "TECNOLOGIA"),
            ("CSS", "MEDIO", "TECNOLOGIA"),
            ("MYSQL", "MEDIO", "BASE_DATOS"),
            ("LINUX", "MEDIO", "SISTEMA"),
            ("WINDOWS", "MEDIO", "SISTEMA"),
            ("OFFICE", "MEDIO", "SOFTWARE"),
            ("GOOGLE", "MEDIO", "INTERNET"),
            ("FACEBOOK", "MEDIO", "REDES"),
            ("TWITTER", "MEDIO", "REDES"),
            ("YOUTUBE", "MEDIO", "VIDEO"),
            ("CAMARA", "MEDIO", "TECNOLOGIA"),
            ("CELULAR", "MEDIO", "TECNOLOGIA"),
            ("COMPUTADORA", "MEDIO", "TECNOLOGIA"),
            ("TECLADO", "MEDIO", "HARDWARE"),
            ("MONITOR", "MEDIO", "HARDWARE"),
            ("IMPRESORA", "MEDIO", "HARDWARE"),
            ("ESCANER", "MEDIO", "HARDWARE"),
            ("AURICULARES", "MEDIO", "HARDWARE")
        ]
        
        palabras_dificil = [
            ("JAVASCRIPT", "DIFICIL", "PROGRAMACION"),
            ("REACT", "DIFICIL", "PROGRAMACION"),
            ("ANGULAR", "DIFICIL", "PROGRAMACION"),
            ("VUE", "DIFICIL", "PROGRAMACION"),
            ("DOCKER", "DIFICIL", "DEVOPS"),
            ("KUBERNETES", "DIFICIL", "DEVOPS"),
            ("MICROSERVICIOS", "DIFICIL", "ARQUITECTURA"),
            ("INTELIGENCIA", "DIFICIL", "IA"),
            ("ARTIFICIAL", "DIFICIL", "IA"),
            ("ALGORITMO", "DIFICIL", "PROGRAMACION"),
            ("CRIPTOCURRENCY", "DIFICIL", "FINANZAS"),
            ("BLOCKCHAIN", "DIFICIL", "TECNOLOGIA"),
            ("CIBERSEGURIDAD", "DIFICIL", "SEGURIDAD"),
            ("VULNERABILIDAD", "DIFICIL", "SEGURIDAD"),
            ("ENCRIPTACION", "DIFICIL", "SEGURIDAD"),
            ("BIGDATA", "DIFICIL", "DATOS"),
            ("DATA SCIENCE", "DIFICIL", "CIENCIA"),
            ("MACHINE LEARNING", "DIFICIL", "IA"),
            ("DEEP LEARNING", "DIFICIL", "IA"),
            ("NEURAL NETWORK", "DIFICIL", "IA")
        ]
        
        # Insertar todas las palabras
        todas_palabras = palabras_facil + palabras_medio + palabras_dificil
        
        self.cursor.executemany(
            "INSERT INTO palabras (palabra, dificultad, categoria) VALUES (?, ?, ?)",
            todas_palabras
        )
    
    def guardar_partida(self, palabra: str, intentos: int, victoria: bool, tiempo: int, dificultad: str):
        """Guarda los resultados de una partida"""
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO estadisticas (fecha, palabra, intentos, victoria, tiempo_segundos, dificultad)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (fecha, palabra, intentos, 1 if victoria else 0, tiempo, dificultad))
        self.conn.commit()
    
    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas generales del juego"""
        # Victorias totales
        self.cursor.execute("SELECT COUNT(*) FROM estadisticas WHERE victoria = 1")
        victorias = self.cursor.fetchone()[0]
        
        # Derrotas totales
        self.cursor.execute("SELECT COUNT(*) FROM estadisticas WHERE victoria = 0")
        derrotas = self.cursor.fetchone()[0]
        
        # Promedio de intentos en victorias
        self.cursor.execute("SELECT AVG(intentos) FROM estadisticas WHERE victoria = 1")
        avg_intentos = self.cursor.fetchone()[0] or 0
        
        # Total partidas
        total = victorias + derrotas
        
        # Estadísticas por dificultad
        stats_dificultad = {}
        for dificultad in ["FACIL", "MEDIO", "DIFICIL"]:
            self.cursor.execute(
                "SELECT COUNT(*) FROM estadisticas WHERE victoria = 1 AND dificultad = ?",
                (dificultad,)
            )
            victorias_dif = self.cursor.fetchone()[0]
            
            self.cursor.execute(
                "SELECT COUNT(*) FROM estadisticas WHERE dificultad = ?",
                (dificultad,)
            )
            total_dif = self.cursor.fetchone()[0]
            
            if total_dif > 0:
                porcentaje = (victorias_dif / total_dif) * 100
            else:
                porcentaje = 0
            
            stats_dificultad[dificultad.lower()] = {
                "victorias": victorias_dif,
                "total": total_dif,
                "porcentaje": round(porcentaje, 1)
            }
        
        return {
            "victorias": victorias,
            "derrotas": derrotas,
            "partidas_totales": total,
            "promedio_intentos": round(avg_intentos, 2) if avg_intentos else 0,
            "por_dificultad": stats_dificultad
        }
    
    def obtener_palabra_aleatoria(self, dificultad: str) -> str:
        """Obtiene una palabra aleatoria según la dificultad"""
        self.cursor.execute(
            "SELECT palabra FROM palabras WHERE dificultad = ? ORDER BY RANDOM() LIMIT 1",
            (dificultad,)
        )
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else self.obtener_palabra_alternativa(dificultad)
    
    def obtener_palabra_alternativa(self, dificultad: str) -> str:
        """Obtiene una palabra alternativa si no hay para la dificultad"""
        if dificultad == "FACIL":
            return "PYTHON"
        elif dificultad == "MEDIO":
            return "PROGRAMACION"
        else:
            return "DESAFIANTE"
    
    def obtener_ranking(self, limite: int = 10, dificultad: str = None):
        """Obtiene el ranking de mejores partidas"""
        if dificultad:
            self.cursor.execute('''
                SELECT palabra, intentos, tiempo_segundos, fecha, dificultad 
                FROM estadisticas 
                WHERE victoria = 1 AND dificultad = ?
                ORDER BY intentos ASC, tiempo_segundos ASC 
                LIMIT ?
            ''', (dificultad, limite))
        else:
            self.cursor.execute('''
                SELECT palabra, intentos, tiempo_segundos, fecha, dificultad 
                FROM estadisticas 
                WHERE victoria = 1 
                ORDER BY intentos ASC, tiempo_segundos ASC 
                LIMIT ?
            ''', (limite,))
        
        return self.cursor.fetchall()
    
    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        self.conn.close()

    # En gestor_bd.py, dentro de la clase GestorBaseDatos, añade:

def obtener_estadisticas_extendidas(self):
    """Obtiene estadísticas extendidas para análisis detallado"""
    stats = self.obtener_estadisticas()
    
    # Obtener datos adicionales
    self.cursor.execute('''
        SELECT 
            COUNT(*) as total_partidas,
            SUM(CASE WHEN victoria = 1 THEN 1 ELSE 0 END) as victorias,
            AVG(CASE WHEN victoria = 1 THEN intentos ELSE NULL END) as avg_intentos_victorias,
            AVG(tiempo_segundos) as avg_tiempo,
            MIN(tiempo_segundos) as mejor_tiempo,
            MAX(tiempo_segundos) as peor_tiempo
        FROM estadisticas
    ''')
    
    datos_extras = self.cursor.fetchone()
    
    # Obtener distribución de intentos
    self.cursor.execute('''
        SELECT intentos, COUNT(*) 
        FROM estadisticas 
        WHERE victoria = 1 
        GROUP BY intentos 
        ORDER BY intentos
    ''')
    
    distribucion_intentos = dict(self.cursor.fetchall())
    
    # Obtener última victoria
    self.cursor.execute('''
        SELECT palabra, intentos, tiempo_segundos, fecha, dificultad
        FROM estadisticas 
        WHERE victoria = 1 
        ORDER BY fecha DESC 
        LIMIT 1
    ''')
    
    ultima_victoria = self.cursor.fetchone()
    
    stats.update({
        "datos_extendidos": datos_extras,
        "distribucion_intentos": distribucion_intentos,
        "ultima_victoria": ultima_victoria,
        "total_metricas": len(distribucion_intentos)
    })
    
    return stats