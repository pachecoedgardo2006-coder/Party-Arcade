# src/scenes/final_results.py
import pygame
from config import settings
from src.scenes.base_scene import BaseScene
from src.ui.components import Boton

class FinalResults(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fuente_titulo = pygame.font.SysFont("consolas", 50, bold=True)
        self.fuente_ganador = pygame.font.SysFont("consolas", 36, bold=True)
        
        # Determinar el ganador final en base a los puntos del manager
        if self.manager.puntaje_j1 > self.manager.puntaje_j2:
            self.texto_ganador = "¡EL RIVAL 1 ES EL CAMPEÓN DEL HUB!"
            self.color_ganador = settings.LINEA_NEON
        elif self.manager.puntaje_j2 > self.manager.puntaje_j1:
            self.texto_ganador = "¡EL RIVAL 2 ES EL CAMPEÓN DEL HUB!"
            self.color_ganador = settings.JUGADOR_COLOR
        else:
            self.texto_ganador = "¡TENEMOS UN EMPATE ABSOLUTO!"
            self.color_ganador = settings.TEXTO_COLOR

        self.btn_menu = Boton(
            settings.ANCHO // 2 - 150, settings.ALTO - 150, 300, 50,
            "VOLVER AL MENÚ", settings.COLOR_PLATAFORMA, settings.LINEA_NEON, settings.TEXTO_COLOR
        )

    def manejar_eventos(self, eventos):
        from src.scenes.main_menu import MainMenu
        for evento in eventos:
            if self.btn_menu.manejar_eventos(evento):
                self.manager.modo_torneo = False
                self.manager.cambiar_escena(MainMenu(self.manager))

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(settings.COLOR_FONDO)
        
        txt_titulo = self.fuente_titulo.render("FIN DEL TORNEO", True, settings.TEXTO_COLOR)
        pantalla.blit(txt_titulo, (settings.ANCHO // 2 - txt_titulo.get_width() // 2, 120))
        
        # Render del anuncio del campeón
        txt_win = self.fuente_ganador.render(self.texto_ganador, True, self.color_ganador)
        pantalla.blit(txt_win, (settings.ANCHO // 2 - txt_win.get_width() // 2, 240))
        
        # Mostrar marcador de cierre
        fuente_puntos = pygame.font.SysFont("consolas", 24)
        txt_marcador = fuente_puntos.render(f"Marcador Final - J1: {self.manager.puntaje_j1} pts | J2: {self.manager.puntaje_j2} pts", True, settings.TEXTO_COLOR)
        pantalla.blit(txt_marcador, (settings.ANCHO // 2 - txt_marcador.get_width() // 2, 320))

        self.btn_menu.dibujar(pantalla)