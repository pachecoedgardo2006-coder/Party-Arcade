import random
from src.modes.modo_juego_2.domain.constants import ANCHO_GRID, ALTO_GRID

class Food:
    def __init__(self):
        self.posicion = (0, 0)
        self.reubicar([])

    def reubicar(self, cuerpo_serpiente):
        # Genera comida en una posición libre de la cuadrícula
        while True:
            x = random.randint(0, ANCHO_GRID - 1)
            y = random.randint(0, ALTO_GRID - 1)
            if (x, y) not in cuerpo_serpiente:
                self.posicion = (x, y)
                break