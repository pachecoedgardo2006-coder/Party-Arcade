# src/modes/retro_racing/core/physics.py
import pygame
import math

class RacingPhysics:
    @staticmethod
    def inicializar_pista_geometria(ancho, alto):
        """Define la pista y una red secuencial de 3 checkpoints distribuidos."""
        rect_exterior = pygame.Rect(40, 40, ancho - 80, alto - 80)
        rect_interior = pygame.Rect(180, 160, ancho - 360, alto - 320)
        
        # Línea de meta arriba (Norte)
        linea_meta = pygame.Rect(180, 40, 2, 120)
        
        # Red de Checkpoints Secuenciales en sentido antihorario
        checkpoints = [
            pygame.Rect(40, 160, 140, 2),   # CP 0: Recta Oeste (Izquierda)
            pygame.Rect(180, 440, 2, 120),  # CP 1: Recta Sur (Abajo)
            pygame.Rect(620, 160, 140, 2)    # CP 2: Recta Este (Derecha)
        ]
        
        return rect_exterior, rect_interior, linea_meta, checkpoints

    @staticmethod
    def determinar_velocidad_limite(carro, rect_ext, rect_int, vel_pista, vel_pasto):
        pos_centro = (int(carro.x), int(carro.y))
        en_anillo_exterior = rect_ext.collidepoint(pos_centro)
        en_isla_interior = rect_int.collidepoint(pos_centro)
        
        if en_anillo_exterior and not en_isla_interior:
            return vel_pista
        return vel_pasto

    @staticmethod
    def procesar_vueltas_y_checkpoints(carro, linea_meta, checkpoints):
        if carro.termino_carrera:
            return

        rect_carro = carro.obtener_rect()

        if rect_carro.colliderect(checkpoints[0]):
            carro.checkpoints_visitados[0] = True
        elif rect_carro.colliderect(checkpoints[1]):
            if carro.checkpoints_visitados[0]:
                carro.checkpoints_visitados[1] = True
        elif rect_carro.colliderect(checkpoints[2]):
            if carro.checkpoints_visitados[1]:
                carro.checkpoints_visitados[2] = True

        if rect_carro.colliderect(linea_meta):
            if all(carro.checkpoints_visitados):
                from ..domain.constants import MAX_VUELTAS
                if carro.vuelta_actual < MAX_VUELTAS:
                    carro.vuelta_actual += 1
                    carro.checkpoints_visitados = [False, False, False]
                else:
                    carro.termino_carrera = True
                    carro.velocidad = 0.0

    @staticmethod
    def verificar_colision_autos(p1, p2):
        """Verifica colisión física y calcula el rebote dinámico real según el ángulo de impacto."""
        rect_p1 = p1.obtener_rect()
        rect_p2 = p2.obtener_rect()

        if rect_p1.colliderect(rect_p2):
            # 1. Separación física inmediata para que no se queden pegados (Despegue radial)
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            distancia = (dx**2 + dy**2)**0.5
            if distancia == 0:
                distancia = 1.0
            
            # Vector normalizado del impacto (va de P1 hacia P2)
            nx = dx / distancia
            ny = dy / distancia
            
            fuerza_despegue = 4.0
            p1.x -= nx * fuerza_despegue
            p1.y -= ny * fuerza_despegue
            p2.x += nx * fuerza_despegue
            p2.y += ny * fuerza_despegue

            # 2. BUG SHIELD REBOTE: Determinar la dirección del golpe usando vectores directores
            # Vector de orientación del P1 (Hacia dónde apunta su frente)
            rad_p1 = math.radians(p1.angulo)
            hx1 = math.cos(rad_p1)
            hy1 = -math.sin(rad_p1) # Eje Y invertido en Pygame
            
            # Vector de orientación del P2
            rad_p2 = math.radians(p2.angulo)
            hx2 = math.cos(rad_p2)
            hy2 = -math.sin(rad_p2)

            # Producto punto para P1: Compara su frente con la posición de P2
            # Si es positivo, P2 está en su frente (P1 chocó de frente). Si es negativo, está detrás.
            dot_p1 = (hx1 * nx) + (hy1 * ny)
            
            # Producto punto para P2: El impacto le llega desde P1 (dirección -nx, -ny)
            dot_p2 = (hx2 * -nx) + (hy2 * -ny)

            # Guardamos las velocidades antes del impacto para la transferencia de energía
            v1_antigua = p1.velocidad
            v2_antigua = p2.velocidad

            # --- RESOLVER JUGADOR 1 ---
            if dot_p1 > 0:
                # Chocó de frente contra el compañero -> Rebota hacia atrás
                p1.velocidad = -abs(v1_antigua) * 0.4
            else:
                # Lo chocaron por detrás -> Recibe un impulso hacia adelante
                p1.velocidad = abs(v2_antigua) * 0.8 + 1.0

            # --- RESOLVER JUGADOR 2 ---
            if dot_p2 > 0:
                # Chocó de frente contra el compañero -> Rebota hacia atrás
                p2.velocidad = -abs(v2_antigua) * 0.4
            else:
                # Lo chocaron por detrás -> Recibe un impulso hacia adelante
                p2.velocidad = abs(v1_antigua) * 0.8 + 1.0