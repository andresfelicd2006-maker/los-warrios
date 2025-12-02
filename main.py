import os
import sys

# Añadir el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from menu_inicial import MenuInicial

if __name__ == "__main__":
    app = MenuInicial()
    app.mainloop()