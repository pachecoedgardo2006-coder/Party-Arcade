import pygame
import sys
from config import settings

class GameManager:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((settings.ANCHO, settings.ALTO))
        pygame.display.set_caption("Party Arcade Hub")
        self.reloj = pygame.time.Clock()
        self.ejecutando = True
        self.escena_actual = None

    def cambiar_escena(self, nueva_escena):
        """Cambia dinámicamente de pantalla (Polimorfismo puro)"""
        self.escena_actual = nueva_escena

    def ejecutar(self):
        while self.ejecutando:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.ejecutando = False

            if self.escena_actual:
                self.escena_actual.manejar_eventos(eventos)
                self.escena_actual.actualizar()
                self.escena_actual.dibujar(self.pantalla)

            pygame.display.flip()
            self.reloj.tick(settings.FPS)

        pygame.quit()
        sys.exit()