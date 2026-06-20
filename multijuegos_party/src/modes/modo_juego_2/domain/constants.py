import pygame

# Dimensiones del área de juego
TAMANIO_CUADRO = 20
ANCHO_GRID = 800 // TAMANIO_CUADRO
ALTO_GRID = 600 // TAMANIO_CUADRO

# Direcciones (Vectores x, y)
DIR_ARRIBA = (0, -1)
DIR_ABAJO = (0, 1)
DIR_IZQUIERDA = (-1, 0)
DIR_DERECHA = (1, 0)

# Colores provisionales de desarrollo
COLOR_FONDO = (20, 20, 20)
COLOR_SNAKE_1 = (0, 255, 0)     # Verde
COLOR_SNAKE_2 = (0, 150, 255)   # Azul
COLOR_COMIDA = (255, 0, 0)      # Rojo