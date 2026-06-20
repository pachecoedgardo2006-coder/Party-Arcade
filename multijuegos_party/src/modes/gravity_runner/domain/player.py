# src/modes/gravity_runner/domain/player.py
import pygame
from config import settings
from ..core.physics import PhysicsEngine
from ..core.particle_sys import ParticleSystem

class Jugador:
    def __init__(self):
        self.ancho = 40
        self.alto = 40
        self.x = 120
        self.y = settings.SUELO_Y - self.alto
        self.vel_y = 0
        self.f_gravedad = 0.9
        self.direccion_gravedad = 1
        self.en_suelo = True
        
        # Animación de deformación (Squash and Stretch)
        self.escala_x = 1.0
        self.escala_y = 1.0
        self.sistema_particulas = ParticleSystem()

    def cambiar_gravedad(self):
        self.direccion_gravedad *= -1
        self.vel_y = 0  # Resetea la velocidad para evitar que la inercia vieja lo arrastre
        self.escala_y = 1.4
        self.escala_x = 0.7
        self.en_suelo = False

    def actualizar(self):
        # Delegamos la física al motor especializado
        PhysicsEngine.aplicar_gravedad(self)

        # Suavizado de la animación de deformación
        self.escala_x += (1.0 - self.escala_x) * 0.15
        self.escala_y += (1.0 - self.escala_y) * 0.15

        # Emitir estela desde el centro posterior del cubo
        centro_y = self.y + self.alto / 2
        self.sistema_particulas.emitir(self.x, centro_y, settings.JUGADOR_COLOR)
        self.sistema_particulas.actualizar()

    def dibujar(self, superficie):
        self.sistema_particulas.dibujar(superficie)

        # Renderizado con transformaciones de escala
        ancho_final = int(self.ancho * self.escala_x)
        alto_final = int(self.alto * self.escala_y)
        diff_x = (ancho_final - self.ancho) // 2
        diff_y = (alto_final - self.alto) // 2
        rect_dibujo = pygame.Rect(self.x - diff_x, self.y - diff_y, ancho_final, alto_final)
        
        pygame.draw.rect(superficie, settings.JUGADOR_COLOR, rect_dibujo, border_radius=6)
        pygame.draw.rect(superficie, (255, 255, 255), rect_dibujo, 2, border_radius=6)

    def obtener_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)