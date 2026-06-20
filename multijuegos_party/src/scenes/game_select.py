import pygame
from config import settings
from src.scenes.base_scene import BaseScene
from src.ui.components import Boton
from src.modes.gravity_runner.runner_game import RunnerGame

class GameSelect(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fuente_titulo = pygame.font.SysFont("consolas", 36, bold=True)
        
        # Botón para iniciar el Modo 1 (Gravity Runner)
        self.btn_runner = Boton(
            settings.ANCHO // 2 - 200, 220, 400, 55,
            "1. GRAVITY RUNNER", settings.COLOR_PLATAFORMA, settings.LINEA_NEON, settings.TEXTO_COLOR
        )
        
        # Placeholder para los próximos juegos del compendio
        self.btn_bloqueado = Boton(
            settings.ANCHO // 2 - 200, 290, 400, 55,
            "2. MODO BLOQUEADO (PRÓXIMAMENTE)", settings.COLOR_PLATAFORMA, settings.COLOR_PLATAFORMA, (100, 100, 120)
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
                
            if self.btn_volver.manejar_eventos(evento):
                self.manager.cambiar_escena(MainMenu(self.manager))

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(settings.COLOR_FONDO)
        
        txt_titulo = self.fuente_titulo.render("SELECCIONA UN JUEGO", True, settings.TEXTO_COLOR)
        pantalla.blit(txt_titulo, (settings.ANCHO // 2 - txt_titulo.get_width() // 2, 100))
        
        self.btn_runner.dibujar(pantalla)
        self.btn_bloqueado.dibujar(pantalla)
        self.btn_volver.dibujar(pantalla)