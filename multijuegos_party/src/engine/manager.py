# src/engine/manager.py
import pygame
import sys
from config import settings

class GameManager:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((settings.ANCHO, settings.ALTO))
        pygame.display.set_caption("Party Arcade Hub")
        self.reloj = pygame.time.Clock()
        self.ejecutando = True
        self.escena_actual = None

        # --- NUEVAS VARIABLES PARA EL MODO TORNEO ---
        self.modo_torneo = False
        self.puntaje_j1 = 0
        self.puntaje_j2 = 0
        self.lista_juegos = []
        self.indice_juego_actual = 0

    def cambiar_escena(self, nueva_escena):
        """Cambia dinámicamente de pantalla (Polimorfismo puro)"""
        self.escena_actual = nueva_escena

    # --- NUEVOS MÉTODOS PARA EL TORNEO ---
    def iniciar_torneo(self):
        """Inicializa los valores del torneo y define la secuencia de juegos"""
        from src.modes.gravity_runner.runner_game import RunnerGame
        from src.modes.battle_snake.battle_snake import battleSnakeGame
        from src.modes.memory_grid.memory_game import MemoryGame
        from src.modes.sumo_combat.sumo_game import SumoGame
        from src.modes.retro_racing.racing_game import RacingGame

        self.modo_torneo = True
        self.puntaje_j1 = 0
        self.puntaje_j2 = 0
        self.indice_juego_actual = 0
        
        # Lista secuencial de las clases de tus minijuegos
        self.lista_juegos = [
            RunnerGame,
            battleSnakeGame,
            MemoryGame,
            SumoGame,
            RacingGame
        ]
        
        # Lanzar automáticamente el primer juego de la lista
        self.cargar_siguiente_juego()

    def cargar_siguiente_juego(self):
        """Revisa si quedan juegos pendientes o si ya terminó el torneo"""
        if self.indice_juego_actual < len(self.lista_juegos):
            # Instanciamos dinámicamente el juego pasándole este mismo manager (self)
            clase_juego = self.lista_juegos[self.indice_juego_actual]
            self.cambiar_escena(clase_juego(self))
        else:
            # Si se completaron todos los modos, pasamos a los resultados finales
            from src.scenes.final_results import FinalResults
            self.cambiar_escena(FinalResults(self))

    def registrar_victoria(self, jugador_ganador):
        """
        Suma un punto al marcador global y avanza el torneo.
        jugador_ganador: 1 para el Jugador 1, 2 para el Jugador 2.
        """
        if self.modo_torneo:
            if jugador_ganador == 1:
                self.puntaje_j1 += 1
            elif jugador_ganador == 2:
                self.puntaje_j2 += 1
            
            # Incrementamos el índice para apuntar al próximo minijuego
            self.indice_juego_actual += 1
            
            # Pasamos a la pantalla intermedia para mostrar cómo va el marcador
            from src.scenes.tournament_score import TournamentScore
            self.cambiar_escena(TournamentScore(self))
        
        else:
            # NUEVO: Si no es torneo, al terminar el juego volvemos directamente al selector de mapas
            from src.scenes.game_select import GameSelect
            self.cambiar_escena(GameSelect(self))

    def ejecutar(self):
        while self.ejecutando:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.ejecutando = False

            if self.escena_actual:
                self.escena_actual.manejar_eventos(eventos)
                self.escena_actual.actualizar()
                self.escena_actual.dibujar(self.pantalla)

            pygame.display.flip()
            self.reloj.tick(settings.FPS)

        pygame.quit()
        sys.exit()