import pygame
import sys
from config import settings
from src.scenes.base_scene import BaseScene
from src.ui.components import Boton
from src.scenes.game_select import GameSelect

class MainMenu(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fuente_titulo = pygame.font.SysFont("consolas", 52, bold=True)
        self.fuente_subtitulo = pygame.font.SysFont("consolas", 20)
        
        # Posicionamiento de botones en el centro de la pantalla
        self.btn_jugar = Boton(
            settings.ANCHO // 2 - 150, settings.ALTO // 2 - 20, 300, 50,
            "SELECCIONAR JUEGO", settings.COLOR_PLATAFORMA, settings.LINEA_NEON, settings.TEXTO_COLOR
        )
        self.btn_salir = Boton(
            settings.ANCHO // 2 - 150, settings.ALTO // 2 + 50, 300, 50,
            "SALIR DEL HUB", settings.COLOR_PLATAFORMA, settings.JUGADOR_COLOR, settings.TEXTO_COLOR
        )

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if self.btn_jugar.manejar_eventos(evento):
                # Cambia polimórficamente a la pantalla de selección
                self.manager.cambiar_escena(GameSelect(self.manager))
                
            if self.btn_salir.manejar_eventos(evento):
                pygame.quit()
                sys.exit()

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(settings.COLOR_FONDO)
        
        # Textos de la interfaz
        txt_titulo = self.fuente_titulo.render("PARTY ARCADE HUB", True, settings.LINEA_NEON)
        txt_sub = self.fuente_subtitulo.render("Compendio de Videojuegos Multijugador", True, settings.TEXTO_COLOR)
        
        pantalla.blit(txt_titulo, (settings.ANCHO // 2 - txt_titulo.get_width() // 2, settings.ALTO // 2 - 140))
        pantalla.blit(txt_sub, (settings.ANCHO // 2 - txt_sub.get_width() // 2, settings.ALTO // 2 - 80))
        
        # Dibujar botones compartidos
        self.btn_jugar.dibujar(pantalla)
        self.btn_salir.dibujar(pantalla)