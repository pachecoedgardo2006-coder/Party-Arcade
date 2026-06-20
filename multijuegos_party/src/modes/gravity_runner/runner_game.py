import pygame
import random
from config import settings
from src.scenes.base_scene import BaseScene
from .entities import Jugador, Obstaculo

class RunnerGame(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fuente_pequena = pygame.font.SysFont("consolas", 22)
        self.fuente_grande = pygame.font.SysFont("consolas", 48, bold=True)
        self.mejor_puntuacion = 0
        self.reiniciar_partida()

    def reiniciar_partida(self):
        self.jugador = Jugador()
        self.obstaculos = []
        self.temporizador_obstaculo = 0
        self.puntuacion = 0
        self.velocidad_juego = 7
        self.estado_interno = "JUGANDO" # JUGANDO, GAME_OVER

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if self.estado_interno == "JUGANDO" and evento.key == pygame.K_SPACE:
                    self.jugador.cambiar_gravedad()
                elif self.estado_interno == "GAME_OVER":
                    if evento.key == pygame.K_SPACE:
                        self.reiniciar_partida()
                    elif evento.key == pygame.K_m:
                        # IMPORTACIÓN LOCAL: Regresa al menú selector de juegos de forma limpia
                        from src.scenes.game_select import GameSelect
                        self.manager.cambiar_escena(GameSelect(self.manager))

    def actualizar(self):
        if self.estado_interno == "JUGANDO":
            self.jugador.actualizar()
            self.velocidad_juego += 0.002
            self.temporizador_obstaculo += 1
            
            frecuencia_minima = max(35, 90 - int(self.velocidad_juego * 2))
            if self.temporizador_obstaculo > random.randint(frecuencia_minima, frecuencia_minima + 35):
                self.obstaculos.append(Obstaculo(self.velocidad_juego))
                self.temporizador_obstaculo = 0

            rect_jugador = self.jugador.obtener_rect()
            for obs in self.obstaculos[:]:
                obs.actualizar()
                
                if rect_jugador.colliderect(obs.obtener_rect()):
                    self.estado_interno = "GAME_OVER"
                    if self.puntuacion > self.mejor_puntuacion:
                        self.mejor_puntuacion = self.puntuacion
                
                if obs.x + obs.ancho < 0:
                    self.obstaculos.remove(obs)
                    self.puntuacion += 1

    def dibujar_escenario(self, pantalla):
        pantalla.fill(settings.COLOR_FONDO)
        pygame.draw.rect(pantalla, settings.COLOR_PLATAFORMA, (0, 0, settings.ANCHO, settings.TECHO_Y))
        pygame.draw.rect(pantalla, settings.COLOR_PLATAFORMA, (0, settings.SUELO_Y, settings.ANCHO, settings.ALTURA_PLATAFORMA))
        pygame.draw.line(pantalla, settings.LINEA_NEON, (0, settings.TECHO_Y), (settings.ANCHO, settings.TECHO_Y), 3)
        pygame.draw.line(pantalla, settings.LINEA_NEON, (0, settings.SUELO_Y), (settings.ANCHO, settings.SUELO_Y), 3)



    def dibujar(self, pantalla):
        self.dibujar_escenario(pantalla)
        self.jugador.dibujar(pantalla)
        
        for obs in self.obstaculos:
            obs.dibujar(pantalla)

        if self.estado_interno == "JUGANDO":
            txt_puntos = self.fuente_pequena.render(f"PUNTOS: {self.puntuacion}", True, settings.TEXTO_COLOR)
            txt_record = self.fuente_pequena.render(f"RÉCORD: {self.mejor_puntuacion}", True, settings.LINEA_NEON)
            pantalla.blit(txt_puntos, (20, 15))
            pantalla.blit(txt_record, (settings.ANCHO - txt_record.get_width() - 20, 15))
            
        elif self.estado_interno == "GAME_OVER":
            texto_game_over = self.fuente_grande.render("¡GAME OVER!", True, settings.JUGADOR_COLOR)
            texto_score_final = self.fuente_pequena.render(f"Puntuación final: {self.puntuacion}", True, settings.TEXTO_COLOR)
            
            # --- MODIFICAMOS ESTA LÍNEA PARA AGREGAR LA INDICACIÓN VISUAL ---
            texto_reintentar = self.fuente_pequena.render(
                "Presiona [ESPACIO] para reintentar o [M] para Menú", True, settings.OBSTACULO_COLOR
            )
            
            # Ajuste de posición centrado en pantalla
            pantalla.blit(texto_game_over, (settings.ANCHO // 2 - texto_game_over.get_width() // 2, settings.ALTO // 2 - 80))
            pantalla.blit(texto_score_final, (settings.ANCHO // 2 - texto_score_final.get_width() // 2, settings.ALTO // 2 + 10))
            pantalla.blit(texto_reintentar, (settings.ANCHO // 2 - texto_reintentar.get_width() // 2, settings.ALTO // 2 + 50))