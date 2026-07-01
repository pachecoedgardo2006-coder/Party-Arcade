# src/modes/gravity_runner/core/physics.py
from config import settings
import pygame

class PhysicsEngine:
    @staticmethod
    def aplicar_gravedad(entidad, plataformas=[]):
        # 1. Aplicar aceleración
        entidad.vel_y += entidad.f_gravedad * entidad.direccion_gravedad
        
        # 2. Predicción de posición vertical
        siguiente_y = entidad.y + entidad.vel_y
        entidad.en_suelo = False

        # Creamos un rect ficticio de la posición a la que quiere ir el jugador
        rect_futuro = pygame.Rect(entidad.x, siguiente_y, entidad.ancho, entidad.alto)

        # 3. Evaluar colisiones con los límites globales del mapa (Suelo y Techo base)
        if entidad.direccion_gravedad == 1:  # Gravedad hacia abajo
            limite_inferior = settings.SUELO_Y - entidad.alto
            if siguiente_y >= limite_inferior:
                entidad.y = limite_inferior
                entidad.vel_y = 0
                entidad.en_suelo = True
                return
        else:  # Gravedad hacia arriba
            limite_superior = settings.TECHO_Y
            if siguiente_y <= limite_superior:
                entidad.y = limite_superior
                entidad.vel_y = 0
                entidad.en_suelo = True
                return

        # 4. Evaluar colisiones con plataformas intermedias
        # Nota: Solo colisionamos si caemos/subimos hacia la superficie de la plataforma
        for plat in plataformas:
            rect_plat = plat.obtener_rect()
            if rect_futuro.colliderect(rect_plat):
                # Si cae hacia abajo y sus pies estaban por encima de la plataforma
                if entidad.direccion_gravedad == 1 and entidad.vel_y >= 0 and (entidad.y + entidad.alto) <= rect_plat.top + 10:
                    entidad.y = rect_plat.top - entidad.alto
                    entidad.vel_y = 0
                    entidad.en_suelo = True
                    return
                # Si sube hacia arriba (gravedad invertida) y su cabeza estaba por debajo de la plataforma
                elif entidad.direccion_gravedad == -1 and entidad.vel_y <= 0 and entidad.y >= rect_plat.bottom - 10:
                    entidad.y = rect_plat.bottom
                    entidad.vel_y = 0
                    entidad.en_suelo = True
                    return

        # Si no colisionó con nada, se aplica el movimiento libre
        entidad.y = siguiente_y