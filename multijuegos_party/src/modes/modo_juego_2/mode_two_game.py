import pygame
from config import settings
from src.modes.modo_juego_2.domain.snake import Snake
from src.modes.modo_juego_2.domain.food import Food
from src.modes.modo_juego_2.domain.constants import *
from src.modes.modo_juego_2.core.logic import SnakeLogic

class ModeTwoGame:
    def __init__(self, manager):
        self.manager = manager
        self.fuente_pequena = pygame.font.SysFont("consolas", 22)
        self.fuente_grande = pygame.font.SysFont("consolas", 48, bold=True)
        
        # Inicializamos las dos serpientes en posiciones distintas
        self.snakes = [
            Snake(ANCHO_GRID // 4, ALTO_GRID // 2, jugador_id=1),
            Snake((ANCHO_GRID // 4) * 3, ALTO_GRID // 2, jugador_id=2)
        ]
        self.food = Food()
        self.reiniciar_partida()

    def reiniciar_partida(self):
        # Reiniciamos ambas serpientes
        self.snakes[0].reiniciar(ANCHO_GRID // 4, ALTO_GRID // 2)
        self.snakes[1].reiniciar((ANCHO_GRID // 4) * 3, ALTO_GRID // 2)
        
        # Combinamos los cuerpos para que la comida no aparezca encima de ninguna
        cuerpos_totales = self.snakes[0].cuerpo + self.snakes[1].cuerpo
        self.food.reubicar(cuerpos_totales)
        
        self.puntuacion_p1 = 0
        self.puntuacion_p2 = 0
        self.tiempo_ultimo_paso = pygame.time.get_ticks()
        self.velocidad_ms = 120
        self.estado_interno = "JUGANDO"

    def manejar_eventos(self, eventos):
        from src.scenes.game_select import GameSelect

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if self.estado_interno == "JUGANDO":
                    # --- CONTROLES JUGADOR 1 (WASD) ---
                    if evento.key == pygame.K_w:
                        self.snakes[0].cambiar_direccion(DIR_ARRIBA)
                    elif evento.key == pygame.K_s:
                        self.snakes[0].cambiar_direccion(DIR_ABAJO)
                    elif evento.key == pygame.K_a:
                        self.snakes[0].cambiar_direccion(DIR_IZQUIERDA)
                    elif evento.key == pygame.K_d:
                        self.snakes[0].cambiar_direccion(DIR_DERECHA)
                    
                    # --- CONTROLES JUGADOR 2 (FLECHAS) ---
                    elif evento.key == pygame.K_UP:
                        self.snakes[1].cambiar_direccion(DIR_ARRIBA)
                    elif evento.key == pygame.K_DOWN:
                        self.snakes[1].cambiar_direccion(DIR_ABAJO)
                    elif evento.key == pygame.K_LEFT:
                        self.snakes[1].cambiar_direccion(DIR_IZQUIERDA)
                    elif evento.key == pygame.K_RIGHT:
                        self.snakes[1].cambiar_direccion(DIR_DERECHA)
                
                # --- CONTROL GLOBAL EN GAME OVER ---
                elif self.estado_interno == "GAME_OVER":
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_r:
                        self.reiniciar_partida()
                    elif evento.key == pygame.K_m or evento.key == pygame.K_ESCAPE:
                        self.manager.cambiar_escena(GameSelect(self.manager))

    def actualizar(self):
        if self.estado_interno != "JUGANDO":
            return

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_paso > self.velocidad_ms:
            self.tiempo_ultimo_paso = tiempo_actual

            # 1. Procesar alimentación de forma independiente
            for snake in self.snakes:
                se_comio_la_comida = SnakeLogic.verificar_comida(snake, self.food)
                snake.avanzar(crecer=se_comio_la_comida)
                
                if se_comio_la_comida:
                    if snake.jugador_id == 1:
                        self.puntuacion_p1 += 1
                    else:
                        self.puntuacion_p2 += 1
                    
                    cuerpos_totales = self.snakes[0].cuerpo + self.snakes[1].cuerpo
                    self.food.reubicar(cuerpos_totales)

            # 2. Verificar si alguna colisionó y murió
            for snake in self.snakes:
                if SnakeLogic.verificar_colisiones(snake, self.snakes):
                    snake.viva = False
                    self.estado_interno = "GAME_OVER"

    def dibujar(self, superficie):
        superficie.fill(COLOR_FONDO)

        # Dibujar comida
        food_rect = pygame.Rect(
            self.food.posicion[0] * TAMANIO_CUADRO,
            self.food.posicion[1] * TAMANIO_CUADRO,
            TAMANIO_CUADRO - 1,
            TAMANIO_CUADRO - 1
        )
        pygame.draw.rect(superficie, COLOR_COMIDA, food_rect)

        # Dibujar ambas serpientes iterando la lista
        for snake in self.snakes:
            color = COLOR_SNAKE_1 if snake.jugador_id == 1 else COLOR_SNAKE_2
            for parte in snake.cuerpo:
                snake_rect = pygame.Rect(
                    parte[0] * TAMANIO_CUADRO,
                    parte[1] * TAMANIO_CUADRO,
                    TAMANIO_CUADRO - 1,
                    TAMANIO_CUADRO - 1
                )
                pygame.draw.rect(superficie, color, snake_rect)

        # UI en juego
        if self.estado_interno == "JUGANDO":
            txt_p1 = self.fuente_pequena.render(f"P1 (VERDE): {self.puntuacion_p1}", True, COLOR_SNAKE_1)
            txt_p2 = self.fuente_pequena.render(f"P2 (AZUL): {self.puntuacion_p2}", True, COLOR_SNAKE_2)
            superficie.blit(txt_p1, (20, 15))
            superficie.blit(txt_p2, (settings.ANCHO - txt_p2.get_width() - 20, 15))
            
        elif self.estado_interno == "GAME_OVER":
            texto_game_over = self.fuente_grande.render("¡FIN DE LA PARTIDA!", True, (255, 0, 0))
            texto_resumen = self.fuente_pequena.render(f"Marcador - P1: {self.puntuacion_p1} | P2: {self.puntuacion_p2}", True, (255, 255, 255))
            texto_reintentar = self.fuente_pequena.render("Presiona [R/ESPACIO] para revancha o [ESC/M] para Menú", True, (200, 200, 200))
            
            superficie.blit(texto_game_over, (settings.ANCHO // 2 - texto_game_over.get_width() // 2, settings.ALTO // 2 - 80))
            superficie.blit(texto_resumen, (settings.ANCHO // 2 - texto_resumen.get_width() // 2, settings.ALTO // 2 + 10))
            superficie.blit(texto_reintentar, (settings.ANCHO // 2 - texto_reintentar.get_width() // 2, settings.ALTO // 2 + 50))