# src/modes/gravity_runner/core/particle_sys.py
import pygame
import random

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


class ParticleSystem:
    def __init__(self):
        self.particulas = []

    def emitir(self, x, y, color):
        if random.random() > 0.2:
            self.particulas.append(Particula(x, y, color))

    def actualizar(self):
        for p in self.particulas[:]:
            p.actualizar()
            if p.vida <= 0 or p.radio <= 0:
                self.particulas.remove(p)

    def dibujar(self, superficie):
        for p in self.particulas:
            p.dibujar(superficie)