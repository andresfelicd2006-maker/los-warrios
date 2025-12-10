# main.py
import tkinter as tk
from menu_inicial import MenuInicial

def main():
    """Función principal que ejecuta el menú inicial"""
    try:
        # Crear ventana principal
        root = tk.Tk()
        root.title("🎮 DESAFÍO DE PALABRAS - Menú Principal")
        
        # Configurar ícono de ventana (si existe)
        try:
            root.iconbitmap("icon.ico")
        except:
            pass
        
        # Crear menú inicial
        app = MenuInicial(root)
        
        # Iniciar el loop principal
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    print("🚀 Iniciando Desafío de Palabras...")
    main()