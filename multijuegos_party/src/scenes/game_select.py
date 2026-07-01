# src/scenes/game_select.py
import pygame
from config import settings
from src.scenes.base_scene import BaseScene
from src.ui.components import Boton
from src.modes.gravity_runner.runner_game import RunnerGame
from src.modes.battle_snake.battle_snake import battleSnakeGame
from src.modes.memory_grid.memory_game import MemoryGame
from src.modes.sumo_combat.sumo_game import SumoGame
from src.modes.retro_racing.racing_game import RacingGame

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
        
        # Botón para iniciar el Modo 3 (Memory Grid)
        self.btn_memory = Boton(
            settings.ANCHO // 2 - 200, 330, 400, 50,
            "3. MEMORY GRID (5X10)", settings.COLOR_PLATAFORMA, settings.LINEA_NEON, settings.TEXTO_COLOR
        )
        
        # Botón para iniciar el Modo 4 (Sumo Combat)
        self.btn_sumo = Boton(
            settings.ANCHO // 2 - 200, 395, 400, 50,
            "4. SUMO COMBAT", settings.COLOR_PLATAFORMA, settings.LINEA_NEON, settings.TEXTO_COLOR
        )
        
        # Botón para iniciar el Modo 5 (Retro Racing)
        self.btn_racing = Boton(
            settings.ANCHO // 2 - 200, 460, 400, 50,
            "5. RETRO RACING", settings.COLOR_PLATAFORMA, settings.LINEA_NEON, settings.TEXTO_COLOR
        )
        
        self.btn_volver = Boton(
            settings.ANCHO // 2 - 100, settings.ALTO - 100, 200, 45,
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
                
            if self.btn_memory.manejar_eventos(evento):
                self.manager.cambiar_escena(MemoryGame(self.manager))
                
            if self.btn_sumo.manejar_eventos(evento):
                self.manager.cambiar_escena(SumoGame(self.manager))
                
            if self.btn_racing.manejar_eventos(evento):
                self.manager.cambiar_escena(RacingGame(self.manager))
                
            if self.btn_volver.manejar_eventos(evento):
                self.manager.cambiar_escena(MainMenu(self.manager))

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(settings.COLOR_FONDO)
        
        txt_titulo = self.fuente_titulo.render("SELECCIONA UN JUEGO", True, settings.TEXTO_COLOR)
        pantalla.blit(txt_titulo, (settings.ANCHO // 2 - txt_titulo.get_width() // 2, 120))
        
        # Renderizamos todos los componentes interactivos
        self.btn_runner.dibujar(pantalla)
        self.btn_snake.dibujar(pantalla)
        self.btn_memory.dibujar(pantalla)
        self.btn_sumo.dibujar(pantalla)
        self.btn_racing.dibujar(pantalla)
        self.btn_volver.dibujar(pantalla)