# src/scenes/main_menu.py
import pygame
import sys
from config import settings
from src.scenes.base_scene import BaseScene
from src.ui.components import Boton

class MainMenu(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fuente_titulo = pygame.font.SysFont("consolas", 52, bold=True)
        self.fuente_subtitulo = pygame.font.SysFont("consolas", 20)
        
        # Botón para iniciar el torneo secuencial
        self.btn_torneo = Boton(
            settings.ANCHO // 2 - 150, settings.ALTO // 2 - 50, 300, 50,
            "INICIAR TORNEO", settings.COLOR_PLATAFORMA, settings.LINEA_NEON, settings.TEXTO_COLOR
        )
        
        # NUEVO: Botón para elegir un minijuego individual
        self.btn_seleccion = Boton(
            settings.ANCHO // 2 - 150, settings.ALTO // 2 + 20, 300, 50,
            "MODO LIBRE", settings.COLOR_PLATAFORMA, settings.LINEA_NEON, settings.TEXTO_COLOR
        )
        
        self.btn_salir = Boton(
            settings.ANCHO // 2 - 150, settings.ALTO // 2 + 90, 300, 50,
            "SALIR DEL HUB", settings.COLOR_PLATAFORMA, settings.JUGADOR_COLOR, settings.TEXTO_COLOR
        )

    def manejar_eventos(self, eventos):
        from src.scenes.game_select import GameSelect # Importación local preventiva
        
        for evento in eventos:
            if self.btn_torneo.manejar_eventos(evento):
                self.manager.iniciar_torneo()
                
            if self.btn_seleccion.manejar_eventos(evento):
                # Desactivamos explícitamente el modo torneo en el manager y vamos a la selección
                self.manager.modo_torneo = False
                self.manager.cambiar_escena(GameSelect(self.manager))
                
            if self.btn_salir.manejar_eventos(evento):
                pygame.quit()
                sys.exit()

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(settings.COLOR_FONDO)
        
        txt_titulo = self.fuente_titulo.render("PARTY ARCADE HUB", True, settings.LINEA_NEON)
        txt_sub = self.fuente_subtitulo.render("Compendio de Videojuegos Multijugador", True, settings.TEXTO_COLOR)
        
        pantalla.blit(txt_titulo, (settings.ANCHO // 2 - txt_titulo.get_width() // 2, settings.ALTO // 2 - 140))
        pantalla.blit(txt_sub, (settings.ANCHO // 2 - txt_sub.get_width() // 2, settings.ALTO // 2 - 80))
        
        self.btn_torneo.dibujar(pantalla)
        self.btn_seleccion.dibujar(pantalla) # Dibujar el nuevo botón
        self.btn_salir.dibujar(pantalla)