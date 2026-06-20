import pygame
import random
from config import settings

class Particula:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radio = random.randint(3, 6)
        self.vel_x = random.uniform(-4, -2)
        self.vel_y = random.uniform(-1, 1)
        self.vida = 255

    def actualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vida -= 8
        if self.radio > 0.2:
            self.radio -= 0.1

    def dibujar(self, superficie):
        if self.vida > 0 and self.radio > 0:
            pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), int(self.radio))


class Jugador:
    def __init__(self):
        self.ancho = 40
        self.alto = 40
        self.x = 120
        self.y = settings.SUELO_Y - self.alto
        self.vel_y = 0
        self.f_gravedad = 0.9
        self.direccion_gravedad = 1
        self.estela = []
        self.escala_x = 1.0
        self.escala_y = 1.0

    def cambiar_gravedad(self):
        self.direccion_gravedad *= -1
        self.escala_y = 1.4
        self.escala_x = 0.7

    def actualizar(self):
        self.vel_y += self.f_gravedad * self.direccion_gravedad
        self.y += self.vel_y

        # Colisiones adaptadas al entorno limpio de configuraciones
        if self.direccion_gravedad == 1:
            if self.y >= settings.SUELO_Y - self.alto:
                self.y = settings.SUELO_Y - self.alto
                self.vel_y = 0
        else:
            if self.y <= settings.TECHO_Y:
                self.y = settings.TECHO_Y
                self.vel_y = 0

        self.escala_x += (1.0 - self.escala_x) * 0.15
        self.escala_y += (1.0 - self.escala_y) * 0.15

        if random.random() > 0.2:
            centro_y = self.y + self.alto / 2
            self.estela.append(Particula(self.x, centro_y, settings.JUGADOR_COLOR))

        for p in self.estela[:]:
            p.actualizar()
            if p.vida <= 0 or p.radio <= 0:
                self.estela.remove(p)

    def dibujar(self, superficie):
        for p in self.estela:
            p.dibujar(superficie)

        ancho_final = int(self.ancho * self.escala_x)
        alto_final = int(self.alto * self.escala_y)
        diff_x = (ancho_final - self.ancho) // 2
        diff_y = (alto_final - self.alto) // 2
        rect_dibujo = pygame.Rect(self.x - diff_x, self.y - diff_y, ancho_final, alto_final)
        
        pygame.draw.rect(superficie, settings.JUGADOR_COLOR, rect_dibujo, border_radius=6)
        pygame.draw.rect(superficie, (255, 255, 255), rect_dibujo, 2, border_radius=6)

    def obtener_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)


class Obstaculo:
    def __init__(self, velocidad):
        self.ancho = random.randint(30, 50)
        self.alto = random.randint(50, 120)
        self.x = settings.ANCHO
        self.velocidad = velocidad
        self.tipo = random.choice([0, 1, 2])
        
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