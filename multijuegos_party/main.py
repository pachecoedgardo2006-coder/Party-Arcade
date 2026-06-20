# main.py
from src.engine.manager import GameManager
from src.scenes.main_menu import MainMenu

if __name__ == "__main__":
    manager = GameManager()
    
    # Establecemos el menú principal como la pantalla de inicio por defecto
    manager.cambiar_escena(MainMenu(manager))
    
    manager.ejecutar()