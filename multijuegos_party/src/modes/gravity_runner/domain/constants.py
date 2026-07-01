# src/modes/gravity_runner/domain/constants.py
import pygame

# Dimensiones y Límites (Asegúrate de que coincidan o escalen con tu config.settings)
ANCHO_JUGADOR = 40
ALTO_JUGADOR = 40
X_INICIAL_J1 = 100
X_INICIAL_J2 = 140  # Ligeramente desplazado para que no se solapen al iniciar

# Colores de Jugadores (Estilo Neon/Cyberpunk)
COLOR_J1 = (0, 255, 204)   # Cyan Neón
COLOR_J2 = (255, 0, 128)   # Magenta/Rosado Neón

# Tipos de Obstáculos
TIPO_SUELO = 0
TIPO_TECHO = 1
TIPO_AEREO = 2

# Configuración de Obstáculos
ANCHO_OBS_MIN = 30
ANCHO_OBS_MAX = 50
ALTO_OBS_MIN = 50
ALTO_OBS_MAX = 110
FRECUENCIA_MINIMA_BASE = 40