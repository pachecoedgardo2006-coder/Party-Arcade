# src/modes/memory_grid/domain/constants.py

# Configuración de la Grilla (5 filas x 10 columnas = 50 tarjetas / 25 pares)
FILAS = 5
COLUMNAS = 10

# Dimensiones de las tarjetas
TARJETA_ANCHO = 65
TARJETA_ALTO = 80
MARGEN = 10

# Tiempos del Ciclo de Juego (en milisegundos)
TIEMPO_MEMORIZAR = 4000      # 4 segundos al inicio para recordar los iconos
TIEMPO_ERROR_ESPERA = 1200   # 1.2 segundos para mostrar el color rojo si fallan

# Estados de la partida
ESTADO_MEMORIZAR = "MEMORIZANDO"
ESTADO_JUGANDO = "JUGANDO"
ESTADO_BLOQUEADO = "BLOQUEADO"  # Evita clics spameros mientras se ocultan las tarjetas incorrectas
ESTADO_GAME_OVER = "GAME_OVER"

# Paleta Cromática Neón Local (Coherente con la UI del Launcher)
COLOR_FONDO_MG = (15, 15, 23)
COLOR_TARJETA_OCULTA = (40, 40, 60)
COLOR_TARJETA_VOLTEADA = (0, 200, 255)  # Cian Neón
COLOR_TARJETA_PAREJA = (0, 255, 150)    # Verde Neón
COLOR_TARJETA_ERROR = (255, 0, 100)     # Rojo/Rosa Neón