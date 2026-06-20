# src/scenes/game_select.py
import pygame
from config import settings
from src.scenes.base_scene import BaseScene
from src.ui.components import Boton
from src.modes.gravity_runner.runner_game import RunnerGame
from src.modes.battle_snake.battle_snake import battleSnakeGame
# Importamos la clase principal de la escena del modo 3
from src.modes.memory_grid.memory_game import MemoryGame

class GameSelect(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fuente_titulo = pygame.font.SysFont("consolas", 36, bold=True)
        
        # Botón para iniciar el Modo 1 (Gravity Runner)
        self.btn_runner = Boton(
            settings.ANCHO // 2 - 200, 200, 400, 50,
            "1. GRAVITY RUNNER", settings.COLOR_PLATAFORMA, settings.LINEA_NEON, settings.TEXTO_COLOR
        )
        
        # Botón para iniciar el Modo 2 (Snake)
        self.btn_snake = Boton(
            settings.ANCHO // 2 - 200, 265, 400, 50,
            "2. SNAKE VERSUS", settings.COLOR_PLATAFORMA, settings.LINEA_NEON, settings.TEXTO_COLOR
        )
        
        # 🚀 NUEVO: Botón para iniciar el Modo 3 (Memory Grid)
        self.btn_memory = Boton(
            settings.ANCHO // 2 - 200, 330, 400, 50,
            "3. MEMORY GRID (5X10)", settings.COLOR_PLATAFORMA, settings.LINEA_NEON, settings.TEXTO_COLOR
        )
        
        self.btn_volver = Boton(
            settings.ANCHO // 2 - 100, settings.ALTO - 120, 200, 45,
            "VOLVER", settings.COLOR_PLATAFORMA, settings.JUGADOR_COLOR, settings.TEXTO_COLOR
        )

    def manejar_eventos(self, eventos):
        # Importación local para prevenir el ciclo infinito de imports
        from src.scenes.main_menu import MainMenu
        
        for evento in eventos:
            if self.btn_runner.manejar_eventos(evento):
                self.manager.cambiar_escena(RunnerGame(self.manager))
                
            if self.btn_snake.manejar_eventos(evento):
                self.manager.cambiar_escena(battleSnakeGame(self.manager))
                
            # Capturamos el evento del nuevo botón para lanzar el Modo 3
            if self.btn_memory.manejar_eventos(evento):
                self.manager.cambiar_escena(MemoryGame(self.manager))
                
            if self.btn_volver.manejar_eventos(evento):
                self.manager.cambiar_escena(MainMenu(self.manager))

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(settings.COLOR_FONDO)
        
        txt_titulo = self.fuente_titulo.render("SELECCIONA UN JUEGO", True, settings.TEXTO_COLOR)
        pantalla.blit(txt_titulo, (settings.ANCHO // 2 - txt_titulo.get_width() // 2, 100))
        
        # Renderizamos los componentes interactivos en pantalla
        self.btn_runner.dibujar(pantalla)
        self.btn_snake.dibujar(pantalla)
        self.btn_memory.dibujar(pantalla) # El botón del modo 3 ahora es visible y clickeable
        self.btn_volver.dibujar(pantalla)