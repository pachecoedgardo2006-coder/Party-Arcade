# src/modes/sumo_combat/domain/wrestler.py
import math
import pygame
from .constants import SUMO_RADIO, SUMO_FUERZA, SUMO_FRICCION, CONTROLES

class Wrestler:
    def __init__(self, x, y, jugador_id):
        self.jugador_id = jugador_id
        self.radio = SUMO_RADIO
        self.inicial_x = x
        self.inicial_y = y
        self.reiniciar_posicion()

    def reiniciar_posicion(self):
        self.x = self.inicial_x
        self.y = self.inicial_y
        self.vx = 0.0
        self.vy = 0.0

    def manejar_entrada(self, teclas):
        # Obtener mapeo de controles específicos del jugador
        control = CONTROLES[self.jugador_id]
        
        ax = 0.0
        ay = 0.0

        if teclas[control["ARRIBA"]]:    ay -= SUMO_FUERZA
        if teclas[control["ABAJO"]]:     ay += SUMO_FUERZA
        if teclas[control["IZQUIERDA"]]: ax -= SUMO_FUERZA
        if teclas[control["DERECHA"]]:   ax += SUMO_FUERZA

        # Normalizar vector de aceleración para evitar diagonal veloz
        if ax != 0 and ay != 0:
            ax *= 0.7071
            ay *= 0.7071

        self.vx += ax
        self.vy += ay

    def actualizar(self):
        # Aplicar velocidad a la posición
        self.x += self.vx
        self.y += self.vy

        # Aplicar fricción para control dinámico estable
        self.vx *= SUMO_FRICCION
        self.vy *= SUMO_FRICCION