import pygame
import sys
import random
import math

# --- CONFIGURACIÓN E INICIALIZACIÓN DE PYGAME ---
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Gravity Runner Pro - Estructura y Clases")
reloj = pygame.time.Clock()
FPS = 60

# --- PALETA DE COLORES (Estilo vectores de neón) ---
COLOR_FONDO = (18, 18, 32)
COLOR_PLATAFORMA = (35, 35, 55)
LINEA_NEON = (0, 255, 200)
JUGADOR_COLOR = (255, 0, 128)
OBSTACULO_COLOR = (255, 180, 0)
TEXTO_COLOR = (240, 240, 255)

# Dimensiones fijas del escenario
ALTURA_PLATAFORMA = 60
SUELO_Y = ALTO - ALTURA_PLATAFORMA
TECHO_Y = ALTURA_PLATAFORMA

# --- CLASE PARTÍCULA (Efectos visuales de estela) ---
class Particula:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radio = random.randint(3, 6)
        self.vel_x = random.uniform(-4, -2) # Se mueven hacia atrás
        self.vel_y = random.uniform(-1, 1)  # Dispersión vertical
        self.vida = 255 # Opacidad/Tiempo de vida simulación

    def actualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vida -= 8 # Se desvanece gradualmente
        if self.radio > 0.2:
            self.radio -= 0.1 # Se encoge

    def dibujar(self, superficie):
        if self.vida > 0 and self.radio > 0:
            pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), int(self.radio))

# --- CLASE JUGADOR ---
class Jugador:
    def __init__(self):
        self.ancho = 40
        self.alto = 40
        self.x = 120
        self.y = SUELO_Y - self.alto
        self.vel_y = 0
        self.f_gravedad = 0.9
        self.direccion_gravedad = 1 # 1 = Abajo, -1 = Arriba
        self.estela = []
        
        # Variables para deformación elástica (Diseño "Juicy")
        self.escala_x = 1.0
        self.escala_y = 1.0

    def cambiar_gravedad(self):
        self.direccion_gravedad *= -1
        # Se estira verticalmente al cambiar bruscamente de gravedad
        self.escala_y = 1.4
        self.escala_x = 0.7

    def actualizar(self, velocidad_juego):
        # Aplicar física básica
        self.vel_y += self.f_gravedad * self.direccion_gravedad
        self.y += self.vel_y

        # Colisión con el Suelo
        if self.direccion_gravedad == 1:
            if self.y >= SUELO_Y - self.alto:
                self.y = SUELO_Y - self.alto
                self.vel_y = 0
        # Colisión con el Techo
        else:
            if self.y <= TECHO_Y:
                self.y = TECHO_Y
                self.vel_y = 0

        # Retornar el personaje a su forma cuadrada de forma elástica y suave
        self.escala_x += (1.0 - self.escala_x) * 0.15
        self.escala_y += (1.0 - self.escala_y) * 0.15

        # Generar partículas de estela trasera según el movimiento
        if random.random() > 0.2:
            centro_y = self.y + self.alto / 2
            self.estela.append(Particula(self.x, centro_y, JUGADOR_COLOR))

        # Actualizar las partículas existentes
        for p in self.estela[:]:
            p.actualizar()
            if p.vida <= 0 or p.radio <= 0:
                self.estela.remove(p)

    def dibujar(self, superficie):
        # Dibujar estela detrás del jugador
        for p in self.estela:
            p.dibujar(superficie)

        # Calcular dimensiones en base a la deformación actual
        ancho_final = int(self.ancho * self.escala_x)
        alto_final = int(self.alto * self.escala_y)
        
        # Centrar el rectángulo deformado para que no parpadee de esquina
        diff_x = (ancho_final - self.ancho) // 2
        diff_y = (alto_final - self.alto) // 2
        rect_dibujo = pygame.Rect(self.x - diff_x, self.y - diff_y, ancho_final, alto_final)
        
        # Dibujar cubo con bordes ligeramente redondeados (Pygame 2+)
        pygame.draw.rect(superficie, JUGADOR_COLOR, rect_dibujo, border_radius=6)
        pygame.draw.rect(superficie, (255, 255, 255), rect_dibujo, 2, border_radius=6) # Borde blanco de brillo

    def obtener_rect(self):
        # Retorna el rect real sin deformar para colisiones precisas
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

# --- CLASE OBSTÁCULO ---
class Obstaculo:
    def __init__(self, velocidad):
        self.ancho = random.randint(30, 50)
        self.alto = random.randint(50, 120)
        self.x = ANCHO
        self.velocidad = velocidad
        
        # TIPOS: 0 = En el suelo, 1 = En el techo, 2 = Flotante en el medio
        self.tipo = random.choice([0, 1, 2])
        
        if self.tipo == 0:
            self.y = SUELO_Y - self.alto
        elif self.tipo == 1:
            self.y = TECHO_Y
        else:
            self.alto = 50 # Los flotantes son bloques cuadrados perfectos
            self.y = (ALTO // 2) - (self.alto // 2) + random.randint(-40, 40)

    def actualizar(self):
        self.x -= self.velocidad

    def dibujar(self, superficie):
        rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        # Dibujar cuerpo del obstáculo
        pygame.draw.rect(superficie, OBSTACULO_COLOR, rect, border_radius=4)
        # Detalle visual interno para que no se vea plano
        pygame.draw.rect(superficie, (255, 255, 255), rect, 1, border_radius=4)

    def obtener_rect(self):
            rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
            return rect

# --- INICIALIZACIÓN DE VARIABLES DE ESTADO ---
fuente_pequena = pygame.font.SysFont("consolas", 22)
fuente_grande = pygame.font.SysFont("consolas", 48, bold=True)

jugador = Jugador()
obstaculos = []
temporizador_obstaculo = 0

puntuacion = 0
mejor_puntuacion = 0
velocidad_juego = 7
estado_juego = "MENU" # Estados posibles: "MENU", "JUGANDO", "GAME_OVER"


# --- FUNCIONES DE SOPORTE Y CONTROL DE ESTADOS ---
def reiniciar_juego():
    """Restablece los valores iniciales para empezar una nueva partida."""
    global jugador, obstaculos, temporizador_obstaculo, puntuacion, velocidad_juego
    jugador = Jugador()
    obstaculos = []
    temporizador_obstaculo = 0
    puntuacion = 0
    velocidad_juego = 7

def dibujar_escenario():
    """Dibuja el fondo de neón, el techo y el suelo estilizados."""
    pantalla.fill(COLOR_FONDO)
    
    # Dibujo de bloques estructurales (Techo y Suelo)
    pygame.draw.rect(pantalla, COLOR_PLATAFORMA, (0, 0, ANCHO, TECHO_Y))
    pygame.draw.rect(pantalla, COLOR_PLATAFORMA, (0, SUELO_Y, ANCHO, ALTURA_PLATAFORMA))
    
    # Líneas brillantes de neón estilo retro/cyberpunk
    pygame.draw.line(pantalla, LINEA_NEON, (0, TECHO_Y), (ANCHO, TECHO_Y), 3)
    pygame.draw.line(pantalla, LINEA_NEON, (0, SUELO_Y), (ANCHO, SUELO_Y), 3)


# --- SOLUCIÓN AL TYPO DE LA PARTE 1 ---
# Reemplaza la función con error sintáctico de la primera parte de forma dinámica
Obstaculo.obtener_rect = lambda self: pygame.Rect(self.x, self.y, self.ancho, self.alto)


# --- BUCLE PRINCIPAL DEL JUEGO ---
ejecutando = True

while ejecutando:
    # Captura de eventos globales (como cerrar la ventana)
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            ejecutando = False

    # ==========================================
    # LÓGICA DEL ESTADO: MENÚ INICIAL
    # ==========================================
    if estado_juego == "MENU":
        dibujar_escenario()
        
        # Renderizado de textos estéticos para el menú
        texto_titulo = fuente_grande.render("GRAVITY RUNNER", True, LINEA_NEON)
        texto_instrucciones = fuente_pequena.render("Presiona [ESPACIO] para empezar", True, TEXTO_COLOR)
        texto_controles = fuente_pequena.render("Control: [ESPACIO] cambia la gravedad", True, OBSTACULO_COLOR)
        
        # Posicionamiento centrado en pantalla
        pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 2 - 80))
        pantalla.blit(texto_instrucciones, (ANCHO // 2 - texto_instrucciones.get_width() // 2, ALTO // 2 + 10))
        pantalla.blit(texto_controles, (ANCHO // 2 - texto_controles.get_width() // 2, ALTO // 2 + 50))
        
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                reiniciar_juego()
                estado_juego = "JUGANDO"

    # ==========================================
    # LÓGICA DEL ESTADO: JUGANDO (GAMEPLAY)
    # ==========================================
    elif estado_juego == "JUGANDO":
        # 1. Entrada de comandos del jugador en partida
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                jugador.cambiar_gravedad()

        # 2. Actualización de físicas y entidades
        jugador.actualizar(velocidad_juego)
        
        # DIFICULTAD PROGRESIVA: Aceleración sutil constante en cada frame
        velocidad_juego += 0.002
        
        # Temporizador adaptativo para generar nuevos obstáculos
        temporizador_obstaculo += 1
        # A mayor velocidad, los obstáculos aparecen con mayor frecuencia
        frecuencia_minima = max(35, 90 - int(velocidad_juego * 2))
        
        if temporizador_obstaculo > random.randint(frecuencia_minima, frecuencia_minima + 35):
            obstaculos.append(Obstaculo(velocidad_juego))
            temporizador_obstaculo = 0

        # Gestión del ciclo de vida de los obstáculos y colisiones
        rect_jugador = jugador.obtener_rect()
        for obs in obstaculos[:]:
            obs.actualizar()
            
            # Detección estricta de colisiones usando el hitbox real
            if rect_jugador.colliderect(obs.obtener_rect()):
                estado_juego = "GAME_OVER"
                if puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
            
            # Otorgar puntos si el obstáculo sale exitosamente del mapa
            if obs.x + obs.ancho < 0:
                obstaculos.remove(obs)
                puntuacion += 1

        # 3. Renderizado y dibujo en la superficie
        dibujar_escenario()
        jugador.dibujar(pantalla) # Dibuja la estela de partículas y el cubo elástico
        
        for obs in obstaculos:
            obs.dibujar(pantalla)
            
        # Dibujar Interfaz de Usuario (HUD) superior
        txt_puntos = fuente_pequena.render(f"PUNTOS: {puntuacion}", True, TEXTO_COLOR)
        txt_record = fuente_pequena.render(f"RÉCORD: {mejor_puntuacion}", True, LINEA_NEON)
        pantalla.blit(txt_puntos, (20, 15))
        pantalla.blit(txt_record, (ANCHO - txt_record.get_width() - 20, 15))

    # ==========================================
    # LÓGICA DEL ESTADO: GAME OVER
    # ==========================================
    elif estado_juego == "GAME_OVER":
        dibujar_escenario()
        
        # Textos de la pantalla de derrota
        texto_game_over = fuente_grande.render("¡GAME OVER!", True, JUGADOR_COLOR)
        texto_score_final = fuente_pequena.render(f"Puntuación final: {puntuacion}", True, TEXTO_COLOR)
        texto_reintentar = fuente_pequena.render("Presiona [ESPACIO] para reintentar o [M] para Menú", True, OBSTACULO_COLOR)
        
        pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 80))
        pantalla.blit(texto_score_final, (ANCHO // 2 - texto_score_final.get_width() // 2, ALTO // 2 + 10))
        pantalla.blit(texto_reintentar, (ANCHO // 2 - texto_reintentar.get_width() // 2, ALTO // 2 + 50))
        
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    reiniciar_juego()
                    estado_juego = "JUGANDO"
                elif evento.key == pygame.K_m:
                    estado_juego = "MENU"

    # Actualizar la ventana completa y regular la velocidad a 60 FPS estables
    pygame.display.flip()
    reloj.tick(FPS)

# Salida limpia del sistema al romper el bucle
pygame.quit()
sys.exit()