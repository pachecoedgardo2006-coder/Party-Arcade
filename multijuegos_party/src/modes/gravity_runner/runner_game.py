# src/modes/gravity_runner/runner_game.py
import pygame
from config import settings
from src.scenes.base_scene import BaseScene
from .domain.player import Jugador
from .domain.map_elements import PlataformaEstatica, Pincho, MetaNivel
from .domain.constants import COLOR_J1, COLOR_J2, X_INICIAL_J1, X_INICIAL_J2
from .domain.mapa_data import NIVEL_1

class RunnerGame(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fuente_pequena = pygame.font.SysFont("consolas", 20)
        self.fuente_grande = pygame.font.SysFont("consolas", 44, bold=True)
        self.reiniciar_partida()

    def reiniciar_partida(self):
        # Inicialización de los dos competidores con sus controles originales
        self.jugadores = [
            Jugador(id_jugador=1, x_inicial=X_INICIAL_J1, color=COLOR_J1, tecla_salto=pygame.K_SPACE),
            Jugador(id_jugador=2, x_inicial=X_INICIAL_J2, color=COLOR_J2, tecla_salto=pygame.K_UP)
        ]
        
        self.distancia_recorrida = 0  # Actúa como el desplazamiento de la cámara (Scroll X)
        self.velocidad_juego = 7.0    # Velocidad constante de avance en el mapa
        self.estado_interno = "JUGANDO"
        self.ganador_torneo = None
        
        # Carga de la meta y los elementos estructurados del mapa predefinido
        self.meta_distancia = NIVEL_1["distancia_meta"]
        
        self.plataformas = []
        for p in NIVEL_1["plataformas"]:
            self.plataformas.append(PlataformaEstatica(p["x"], p["y"], p["ancho"], p["alto"]))
            
        self.pinchos = []
        for pincho in NIVEL_1["pinchos"]:
            y_calc = settings.SUELO_Y - 40  # Altura por defecto en el suelo base
            if pincho["y"] == "techo":
                y_calc = settings.TECHO_Y
            elif pincho["y"] == "plataforma":
                # Posicionar el pincho exactamente arriba de la plataforma referenciada
                plat_asociada = NIVEL_1["plataformas"][pincho["index_plat"]]
                y_calc = plat_asociada["y"] - 40
                
            self.pinchos.append(Pincho(pincho["x"], y_calc, pincho["y"]))
            
        self.meta = MetaNivel(self.meta_distancia)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if self.estado_interno == "JUGANDO":
                    # Mapeo de controles individuales para el cambio de gravedad
                    for jugador in self.jugadores:
                        if evento.key == jugador.tecla_salto:
                            jugador.cambiar_gravedad()
                            
                elif self.estado_interno in ["GAME_OVER", "VICTORIA"]:
                    if evento.key == pygame.K_SPACE:
                        self.reiniciar_partida()
                    elif evento.key == pygame.K_m:
                        from src.scenes.game_select import GameSelect
                        self.manager.cambiar_escena(GameSelect(self.manager))

    def actualizar(self):
        if self.estado_interno != "JUGANDO":
            return

        # 1. Avanzar la posición de la cámara en el nivel
        self.distancia_recorrida += self.velocidad_juego

        # 2. Actualizar posiciones relativas de los objetos del mapa con respecto a la cámara
        for plat in self.plataformas:
            plat.actualizar(self.distancia_recorrida)
        for pincho in self.pinchos:
            pincho.actualizar(self.distancia_recorrida)
        self.meta.actualizar(self.distancia_recorrida)

        # 3. Actualizar jugadores vivos pasándoles las plataformas para su colisión física
        jugadores_vivos = [j for j in self.jugadores if j.vivo]
        for jugador in jugadores_vivos:
            jugador.actualizar(self.plataformas)

        # 4. Gestión de colisiones mortales con los pinchos del mapa
        for pincho in self.pinchos:
            rect_pincho = pincho.obtener_rect()
            for jugador in jugadores_vivos:
                if jugador.obtener_rect().colliderect(rect_pincho):
                    jugador.vivo = False

        # Re-evaluar los jugadores sobrevivientes tras las colisiones
        jugadores_restantes = [j for j in self.jugadores if j.vivo]

        # 5. Condición de Victoria: Llegar a la meta estilo Geometry Dash
        for jugador in jugadores_restantes:
            if jugador.x >= self.meta.x_pantalla:
                # Si llega a la meta, ese jugador gana directamente y suma su punto en el torneo
                self.finalizar_juego(ganador_id=jugador.id, llego_a_meta=True)
                return

        # 6. Condición de Torneo / Supervivencia (Si alguien muere antes de la meta)
        if len(jugadores_restantes) == 0:
            # En caso de muerte simultánea estricta, se le otorga al J1 por defecto para no congelar
            self.finalizar_juego(ganador_id=1, llego_a_meta=False)
        elif len(jugadores_restantes) == 1 and len(self.jugadores) > 1:
            # Si el rival muere en un pincho, el jugador sobreviviente gana el punto del torneo
            self.finalizar_juego(ganador_id=jugadores_restantes[0].id, llego_a_meta=False)

    def finalizar_juego(self, ganador_id, llego_a_meta=False):
        if llego_a_meta:
            self.estado_interno = "VICTORIA"
        else:
            self.estado_interno = "GAME_OVER"
            
        self.ganador_torneo = ganador_id
        # Registro y asignación automática del punto en el gestor de torneos del Party Hub
        self.manager.registrar_victoria(ganador_id)

    def dibujar_escenario(self, pantalla):
        pantalla.fill(settings.COLOR_FONDO)
        pygame.draw.rect(pantalla, settings.COLOR_PLATAFORMA, (0, 0, settings.ANCHO, settings.TECHO_Y))
        pygame.draw.rect(pantalla, settings.COLOR_PLATAFORMA, (0, settings.SUELO_Y, settings.ANCHO, settings.ALTURA_PLATAFORMA))
        pygame.draw.line(pantalla, settings.LINEA_NEON, (0, settings.TECHO_Y), (settings.ANCHO, settings.TECHO_Y), 3)
        pygame.draw.line(pantalla, settings.LINEA_NEON, (0, settings.SUELO_Y), (settings.ANCHO, settings.SUELO_Y), 3)

    def dibujar(self, pantalla):
        self.dibujar_escenario(pantalla)
        
        # Dibujar elementos interactivos del nivel mapeado
        for plat in self.plataformas:
            plat.dibujar(pantalla)
        for pincho in self.pinchos:
            pincho.dibujar(pantalla)
        self.meta.dibujar(pantalla)
        
        # Dibujar cubos de los jugadores
        for jugador in self.jugadores:
            jugador.dibujar(pantalla)

        # HUD UI según el estado del juego
        if self.estado_interno == "JUGANDO":
            txt_j1 = self.fuente_pequena.render("J1: [ESPACIO]", True, COLOR_J1)
            txt_j2 = self.fuente_pequena.render("J2: [FLECHA ARRIBA]", True, COLOR_J2)
            # Muestra cuánta distancia del mapa han recorrido en píxeles
            txt_dist = self.fuente_pequena.render(f"PROGRESO: {int(self.distancia_recorrida)}m / {self.meta_distancia}m", True, settings.TEXTO_COLOR)
            
            pantalla.blit(txt_j1, (20, 15))
            pantalla.blit(txt_j2, (settings.ANCHO - txt_j2.get_width() - 20, 15))
            pantalla.blit(txt_dist, (settings.ANCHO // 2 - txt_dist.get_width() // 2, 15))
            
        elif self.estado_interno in ["GAME_OVER", "VICTORIA"]:
            color_ganador = COLOR_J1 if self.ganador_torneo == 1 else COLOR_J2
            mensaje = f"¡VICTORIA PARA JUGADOR {self.ganador_torneo}!" if self.estado_interno == "VICTORIA" else f"¡JUGADOR {self.ganador_torneo} GANA POR SUPERVIVENCIA!"
            
            texto_titulo = self.fuente_grande.render(mensaje, True, color_ganador)
            texto_score = self.fuente_pequena.render(f"Recorrido total: {int(self.distancia_recorrida)} unidades", True, settings.TEXTO_COLOR)
            texto_reintentar = self.fuente_pequena.render("Presiona [ESPACIO] para revancha o [M] para Menú", True, settings.OBSTACULO_COLOR)
            
            pantalla.blit(texto_titulo, (settings.ANCHO // 2 - texto_titulo.get_width() // 2, settings.ALTO // 2 - 60))
            pantalla.blit(texto_score, (settings.ANCHO // 2 - texto_score.get_width() // 2, settings.ALTO // 2 + 15))
            pantalla.blit(texto_reintentar, (settings.ANCHO // 2 - texto_reintentar.get_width() // 2, settings.ALTO // 2 + 55))