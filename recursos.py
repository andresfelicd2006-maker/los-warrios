import os
from PIL import Image, ImageTk
import tkinter as tk

class ImageManager:
    def __init__(self):
        self.images = {}
        self.load_images()
    
    def load_images(self):
        """Carga todas las imágenes necesarias"""
        try:
            # Iconos para el menú
            self.images['brain_icon'] = self.create_brain_icon()
            self.images['play_icon'] = self.create_play_icon()
            self.images['exit_icon'] = self.create_exit_icon()
            
            # Fondos y elementos del juego
            self.images['game_bg'] = self.create_game_background()
            self.images['letter_box'] = self.create_letter_box()
            self.images['letter_box_correct'] = self.create_letter_box_correct()
            self.images['heart'] = self.create_heart_icon()
            self.images['victory'] = self.create_victory_icon()
            self.images['defeat'] = self.create_defeat_icon()
            
        except Exception as e:
            print(f"Error cargando imágenes: {e}")
            # Fallback a emojis si no se pueden cargar imágenes
            self.images = self.create_fallback_images()
    
    def create_brain_icon(self):
        """Crea un icono de cerebro programáticamente"""
        from PIL import Image, ImageDraw
        
        img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Color del cerebro (naranja/rojo)
        brain_color = (255, 107, 107, 255)
        
        # Dibujar cerebro simplificado
        draw.ellipse([70, 70, 186, 186], fill=brain_color, outline=(255, 255, 255, 255), width=3)
        
        # Lóbulos
        draw.ellipse([50, 100, 110, 160], fill=brain_color)
        draw.ellipse([146, 100, 206, 160], fill=brain_color)
        
        # Surcos
        for y in range(90, 170, 20):
            draw.line([128, y, 128, y+10], fill=(255, 255, 255, 200), width=2)
        
        return ImageTk.PhotoImage(img)
    
    def create_play_icon(self):
        """Crea icono de play"""
        from PIL import Image, ImageDraw
        
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Triángulo de play
        points = [(15, 10), (15, 54), (50, 32)]
        draw.polygon(points, fill=(56, 134, 89, 255))
        
        return ImageTk.PhotoImage(img)
    
    def create_exit_icon(self):
        """Crea icono de salida"""
        from PIL import Image, ImageDraw
        
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Cruz de salida
        draw.rectangle([15, 15, 49, 49], outline=(255, 107, 107, 255), width=3)
        draw.line([20, 20, 44, 44], fill=(255, 107, 107, 255), width=3)
        draw.line([44, 20, 20, 44], fill=(255, 107, 107, 255), width=3)
        
        return ImageTk.PhotoImage(img)
    
    def create_game_background(self):
        """Crea fondo para el juego"""
        from PIL import Image, ImageDraw
        
        img = Image.new('RGB', (1200, 750), (13, 17, 23))
        draw = ImageDraw.Draw(img)
        
        # Patrón sutil de puntos
        for x in range(0, 1200, 50):
            for y in range(0, 750, 50):
                draw.ellipse([x, y, x+2, y+2], fill=(40, 45, 60, 50))
        
        return ImageTk.PhotoImage(img)
    
    def create_letter_box(self):
        """Crea imagen para cuadro de letra vacío"""
        from PIL import Image, ImageDraw
        
        img = Image.new('RGBA', (70, 80), (22, 27, 34, 255))
        draw = ImageDraw.Draw(img)
        
        # Borde
        draw.rectangle([0, 0, 69, 79], outline=(48, 54, 61, 255), width=2)
        
        # Efecto 3D sutil
        draw.line([1, 1, 68, 1], fill=(40, 45, 52, 255), width=1)
        draw.line([1, 1, 1, 78], fill=(40, 45, 52, 255), width=1)
        
        return ImageTk.PhotoImage(img)
    
    def create_letter_box_correct(self):
        """Crea imagen para cuadro de letra correcta"""
        from PIL import Image, ImageDraw
        
        img = Image.new('RGBA', (70, 80), (35, 134, 54, 255))
        draw = ImageDraw.Draw(img)
        
        # Borde
        draw.rectangle([0, 0, 69, 79], outline=(45, 164, 78, 255), width=2)
        
        # Efecto brillo
        draw.line([1, 1, 68, 1], fill=(56, 174, 89, 255), width=1)
        draw.line([1, 1, 1, 78], fill=(56, 174, 89, 255), width=1)
        
        return ImageTk.PhotoImage(img)
    
    def create_heart_icon(self):
        """Crea icono de corazón"""
        from PIL import Image, ImageDraw
        
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Forma de corazón
        # Parte izquierda
        draw.ellipse([0, 0, 20, 20], fill=(255, 107, 107, 255))
        # Parte derecha
        draw.ellipse([12, 0, 32, 20], fill=(255, 107, 107, 255))
        # Parte inferior
        points = [(0, 10), (16, 31), (32, 10)]
        draw.polygon(points, fill=(255, 107, 107, 255))
        
        return ImageTk.PhotoImage(img)
    
    def create_victory_icon(self):
        """Crea icono de victoria"""
        from PIL import Image, ImageDraw
        
        img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Copa
        draw.ellipse([40, 80, 88, 100], fill=(255, 215, 0, 255))
        draw.rectangle([54, 40, 74, 80], fill=(255, 215, 0, 255))
        
        # Base
        draw.rectangle([44, 100, 84, 110], fill=(255, 215, 0, 255))
        
        # Estrellas alrededor
        for x, y in [(20, 20), (108, 20), (64, 10), (30, 60), (98, 60)]:
            self.draw_star(draw, x, y, 10, (255, 215, 0, 200))
        
        return ImageTk.PhotoImage(img)
    
    def create_defeat_icon(self):
        """Crea icono de derrota"""
        from PIL import Image, ImageDraw
        
        img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calavera
        draw.ellipse([40, 20, 88, 68], fill=(200, 200, 200, 255))
        
        # Ojos
        draw.ellipse([52, 40, 60, 48], fill=(0, 0, 0, 255))
        draw.ellipse([68, 40, 76, 48], fill=(0, 0, 0, 255))
        
        # Boca
        draw.arc([52, 50, 76, 60], 0, 180, fill=(0, 0, 0, 255), width=3)
        
        # Huesos cruzados
        draw.rectangle([20, 70, 108, 78], fill=(200, 200, 200, 255))
        draw.rectangle([64, 30, 72, 118], fill=(200, 200, 200, 255))
        
        return ImageTk.PhotoImage(img)
    
    def draw_star(self, draw, x, y, size, color):
        """Dibuja una estrella"""
        points = []
        for i in range(5):
            angle = 4 * 3.14159 * i / 5 - 3.14159 / 2
            points.extend([
                x + size * 0.5 * (1 + 0.5 * (i % 2)) * 3.14159 * angle,
                y + size * 0.5 * (1 + 0.5 * (i % 2)) * 3.14159 * angle
            ])
        draw.polygon(points, fill=color)
    
    def create_fallback_images(self):
        """Crea imágenes de fallback con emojis para tkinter"""
        return {
            'brain_icon': None,
            'play_icon': None,
            'exit_icon': None,
            'game_bg': None,
            'letter_box': None,
            'letter_box_correct': None,
            'heart': None,
            'victory': None,
            'defeat': None
        }