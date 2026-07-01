import pygame
from config import settings
from src.scenes.base_scene import BaseScene
from .domain.constants import *
from .domain.car import Car
from .core.physics import RacingPhysics

class RacingGame(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fuente_pequena = pygame.font.SysFont("consolas", 20)
        self.fuente_mediana = pygame.font.SysFont("consolas", 24, bold=True)
        self.fuente_grande = pygame.font.SysFont("consolas", 46, bold=True)
        
        # Inicialización de la pista con múltiples checkpoints
        self.rect_ext, self.rect_int, self.linea_meta, self.checkpoints = \
            RacingPhysics.inicializar_pista_geometria(settings.ANCHO, settings.ALTO)
            
        self.reiniciar_partida()

    def reiniciar_partida(self):
        # Posición inicial cómoda en la recta superior norte
        self.carro_p1 = Car(x=260, y=90, angulo_inicial=180, jugador_id=1)
        self.carro_p2 = Car(x=260, y=125, angulo_inicial=180, jugador_id=2)
        
        self.ganador_id = None
        self.estado_interno = "JUGANDO"

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
        if self.estado_interno != "JUGANDO":
            return

        teclas = pygame.key.get_pressed()

        # --- TELEMETRÍA Y CONTROLES JUGADOR 1 (WASD) ---
        limite_p1 = RacingPhysics.determinar_velocidad_limite(
            self.carro_p1, self.rect_ext, self.rect_int, VEL_MAX_PISTA, VEL_MAX_PASTO
        )
        if teclas[pygame.K_w]:
            self.carro_p1.acelerar(reversa=False, velocidad_limite=limite_p1)
        elif teclas[pygame.K_s]:
            self.carro_p1.acelerar(reversa=True, velocidad_limite=limite_p1)
        else:
            self.carro_p1.aplicar_friccion()

        if teclas[pygame.K_a]:
            self.carro_p1.rotar("IZQUIERDA")
        elif teclas[pygame.K_d]:
            self.carro_p1.rotar("DERECHA")

        # --- TELEMETRÍA Y CONTROLES JUGADOR 2 (FLECHAS) ---
        limite_p2 = RacingPhysics.determinar_velocidad_limite(
            self.carro_p2, self.rect_ext, self.rect_int, VEL_MAX_PISTA, VEL_MAX_PASTO
        )
        if teclas[pygame.K_UP]:
            self.carro_p2.acelerar(reversa=False, velocidad_limite=limite_p2)
        elif teclas[pygame.K_DOWN]:
            self.carro_p2.acelerar(reversa=True, velocidad_limite=limite_p2)
        else:
            self.carro_p2.aplicar_friccion()

        if teclas[pygame.K_LEFT]:
            self.carro_p2.rotar("IZQUIERDA")
        elif teclas[pygame.K_RIGHT]:
            self.carro_p2.rotar("DERECHA")

        # --- CONTROL DE COLISIÓN ENTRE VEHÍCULOS (NUEVO) ---
        RacingPhysics.verificar_colision_autos(self.carro_p1, self.carro_p2)

        # --- APLICAR FISICAS INDIVIDUALES Y CHECKPOINTS ---
        for carro in (self.carro_p1, self.carro_p2):
            carro.actualizar_posicion()
            RacingPhysics.procesar_vueltas_y_checkpoints(carro, self.linea_meta, self.checkpoints)

        # --- DETECTAR REY DE LA PARRILLA ---
        if self.carro_p1.termino_carrera:
            self.ganador_id = 1
            self.estado_interno = "GAME_OVER"
            self.manager.registrar_victoria(1)
        elif self.carro_p2.termino_carrera:
            self.ganador_id = 2
            self.estado_interno = "GAME_OVER"
            self.manager.registrar_victoria(2)

    def dibujar(self, superficie):
        # Dibujar asfalto
        superficie.fill(COLOR_FONDO_RR)
        pygame.draw.rect(superficie, COLOR_PISTA, self.rect_ext)
        pygame.draw.rect(superficie, COLOR_FONDO_RR, self.rect_int)
        
        # Líneas de contención neón
        pygame.draw.rect(superficie, COLOR_BORDE, self.rect_ext, width=2)
        pygame.draw.rect(superficie, COLOR_BORDE, self.rect_int, width=2)

        # Pintar línea de meta
        pygame.draw.rect(superficie, COLOR_META, self.linea_meta)

        # [Opcional / Debug Funcional]: Para ver las líneas invisibles de los 3 checkpoints,
        # puedes descomentar las siguientes líneas si necesitas testear la trayectoria física:
        # for cp in self.checkpoints:
        #     pygame.draw.rect(superficie, (50, 50, 70), cp)

        # Renderizar carros como rectángulos orientados vectorialmente
        for carro in (self.carro_p1, self.carro_p2):
            color = COLOR_CARRO_1 if carro.jugador_id == 1 else COLOR_CARRO_2
            
            carro_surf = pygame.Surface((carro.ancho, carro.alto), pygame.SRCALPHA)
            carro_surf.fill(color)
            
            # Trompa del auto blanca para conocer el frente en plena colisión
            pygame.draw.rect(carro_surf, (255, 255, 255), (carro.ancho - 6, 0, 6, carro.alto))
            
            surf_rotada = pygame.transform.rotate(carro_surf, carro.angulo)
            rect_rotado = surf_rotada.get_rect(center=(carro.x, carro.y))
            superficie.blit(surf_rotada, rect_rotado)

        # UI del estado de la carrera
        txt_v1 = self.fuente_pequena.render(f"P1 Vuelta: {self.carro_p1.vuelta_actual}/{MAX_VUELTAS}", True, COLOR_CARRO_1)
        txt_v2 = self.fuente_pequena.render(f"P2 Vuelta: {self.carro_p2.vuelta_actual}/{MAX_VUELTAS}", True, COLOR_CARRO_2)
        superficie.blit(txt_v1, (40, 10))
        superficie.blit(txt_v2, (settings.ANCHO - txt_v2.get_width() - 40, 10))

        # UI de Game Over
        if self.estado_interno == "GAME_OVER":
            overlay = pygame.Surface((settings.ANCHO, settings.ALTO))
            overlay.set_alpha(225)
            overlay.fill((10, 10, 15))
            superficie.blit(overlay, (0, 0))

            texto_ganador = self.fuente_grande.render(f"¡GANADOR: JUGADOR {self.ganador_id}!", True, COLOR_BORDE)
            texto_reintentar = self.fuente_pequena.render("Presiona [R / ESPACIO] para revancha o [ESC] para salir", True, (200, 200, 200))

            superficie.blit(texto_ganador, (settings.ANCHO // 2 - texto_ganador.get_width() // 2, settings.ALTO // 2 - 40))
            superficie.blit(texto_reintentar, (settings.ANCHO // 2 - texto_reintentar.get_width() // 2, settings.ALTO // 2 + 40))