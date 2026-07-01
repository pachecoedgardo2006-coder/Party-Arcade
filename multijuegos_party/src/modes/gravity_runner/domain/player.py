# src/modes/gravity_runner/domain/player.py
import pygame
from config import settings
from ..core.physics import PhysicsEngine
from ..core.particle_sys import ParticleSystem
from .constants import ANCHO_JUGADOR, ALTO_JUGADOR

class Jugador:
    def __init__(self, id_jugador, x_inicial, color, tecla_salto):
        self.id = id_jugador
        self.ancho = ANCHO_JUGADOR
        self.alto = ALTO_JUGADOR
        self.x = x_inicial
        self.y = settings.SUELO_Y - self.alto
        self.vel_y = 0
        self.f_gravedad = 0.9
        self.direccion_gravedad = 1
        self.en_suelo = True
        self.tecla_salto = tecla_salto
        self.color = color
        self.vivo = True
        
        # Animación de deformación (Squash and Stretch)
        self.escala_x = 1.0
        self.escala_y = 1.0
        self.sistema_particulas = ParticleSystem()

    def cambiar_gravedad(self):
        if not self.vivo:
            return
        self.direccion_gravedad *= -1
        self.vel_y = 0  
        self.escala_y = 1.4
        self.escala_x = 0.7
        self.en_suelo = False

    # Ahora acepta las plataformas del mapa
    def actualizar(self, plataformas=[]):
        if not self.vivo:
            return
            
        # Le pasamos las plataformas al motor de física modificado
        PhysicsEngine.aplicar_gravedad(self, plataformas)

        # Suavizado Squash and Stretch
        self.escala_x += (1.0 - self.escala_x) * 0.15
        self.escala_y += (1.0 - self.escala_y) * 0.15

        # Estela desde el centro posterior
        centro_y = self.y + self.alto / 2
        self.sistema_particulas.emitir(self.x, centro_y, self.color)
        self.sistema_particulas.actualizar()

    def dibujar(self, superficie):
        # Dibujar partículas incluso si muere (efecto residual elegante)
        self.sistema_particulas.dibujar(superficie)

        if not self.vivo:
            return

        # Renderizado con transformaciones de escala
        ancho_final = int(self.ancho * self.escala_x)
        alto_final = int(self.alto * self.escala_y)
        diff_x = (ancho_final - self.ancho) // 2
        diff_y = (alto_final - self.alto) // 2
        rect_dibujo = pygame.Rect(self.x - diff_x, self.y - diff_y, ancho_final, alto_final)
        
        pygame.draw.rect(superficie, self.color, rect_dibujo, border_radius=6)
        pygame.draw.rect(superficie, (255, 255, 255), rect_dibujo, 2, border_radius=6)

    def obtener_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)