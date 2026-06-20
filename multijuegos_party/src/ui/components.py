import pygame
from config import settings

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_base, color_hover, color_texto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.fuente = pygame.font.SysFont("consolas", 22, bold=True)
        self.hovered = False

    def manejar_eventos(self, evento):
        """Detecta movimientos y clics del mouse sobre el botón"""
        if evento.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(evento.pos)
            
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.hovered:
                return True  # Indica que el botón fue clickeado
        return False

    def dibujar(self, pantalla):
        # Cambia de color si el cursor está encima
        color_actual = self.color_hover if self.hovered else self.color_base
        
        # Dibujar fondo del botón con bordes redondeados
        pygame.draw.rect(pantalla, color_actual, self.rect, border_radius=8)
        # Borde de brillo neón
        pygame.draw.rect(pantalla, settings.TEXTO_COLOR, self.rect, 2, border_radius=8)
        
        # Renderizar texto centrado
        txt_render = self.fuente.render(self.texto, True, self.color_texto)
        txt_rect = txt_render.get_rect(center=self.rect.center)
        pantalla.blit(txt_render, txt_rect)