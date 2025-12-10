# juego_logica.py
from datetime import datetime
from typing import Dict, List, Optional
from gestor_bd import GestorBaseDatos
from configuracion import Configuracion

class JuegoLogica:
    """Clase que maneja la lógica principal del juego"""
    
    def __init__(self, gestor_db: GestorBaseDatos, config: Configuracion):
        self.gestor_db = gestor_db
        self.config = config
        self.reiniciar_juego()
    
    def reiniciar_juego(self):
        """Reinicia el estado del juego"""
        self.palabra_secreta = self.gestor_db.obtener_palabra_aleatoria(
            self.config.obtener("dificultad")
        )
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.intentos = 0
        self.max_intentos = self.config.obtener("max_intentos")
        self.inicio_tiempo = datetime.now()
        self.game_over = False
        self.victoria = False
        self.tiempo_final = 0
        
        # Palabras intentadas completas
        self.palabras_intentadas = []
    
    def procesar_intento(self, entrada: str) -> Dict:
        """Procesa un intento del jugador (letra o palabra completa)"""
        entrada = entrada.upper().strip()
        
        if self.game_over:
            return {"estado": "game_over", "mensaje": "El juego ha terminado"}
        
        if not entrada:
            return {"estado": "error", "mensaje": "Entrada vacía"}
        
        # Verificar si es una palabra completa
        if len(entrada) > 1 and self.config.obtener("palabra_completa", False):
            return self.procesar_palabra_completa(entrada)
        
        # Procesar como letra individual
        return self.procesar_letra(entrada)
    
    def procesar_letra(self, letra: str) -> Dict:
        """Procesa una letra individual"""
        if len(letra) != 1 or not letra.isalpha():
            return {"estado": "error", "mensaje": "Debe ser una sola letra (A-Z)"}
        
        if letra in self.letras_adivinadas or letra in self.letras_incorrectas:
            return {"estado": "error", "mensaje": f"La letra '{letra}' ya fue intentada"}
        
        if letra in self.palabra_secreta:
            self.letras_adivinadas.add(letra)
            
            # Verificar si ganó
            if self.verificar_victoria():
                return self.finalizar_victoria()
            
            return {"estado": "acierto", "letra": letra}
        else:
            self.letras_incorrectas.add(letra)
            self.intentos += 1
            
            if self.intentos >= self.max_intentos:
                return self.finalizar_derrota()
            
            return {"estado": "fallo", "letra": letra}
    
    def procesar_palabra_completa(self, palabra: str) -> Dict:
        """Procesa una palabra completa"""
        if len(palabra) != len(self.palabra_secreta):
            return {"estado": "error", "mensaje": f"La palabra debe tener {len(self.palabra_secreta)} letras"}
        
        self.palabras_intentadas.append(palabra)
        self.intentos += 1
        
        if palabra == self.palabra_secreta:
            # Adivinar todas las letras
            for letra in self.palabra_secreta:
                self.letras_adivinadas.add(letra)
            return self.finalizar_victoria()
        else:
            if self.intentos >= self.max_intentos:
                return self.finalizar_derrota()
            
            # Dar pistas sobre letras correctas
            letras_correctas = []
            for i, letra in enumerate(palabra):
                if i < len(self.palabra_secreta) and letra == self.palabra_secreta[i]:
                    letras_correctas.append(f"Posición {i+1}: {letra}")
            
            mensaje = f"Palabra incorrecta"
            if letras_correctas:
                mensaje += f". Letras correctas: {', '.join(letras_correctas)}"
            
            return {"estado": "palabra_incorrecta", "mensaje": mensaje}
    
    def verificar_victoria(self) -> bool:
        """Verifica si el jugador ha ganado"""
        return all(letra in self.letras_adivinadas for letra in self.palabra_secreta)
    
    def finalizar_victoria(self) -> Dict:
        """Finaliza el juego con victoria"""
        self.game_over = True
        self.victoria = True
        self.tiempo_final = (datetime.now() - self.inicio_tiempo).seconds
        
        # Guardar en base de datos
        self.gestor_db.guardar_partida(
            self.palabra_secreta,
            self.intentos,
            True,
            self.tiempo_final,
            self.config.obtener("dificultad")
        )
        
        return {
            "estado": "victoria",
            "mensaje": f"¡VICTORIA! Adivinaste '{self.palabra_secreta}' en {self.intentos} intentos y {self.tiempo_final} segundos",
            "palabra": self.palabra_secreta,
            "intentos": self.intentos,
            "tiempo": self.tiempo_final
        }
    
    def finalizar_derrota(self) -> Dict:
        """Finaliza el juego con derrota"""
        self.game_over = True
        self.victoria = False
        tiempo = (datetime.now() - self.inicio_tiempo).seconds
        
        # Guardar en base de datos
        self.gestor_db.guardar_partida(
            self.palabra_secreta,
            self.intentos,
            False,
            tiempo,
            self.config.obtener("dificultad")
        )
        
        return {
            "estado": "derrota",
            "mensaje": f"¡FIN DEL JUEGO! La palabra era: {self.palabra_secreta}",
            "palabra": self.palabra_secreta,
            "intentos": self.intentos,
            "tiempo": tiempo
        }
    
    def obtener_palabra_oculta(self) -> str:
        """Obtiene la palabra con letras ocultas"""
        resultado = []
        for letra in self.palabra_secreta:
            if letra in self.letras_adivinadas:
                resultado.append(letra)
            else:
                resultado.append("_")
        return " ".join(resultado)
    
    def obtener_pistas(self) -> List[str]:
        """Devuelve pistas sobre la palabra"""
        if not self.config.obtener("mostrar_pistas", True):
            return []
        
        pistas = []
        
        # Pista básica: longitud
        if self.intentos >= 0:
            pistas.append(f"Longitud: {len(self.palabra_secreta)} letras")
        
        # Pista después de 1 intento: categoría
        if self.intentos >= 1:
            # Obtener categoría de la base de datos
            self.gestor_db.cursor.execute(
                "SELECT categoria FROM palabras WHERE palabra = ?",
                (self.palabra_secreta,)
            )
            resultado = self.gestor_db.cursor.fetchone()
            if resultado:
                pistas.append(f"Categoría: {resultado[0]}")
        
        # Pista después de 2 intentos: primera letra
        if self.intentos >= 2:
            pistas.append(f"Primera letra: {self.palabra_secreta[0]}")
        
        # Pista después de 3 intentos: última letra
        if self.intentos >= 3 and len(self.palabra_secreta) > 1:
            pistas.append(f"Última letra: {self.palabra_secreta[-1]}")
        
        # Pista especial para dificultad DIFICIL
        if self.config.obtener("dificultad") == "DIFICIL" and self.intentos >= 4:
            # Mostrar una letra aleatoria que no haya sido adivinada
            letras_no_adivinadas = [l for l in self.palabra_secreta if l not in self.letras_adivinadas]
            if letras_no_adivinadas:
                import random
                letra_pista = random.choice(letras_no_adivinadas)
                pistas.append(f"Contiene la letra: {letra_pista}")
        
        return pistas
    
    def obtener_tiempo_transcurrido(self) -> int:
        """Obtiene el tiempo transcurrido en segundos"""
        if not self.game_over:
            return (datetime.now() - self.inicio_tiempo).seconds
        return self.tiempo_final if self.victoria else (datetime.now() - self.inicio_tiempo).seconds
    
    def obtener_estado_actual(self) -> Dict:
        """Obtiene el estado actual del juego"""
        return {
            "palabra": self.palabra_secreta,
            "oculta": self.obtener_palabra_oculta(),
            "intentos": self.intentos,
            "max_intentos": self.max_intentos,
            "letras_adivinadas": list(self.letras_adivinadas),
            "letras_incorrectas": list(self.letras_incorrectas),
            "game_over": self.game_over,
            "victoria": self.victoria,
            "tiempo": self.obtener_tiempo_transcurrido(),
            "dificultad": self.config.obtener("dificultad")
        }
    
    def cambiar_dificultad(self, dificultad: str):
        """Cambia la dificultad del juego"""
        self.config.establecer_dificultad(dificultad)
        self.max_intentos = self.config.obtener("max_intentos")