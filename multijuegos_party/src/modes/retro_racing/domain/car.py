import pygame
import math
from .constants import *

class Car:
    def __init__(self, x, y, angulo_inicial, jugador_id):
        self.jugador_id = jugador_id
        self.ancho = 24
        self.alto = 14
        self.reiniciar(x, y, angulo_inicial)

    def reiniciar(self, x, y, angulo_inicial):
        self.x = x
        self.y = y
        self.velocidad = 0.0
        self.angulo = angulo_inicial  # En grados
        
        self.vuelta_actual = 1
        self.termino_carrera = False
        
        # BUG SHIELD: Lista de control de checkpoints secuenciales para evitar atajos
        # El auto debe marcar True en cada índice ordenadamente: [CP_Oeste, CP_Sur, CP_Este]
        self.checkpoints_visitados = [False, False, False]

    def acelerar(self, reversa=False, velocidad_limite=VEL_MAX_PISTA):
        limite = velocidad_limite if not reversa else -velocidad_limite / 2
        if not reversa:
            if self.velocidad < limite:
                self.velocidad += ACELERACION
        else:
            if self.velocidad > limite:
                self.velocidad -= ACELERACION

    def rotar(self, direccion):
        if abs(self.velocidad) > 0.2:
            multiplicador = 1 if self.velocidad > 0 else -1
            if direccion == "IZQUIERDA":
                self.angulo += VEL_ROTACION * multiplicador
            elif direccion == "DERECHA":
                self.angulo -= VEL_ROTACION * multiplicador

    def aplicar_friccion(self):
        if self.velocidad > 0:
            self.velocidad = max(0.0, self.velocidad - FRICCION)
        elif self.velocidad < 0:
            self.velocidad = min(0.0, self.velocidad + FRICCION)

    def actualizar_posicion(self):
        radianes = math.radians(self.angulo)
        self.x += self.velocidad * math.cos(radianes)
        self.y -= self.velocidad * math.sin(radianes)
        
        # BUG SHIELD: Evitar que los carros desaparezcan en los bordes extremos de la pantalla
        mitad_ancho = self.ancho // 2
        mitad_alto = self.alto // 2
        
        if self.x < mitad_ancho:
            self.x = mitad_ancho
            self.velocidad = 0
        elif self.x > ANCHO_PISTA - mitad_ancho:
            self.x = ANCHO_PISTA - mitad_ancho
            self.velocidad = 0
            
        if self.y < mitad_alto:
            self.y = mitad_alto
            self.velocidad = 0
        elif self.y > ALTO_PISTA - mitad_alto:
            self.y = ALTO_PISTA - mitad_alto
            self.velocidad = 0

    def obtener_rect(self):
        return pygame.Rect(self.x - self.ancho // 2, self.y - self.alto // 2, self.ancho, self.alto)