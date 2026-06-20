import pygame

# Dimensiones de la ventana y rendimiento
ANCHO = 800
ALTO = 600
FPS = 60

# Paleta de Colores Neon Cyberpunk
COLOR_FONDO = (18, 18, 32)
COLOR_PLATAFORMA = (35, 35, 55)
LINEA_NEON = (0, 255, 200)
JUGADOR_COLOR = (255, 0, 128)
OBSTACULO_COLOR = (255, 180, 0)
TEXTO_COLOR = (240, 240, 255)

# Configuración del escenario del Runner
ALTURA_PLATAFORMA = 60
SUELO_Y = ALTO - ALTURA_PLATAFORMA
TECHO_Y = ALTURA_PLATAFORMA