# src/scenes/tournament_score.py
import pygame
from config import settings
from src.scenes.base_scene import BaseScene
from src.ui.components import Boton

class TournamentScore(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fuente_titulo = pygame.font.SysFont("consolas", 40, bold=True)
        self.fuente_marcador = pygame.font.SysFont("consolas", 30)
        
        self.btn_siguiente = Boton(
            settings.ANCHO // 2 - 150, settings.ALTO - 150, 300, 50,
            "SIGUIENTE JUEGO", settings.COLOR_PLATAFORMA, settings.LINEA_NEON, settings.TEXTO_COLOR
        )

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if self.btn_siguiente.manejar_eventos(evento):
                # Le pide al manager que cargue el siguiente índice en la lista
                self.manager.cargar_siguiente_juego()

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(settings.COLOR_FONDO)
        
        txt_titulo = self.fuente_titulo.render("PUNTAJE DEL TORNEO", True, settings.LINEA_NEON)
        pantalla.blit(txt_titulo, (settings.ANCHO // 2 - txt_titulo.get_width() // 2, 100))
        
        # Mostramos los contadores globales que persisten en el manager
        txt_j1 = self.fuente_marcador.render(f"RIVAL 1 (J1): {self.manager.puntaje_j1} Pts", True, settings.TEXTO_COLOR)
        txt_j2 = self.fuente_marcador.render(f"RIVAL 2 (J2): {self.manager.puntaje_j2} Pts", True, settings.TEXTO_COLOR)
        
        pantalla.blit(txt_j1, (settings.ANCHO // 2 - txt_j1.get_width() // 2, 220))
        pantalla.blit(txt_j2, (settings.ANCHO // 2 - txt_j2.get_width() // 2, 280))
        
        # Muestra el avance (Ej: "Juego 3 de 5")
        txt_progreso = self.fuente_marcador.render(f"Progreso: {self.manager.indice_juego_actual} / {len(self.manager.lista_juegos)}", True, settings.JUGADOR_COLOR)
        pantalla.blit(txt_progreso, (settings.ANCHO // 2 - txt_progreso.get_width() // 2, 380))

        self.btn_siguiente.dibujar(pantalla)