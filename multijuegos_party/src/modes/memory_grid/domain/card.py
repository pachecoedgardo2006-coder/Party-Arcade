# src/modes/memory_grid/domain/card.py
import pygame

class Card:
    def __init__(self, fila, columna, x, y, icono_id):
        self.fila = fila
        self.columna = columna
        self.x = x
        self.y = y
        self.icono_id = icono_id  # Número entero del 1 al 25 que representa su par
        
        # Estados booleanos de la tarjeta
        self.volteada = False
        self.resuelta = False
        
    def obtener_rect(self, ancho, alto):
        """Retorna el objeto Rect de Pygame para detectar colisiones con el mouse."""
        return pygame.Rect(self.x, self.y, ancho, alto)

    def reiniciar(self):
        """Devuelve la tarjeta a su estado inicial oculto."""
        self.volteada = False
        self.resuelta = False