# src/modes/sumo_combat/core/physics.py
import math
from src.modes.sumo_combat.domain.constants import CENTRO_ARENA, RADIO_ARENA

class SumoPhysics:
    @staticmethod
    def resolver_colision_sumos(s1, s2):
        """Calcula el impacto elástico masivo y separa los cuerpos inmediatamente."""
        dx = s2.x - s1.x
        dy = s2.y - s1.y
        distancia = math.hypot(dx, dy)
        distancia_minima = s1.radio + s2.radio

        if distancia < distancia_minima:
            # 1. SOLUCIÓN ANTIBUG: Separación física inmediata
            if distancia == 0:  
                overlap = distancia_minima
                nx, ny = 1.0, 0.0
            else:
                overlap = distancia_minima - distancia
                nx = dx / distancia
                ny = dy / distancia

            s1.x -= nx * (overlap * 0.5)
            s1.y -= ny * (overlap * 0.5)
            s2.x += nx * (overlap * 0.5)
            s2.y += ny * (overlap * 0.5)

            # 2. FÍSICA DE REBOTE EXPLOSIVO (Modificada)
            kx = s1.vx - s2.vx
            ky = s1.vy - s2.vy
            
            p_punto = kx * nx + ky * ny

            # Solo rebotar si se están moviendo uno hacia el otro
            if p_punto > 0:
                # 💥 MULTIPLICADOR DE IMPACTO 
                impulso = p_punto * 1.8 
                
                s1.vx -= impulso * nx
                s1.vy -= impulso * ny
                s2.vx += impulso * nx
                s2.vy += impulso * ny

    @staticmethod
    def verificar_fuera_arena(sumo):
        """Calcula si la distancia desde el centro de la arena supera el radio permitido."""
        dx = sumo.x - CENTRO_ARENA[0]
        dy = sumo.y - CENTRO_ARENA[1]
        distancia_centro = math.hypot(dx, dy)
        
        return distancia_centro > RADIO_ARENA