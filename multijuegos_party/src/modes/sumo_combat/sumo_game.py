# src/modes/sumo_combat/sumo_game.py
import pygame
from config import settings
from src.scenes.base_scene import BaseScene
from .domain.constants import *
from .domain.wrestler import Wrestler
from .core.physics import SumoPhysics

class SumoGame(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fuente_pequena = pygame.font.SysFont("consolas", 22)
        self.fuente_grande = pygame.font.SysFont("consolas", 48, bold=True)
        
        # Instanciar luchadores en extremos opuestos de la arena circular
        self.player1 = Wrestler(CENTRO_ARENA[0] - 130, CENTRO_ARENA[1], jugador_id=1)
        self.player2 = Wrestler(CENTRO_ARENA[0] + 130, CENTRO_ARENA[1], jugador_id=2)
        
        self.puntuacion_p1 = 0
        self.puntuacion_p2 = 0
        self.reiniciar_partida()

    def reiniciar_partida(self):
        self.puntuacion_p1 = 0
        self.puntuacion_p2 = 0
        self.estado_interno = "JUGANDO"
        self.reiniciar_ronda()

    def reiniciar_ronda(self):
        self.player1.reiniciar_posicion()
        self.player2.reiniciar_posicion()
        self.temporizador_ronda = 0
        # Dar un pequeño respiro congelado antes de empezar a mover (1.5 segundos)
        self.tiempo_espera_inicio = pygame.time.get_ticks() + 1500 

    def manejar_eventos(self, eventos):
        from src.scenes.game_select import GameSelect

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if self.estado_interno == "GAME_OVER":
                    if evento.key in (pygame.K_SPACE, pygame.K_r):
                        self.reiniciar_partida()
                    elif evento.key in (pygame.K_m, pygame.K_ESCAPE):
                        self.manager.cambiar_escena(GameSelect(self.manager))
                else:
                    if evento.key == pygame.K_ESCAPE:
                        self.manager.cambiar_escena(GameSelect(self.manager))

    def actualizar(self):
        if self.estado_interno == "GAME_OVER":
            return

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual < self.tiempo_espera_inicio:
            return  # Pausa de preparación activa

        # 1. Capturar entradas de teclado de ambos jugadores de forma simultánea
        teclas = pygame.key.get_pressed()
        self.player1.manejar_entrada(teclas)
        self.player2.manejar_entrada(teclas)

        # 2. Actualizar posiciones físicas individuales
        self.player1.actualizar()
        self.player2.actualizar()

        # 3. Resolver colisión e interpenetración mutua
        SumoPhysics.resolver_colision_sumos(self.player1, self.player2)

        # 4. Validar caídas fuera de la arena (Bug Shield de doble muerte por prioridad secuencial)
        p1_fuera = SumoPhysics.verificar_fuera_arena(self.player1)
        p2_fuera = SumoPhysics.verificar_fuera_arena(self.player2)

        if p1_fuera or p2_fuera:
            if p1_fuera and not p2_fuera:
                self.puntuacion_p2 += 1
            elif p2_fuera and not p1_fuera:
                self.puntuacion_p1 += 1
            else:
                # Si ambos salen exactamente el mismo frame, nadie puntúa (Empate de ronda)
                pass

            # Validar condiciones de fin de juego completas
            if self.puntuacion_p1 >= PUNTOS_VICTORIA or self.puntuacion_p2 >= PUNTOS_VICTORIA:
                self.estado_interno = "GAME_OVER"

                if self.puntuacion_p1 > self.puntuacion_p2:
                    self.manager.registrar_victoria(1)
                else:
                    self.manager.registrar_victoria(2)
                    
            else:
                self.reiniciar_ronda()

    def dibujar(self, superficie):
        # Fondo plano minimalista
        superficie.fill(COLOR_FONDO_SC)

        # --- DIBUJAR ARENA (Vista Cenital Estructurada) ---
        # Sombra/Relleno central de la plataforma
        pygame.draw.circle(superficie, COLOR_ARENA, CENTRO_ARENA, RADIO_ARENA)
        # Línea perimetral de advertencia Neón
        pygame.draw.circle(superficie, COLOR_BORDE_ARENA, CENTRO_ARENA, RADIO_ARENA, width=4)

        # --- DIBUJAR LUCHADORES ---
        # Jugador 1
        pygame.draw.circle(superficie, COLOR_SUMO_1, (int(self.player1.x), int(self.player1.y)), self.player1.radio)
        pygame.draw.circle(superficie, (255, 255, 255), (int(self.player1.x), int(self.player1.y)), self.player1.radio, width=1)
        
        # Jugador 2
        pygame.draw.circle(superficie, COLOR_SUMO_2, (int(self.player2.x), int(self.player2.y)), self.player2.radio)
        pygame.draw.circle(superficie, (255, 255, 255), (int(self.player2.x), int(self.player2.y)), self.player2.radio, width=1)

        # --- INTERFAZ GRÁFICA (UI) ---
        # Marcador persistente en pantalla[cite: 2]
        txt_p1 = self.fuente_pequena.render(f"P1 (WASD): {self.puntuacion_p1} / {PUNTOS_VICTORIA}", True, COLOR_SUMO_1)
        txt_p2 = self.fuente_pequena.render(f"P2 (FLECHAS): {self.puntuacion_p2} / {PUNTOS_VICTORIA}", True, COLOR_SUMO_2)
        superficie.blit(txt_p1, (40, 20))
        superficie.blit(txt_p2, (settings.ANCHO - txt_p2.get_width() - 40, 20))

        # Texto intermitente de preparación de ronda
        tiempo_actual = pygame.time.get_ticks()
        if self.estado_interno == "JUGANDO" and tiempo_actual < self.tiempo_espera_inicio:
            txt_ready = self.fuente_grande.render("¡PREPARADOS!", True, (255, 255, 255))
            superficie.blit(txt_ready, (settings.ANCHO // 2 - txt_ready.get_width() // 2, settings.ALTO // 2 - 30))

        # Pantalla final de fin de partida
        elif self.estado_interno == "GAME_OVER":
            # Capa de oscurecimiento interactivo[cite: 4]
            overlay = pygame.Surface((settings.ANCHO, settings.ALTO))
            overlay.set_alpha(200)
            overlay.fill((10, 10, 15))
            superficie.blit(overlay, (0, 0))
            ganador = "JUGADOR 1" if self.puntuacion_p1 > self.puntuacion_p2 else "JUGADOR 2"
            color_ganador = COLOR_SUMO_1 if ganador == "JUGADOR 1" else COLOR_SUMO_2

            texto_game_over = self.fuente_grande.render(f"¡VICTORIA DE {ganador}!", True, color_ganador)
            texto_reintentar = self.fuente_pequena.render("Presiona [R / ESPACIO] para revancha o [ESC] para salir", True, (200, 200, 200))
            
            superficie.blit(texto_game_over, (settings.ANCHO // 2 - texto_game_over.get_width() // 2, settings.ALTO // 2 - 40))
            superficie.blit(texto_reintentar, (settings.ANCHO // 2 - texto_reintentar.get_width() // 2, settings.ALTO // 2 + 30))