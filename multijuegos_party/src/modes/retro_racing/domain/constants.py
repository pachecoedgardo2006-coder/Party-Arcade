import pygame

# Dimensiones de la pista funcional (Mapeada sobre el estándar 800x600)
ANCHO_PISTA = 800
ALTO_PISTA = 600

# Colores locales con estética Neón para el Hub
COLOR_FONDO_RR = (15, 15, 22)
COLOR_PISTA = (30, 30, 45)
COLOR_BORDE = (0, 255, 200)       # Línea Neón exterior/interior
COLOR_META = (255, 255, 255)       # Línea de meta blanca/cuadros
COLOR_CARRO_1 = (255, 0, 100)      # Fucsia Neón P1
COLOR_CARRO_2 = (0, 150, 255)      # Azul Neón P2

# Reglas de juego
MAX_VUELTAS = 3

# Físicas del vehículo arcade
VEL_MAX_PISTA = 5.0
VEL_MAX_PASTO = 1.5                # Penalización por salirse de la pista
ACELERACION = 0.15
FRENADO = 0.25
FRICCION = 0.05
VEL_ROTACION = 4.5                 # Velocidad de giro en grados por frame