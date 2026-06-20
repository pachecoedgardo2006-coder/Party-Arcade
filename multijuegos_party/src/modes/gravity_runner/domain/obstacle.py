# src/modes/gravity_runner/domain/obstacle.py
import pygame
import random
from config import settings

class Obstaculo:
    def __init__(self, velocidad):
        self.ancho = random.randint(30, 50)
        self.alto = random.randint(50, 120)
        self.x = settings.ANCHO
        self.velocidad = velocidad
        self.tipo = random.choice([0, 1, 2]) # 0: Suelo, 1: Techo, 2: Aéreo
        
        if self.tipo == 0:
            self.y = settings.SUELO_Y - self.alto
        elif self.tipo == 1:
            self.y = settings.TECHO_Y
        else:
            self.alto = 50
            self.y = (settings.ALTO // 2) - (self.alto // 2) + random.randint(-40, 40)

    def actualizar(self):
        self.x -= self.velocidad

    def dibujar(self, superficie):
        rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        pygame.draw.rect(superficie, settings.OBSTACULO_COLOR, rect, border_radius=4)
        pygame.draw.rect(superficie, (255, 255, 255), rect, 1, border_radius=4)

    def obtener_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)