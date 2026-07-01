# src/modes/memory_grid/memory_game.py
import pygame
from config import settings
from src.scenes.base_scene import BaseScene
from .domain.constants import *
from .core.logic import MemoryLogic

class MemoryGame(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fuente_pequena = pygame.font.SysFont("consolas", 20)
        self.fuente_mediana = pygame.font.SysFont("consolas", 24, bold=True)
        self.fuente_grande = pygame.font.SysFont("consolas", 44, bold=True)
        
        self.logic = MemoryLogic()
        self.calcular_y_centrar_grilla()
        self.reiniciar_partida()

    def calcular_y_centrar_grilla(self):
        """Calcula de forma dinámica los márgenes para centrar la grilla de 5x10 en la ventana."""
        ancho_total_grilla = (COLUMNAS * TARJETA_ANCHO) + ((COLUMNAS - 1) * MARGEN)
        alto_total_grilla = (FILAS * TARJETA_ALTO) + ((FILAS - 1) * MARGEN)
        
        # Margen de offset respecto a la ventana central (800x600)
        self.inicio_x = (settings.ANCHO - ancho_total_grilla) // 2
        self.inicio_y = ((settings.ALTO - alto_total_grilla) // 2) + 20  # Pequeño desfase para dejar espacio a la UI superior

    def reiniciar_partida(self):
        self.logic.reiniciar_logica()
        self.tablero = self.logic.generar_tablero(
            self.inicio_x, self.inicio_y, TARJETA_ANCHO, TARJETA_ALTO, MARGEN
        )
        
        # Configuraciones de flujos de tiempo iniciales
        self.estado_interno = ESTADO_MEMORIZAR
        self.tiempo_cambio_estado = pygame.time.get_ticks() + TIEMPO_MEMORIZAR
        
        # Forzar a que todas se vean bocarriba durante la fase de memorización inicial
        for card in self.tablero:
            card.volteada = True

    def manejar_eventos(self, eventos):
        from src.scenes.game_select import GameSelect

        for evento in eventos:
            if evento.type == pygame.QUIT:
                pass  # Gestionado centralmente por GameManager
                
            elif evento.type == pygame.KEYDOWN:
                if self.estado_interno == ESTADO_GAME_OVER:
                    if evento.key in (pygame.K_SPACE, pygame.K_r):
                        self.reiniciar_partida()
                    elif evento.key in (pygame.K_m, pygame.K_ESCAPE):
                        self.manager.cambiar_escena(GameSelect(self.manager))
                else:
                    if evento.key == pygame.K_ESCAPE:
                        self.manager.cambiar_escena(GameSelect(self.manager))

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1: # Clic izquierdo
                # BUG SHIELD: Si el juego está bloqueado por error o memorización, no procesar clics
                if self.estado_interno != ESTADO_JUGANDO:
                    continue
                    
                pos_mouse = pygame.mouse.get_pos()
                for card in self.tablero:
                    if card.obtener_rect(TARJETA_ANCHO, TARJETA_ALTO).collidepoint(pos_mouse):
                        resultado = self.logic.procesar_seleccion(card)
                        
                        if resultado is True:
                            # Hubo coincidencia exitosa. Comprobamos fin de partida instantáneamente
                            if self.logic.verificar_victoria(self.tablero):
                                self.estado_interno = ESTADO_GAME_OVER

                                if self.logic.puntuacion_p1 > self.logic.puntuacion_p2:
                                    self.manager.registrar_victoria(1)
                                elif self.logic.puntuacion_p2 > self.logic.puntuacion_p1:
                                    self.manager.registrar_victoria(2)
                                else:
                                    # En caso de empate técnico, decides si darlo al P1 o manejar un 0
                                    self.manager.registrar_victoria(0)

                        elif resultado is False:
                            # Error de coincidencia. Bloqueamos tablero y agendamos temporizador de ocultación
                            self.estado_interno = ESTADO_BLOQUEADO
                            self.tiempo_cambio_estado = pygame.time.get_ticks() + TIEMPO_ERROR_ESPERA
                        break

    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()

        # Control del temporizador de la fase inicial de memorización
        if self.estado_interno == ESTADO_MEMORIZAR:
            if tiempo_actual >= self.tiempo_cambio_estado:
                self.estado_interno = ESTADO_JUGANDO
                for card in self.tablero:
                    card.volteada = False
                    
        # Control del temporizador tras un error de emparejamiento
        elif self.estado_interno == ESTADO_BLOQUEADO:
            if tiempo_actual >= self.tiempo_cambio_estado:
                # Ocultamos el par incorrecto y limpiamos la selección lógica
                for card in self.logic.tarjetas_seleccionadas:
                    card.volteada = False
                self.logic.tarjetas_seleccionadas.clear()
                
                # Alternamos el turno y liberamos el tablero
                self.logic.cambiar_turno()
                self.estado_interno = ESTADO_JUGANDO

    def dibujar(self, superficie):
        superficie.fill(COLOR_FONDO_MG)
        
        # --- RENDERIZADO DE LA SECCIÓN DE RECUADROS (TABLERO) ---
        for card in self.tablero:
            rect_card = card.obtener_rect(TARJETA_ANCHO, TARJETA_ALTO)
            
            # 1. Definición cromática basada en estados atómicos
            if card.resuelta:
                color_actual = COLOR_TARJETA_PAREJA
            elif card.volteada:
                # Si estamos bloqueados por error, las tarjetas de la jugada fallida van en rojo
                if self.estado_interno == ESTADO_BLOQUEADO and card in self.logic.tarjetas_seleccionadas:
                    color_actual = COLOR_TARJETA_ERROR
                else:
                    color_actual = COLOR_TARJETA_VOLTEADA
            else:
                color_actual = COLOR_TARJETA_OCULTA

            # Dibujamos el cuerpo de la tarjeta
            pygame.draw.rect(superficie, color_actual, rect_card, border_radius=6)
            # Bordes estilizados neón
            pygame.draw.rect(superficie, (255, 255, 255), rect_card, width=1, border_radius=6)

            # 2. Render de los Identificadores Visuales (Simulando los iconos mediante ID de texto centrado)
            if card.volteada or card.resuelta:
                txt_id = self.fuente_mediana.render(str(card.icono_id), True, (255, 255, 255))
                centro_x = card.x + (TARJETA_ANCHO // 2) - (txt_id.get_width() // 2)
                centro_y = card.y + (TARJETA_ALTO // 2) - (txt_id.get_height() // 2)
                superficie.blit(txt_id, (centro_x, centro_y))

        # --- RENDERIZADO DE LA INTERFAZ DE USUARIO (UI) ---
        # Colores dinámicos para remarcar visualmente quién posee el turno actual de forma interactiva
        c_p1 = settings.LINEA_NEON if self.logic.turno_jugador == 1 else (100, 100, 100)
        c_p2 = settings.LINEA_NEON if self.logic.turno_jugador == 2 else (100, 100, 100)
        
        txt_p1 = self.fuente_pequena.render(f"P1 (Turno): {self.logic.puntuacion_p1}" if self.logic.turno_jugador == 1 else f"P1: {self.logic.puntuacion_p1}", True, c_p1)
        txt_p2 = self.fuente_pequena.render(f"P2 (Turno): {self.logic.puntuacion_p2}" if self.logic.turno_jugador == 2 else f"P2: {self.logic.puntuacion_p2}", True, c_p2)
        
        superficie.blit(txt_p1, (30, 20))
        superficie.blit(txt_p2, (settings.ANCHO - txt_p2.get_width() - 30, 20))

        # Indicador de fases superiores
        if self.estado_interno == ESTADO_MEMORIZAR:
            tiempo_restante = max(0, (self.tiempo_cambio_estado - pygame.time.get_ticks()) // 1000 + 1)
            txt_fase = self.fuente_mediana.render(f"¡MEMORIZA LOS ICONOS! {tiempo_restante}s", True, COLOR_TARJETA_VOLTEADA)
            superficie.blit(txt_fase, (settings.ANCHO // 2 - txt_fase.get_width() // 2, 20))
            
        elif self.estado_interno == ESTADO_JUGANDO or self.estado_interno == ESTADO_BLOQUEADO:
            txt_fase = self.fuente_mediana.render(f"Turno de: Jugador {self.logic.turno_jugador}", True, settings.TEXTO_COLOR)
            superficie.blit(txt_fase, (settings.ANCHO // 2 - txt_fase.get_width() // 2, 20))

        # Pantalla final de Game Over / Resultados
        elif self.estado_interno == ESTADO_GAME_OVER:
            # Dibujar un overlay semitransparente para dar el efecto de desenfoque/atenuado oscuro
            overlay = pygame.Surface((settings.ANCHO, settings.ALTO))
            overlay.set_alpha(220)
            overlay.fill((10, 10, 15))
            superficie.blit(overlay, (0, 0))

            # Determinar el string ganador
            if self.logic.puntuacion_p1 > self.logic.puntuacion_p2:
                ganador_str = "¡VICTORIA PARA EL JUGADOR 1!"
            elif self.logic.puntuacion_p2 > self.logic.puntuacion_p1:
                ganador_str = "¡VICTORIA PARA EL JUGADOR 2!"
            else:
                ganador_str = "¡EMPATE ABSOLUTO!"

            texto_ganador = self.fuente_grande.render(ganador_str, True, COLOR_TARJETA_PAREJA)
            texto_resumen = self.fuente_pequena.render(f"Marcador - P1: {self.logic.puntuacion_p1} | P2: {self.logic.puntuacion_p2}", True, (255, 255, 255))
            texto_reintentar = self.fuente_pequena.render("Presiona [R / ESPACIO] para revancha o [ESC / M] para salir", True, (180, 180, 180))

            superficie.blit(texto_ganador, (settings.ANCHO // 2 - texto_ganador.get_width() // 2, settings.ALTO // 2 - 60))
            superficie.blit(texto_resumen, (settings.ANCHO // 2 - texto_resumen.get_width() // 2, settings.ALTO // 2 + 15))
            superficie.blit(texto_reintentar, (settings.ANCHO // 2 - texto_reintentar.get_width() // 2, settings.ALTO // 2 + 65))