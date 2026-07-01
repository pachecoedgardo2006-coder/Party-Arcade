import pygame
import random
from config import settings
from .constants import (
    ANCHO_OBS_MIN, ANCHO_OBS_MAX, ALTO_OBS_MIN, ALTO_OBS_MAX,
    TIPO_SUELO, TIPO_TECHO, TIPO_AEREO
)

class Obstaculo:
    def __init__(self, velocidad):
        self.velocidad = velocidad
        self.x = settings.ANCHO
        self.tipo = random.choice([TIPO_SUELO, TIPO_TECHO, TIPO_AEREO])
        
        # Dimensiones dinámicas según tipo para balancear dificultad
        if self.tipo == TIPO_AEREO:
            self.ancho = random.randint(30, 45)
            self.alto = 50
            # Posición central con ligera variación controlada
            self.y = (settings.ALTO // 2) - (self.alto // 2) + random.randint(-30, 30)
        else:
            self.ancho = random.randint(ANCHO_OBS_MIN, ANCHO_OBS_MAX)
            self.alto = random.randint(ALTO_OBS_MIN, ALTO_OBS_MAX)
            
            if self.tipo == TIPO_SUELO:
                self.y = settings.SUELO_Y - self.alto
            elif self.tipo == TIPO_TECHO:
                self.y = settings.TECHO_Y

    def actualizar(self):
        self.x -= self.velocidad

    def dibujar(self, superficie):
        rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        pygame.draw.rect(superficie, settings.OBSTACULO_COLOR, rect, border_radius=4)
        pygame.draw.rect(superficie, (255, 255, 255), rect, 1, border_radius=4)

    def obtener_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)