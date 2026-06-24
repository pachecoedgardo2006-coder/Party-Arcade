# src/modes/sumo_combat/domain/constants.py
import pygame

# Dimensiones lógicas locales
RADIO_ARENA = 230
CENTRO_ARENA = (400, 300)

# Propiedades de los luchadores (Sumos) - 🛠️ AJUSTADAS PARA MAYOR IMPACTO
SUMO_RADIO = 25
SUMO_MASA = 1.0
SUMO_FUERZA = 0.55    # ⬆️ Aumentado (Antes: 0.45) para acelerar con más potencia
SUMO_FRICCION = 0.94  # ⬆️ Menos fricción (Antes: 0.92) para que "resbalen" más y mantengan el impulso

# Puntuación máxima para ganar la partida
PUNTOS_VICTORIA = 3

# Paleta de Colores
COLOR_FONDO_SC = (15, 15, 22)
COLOR_ARENA = (40, 40, 50)
COLOR_BORDE_ARENA = (255, 0, 100)      
COLOR_SUMO_1 = (0, 255, 200)          
COLOR_SUMO_2 = (255, 200, 0)          

# Mapeo estricto de controles por jugador
CONTROLES = {
    1: {
        "ARRIBA": pygame.K_w,
        "ABAJO": pygame.K_s,
        "IZQUIERDA": pygame.K_a,
        "DERECHA": pygame.K_d
    },
    2: {
        "ARRIBA": pygame.K_UP,
        "ABAJO": pygame.K_DOWN,
        "IZQUIERDA": pygame.K_LEFT,
        "DERECHA": pygame.K_RIGHT
    }
}