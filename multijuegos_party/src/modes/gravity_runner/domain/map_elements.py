import pygame
from config import settings

class PlataformaEstatica:
    def __init__(self, x_absoluto, y, ancho, alto):
        self.x_abs = x_absoluto
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.x_pantalla = x_absoluto

    def actualizar(self, distancia_camara):
        # Desplazamiento síncrono con la cámara
        self.x_pantalla = self.x_abs - distancia_camara

    def obtener_rect(self):
        return pygame.Rect(self.x_pantalla, self.y, self.ancho, self.alto)

    def dibujar(self, superficie):
        rect = self.obtener_rect()
        # Renderizado lógico plano (Color sólido + borde)
        pygame.draw.rect(superficie, settings.COLOR_PLATAFORMA, rect)
        pygame.draw.rect(superficie, (255, 255, 255), rect, 1)


class Pincho:
    def __init__(self, x_absoluto, y_base, tipo="suelo", alto_obstaculo=40):
        self.x_abs = x_absoluto
        self.tipo = tipo
        self.ancho = 32
        self.alto = alto_obstaculo
        self.x_pantalla = x_absoluto
        self.y = y_base # Se calculará al instanciar el mapa (ver siguiente sección)

    def actualizar(self, distancia_camara):
        self.x_pantalla = self.x_abs - distancia_camara

    def obtener_rect(self):
        # Para que se sienta justo como Geometry Dash, la hitbox puede ser ligeramente
        # más pequeña que el dibujo para evitar muertes injustas (un padding de 4px)
        return pygame.Rect(self.x_pantalla + 4, self.y + 4, self.ancho - 8, self.alto - 8)

    def dibujar(self, superficie):
        # Dibujo lógico de un triángulo
        x = self.x_pantalla
        if "suelo" in self.tipo or "plataforma" in self.tipo:
            puntos = [(x, self.y + self.alto), (x + self.ancho // 2, self.y), (x + self.ancho, self.y + self.alto)]
        else: # Techo (Pincho invertido)
            puntos = [(x, self.y), (x + self.ancho // 2, self.y + self.alto), (x + self.ancho, self.y)]
            
        pygame.draw.polygon(superficie, settings.OBSTACULO_COLOR, puntos)
        pygame.draw.polygon(superficie, (255, 255, 255), puntos, 1)


class MetaNivel:
    def __init__(self, x_absoluto):
        self.x_abs = x_absoluto
        self.x_pantalla = x_absoluto
        self.ancho = 50

    def actualizar(self, distancia_camara):
        self.x_pantalla = self.x_abs - distancia_camara

    def obtener_rect(self):
        return pygame.Rect(self.x_pantalla, settings.TECHO_Y, self.ancho, settings.SUELO_Y - settings.TECHO_Y)

    def dibujar(self, superficie):
        # Una línea vertical o barra estilo damero/neón
        rect = self.obtener_rect()
        pygame.draw.rect(superficie, (0, 255, 0), rect, 4) # Verde Meta