# src/modes/memory_grid/core/logic.py
import random
from ..domain.constants import FILAS, COLUMNAS
from ..domain.card import Card

class MemoryLogic:
    def __init__(self):
        self.puntuacion_p1 = 0
        self.puntuacion_p2 = 0
        self.turno_jugador = 1  # 1 = Jugador 1, 2 = Jugador 2
        self.tarjetas_seleccionadas = []  # Almacena hasta un máximo de 2 tarjetas elegidas
        
    def generar_tablero(self, inicio_x, inicio_y, ancho_t, alto_t, margen):
        """Genera y mezcla los pares de tarjetas de forma matemática."""
        num_pares = (FILAS * COLUMNAS) // 2
        # Creamos una lista con parejas de IDs: [1, 1, 2, 2, 3, 3...]
        iconos = list(range(1, num_pares + 1)) * 2
        random.shuffle(iconos)
        
        tablero = []
        indice = 0
        for f in range(FILAS):
            for c in range(COLUMNAS):
                x = inicio_x + c * (ancho_t + margen)
                y = inicio_y + f * (alto_t + margen)
                tablero.append(Card(f, c, x, y, iconos[indice]))
                indice += 1
        return tablero

    def procesar_seleccion(self, tarjeta):
        """
        Reglas de Negocio ante la selección de una tarjeta.
        Retorna True si se completó un par en este movimiento, False de lo contrario.
        """
        # BUG SHIELD: Ignorar por completo clics en tarjetas ya volteadas o resueltas
        if tarjeta.volteada or tarjeta.resuelta:
            return None
            
        tarjeta.volteada = True
        self.tarjetas_seleccionadas.append(tarjeta)
        
        # Si ya se volteó el par, evaluamos el resultado
        if len(self.tarjetas_seleccionadas) == 2:
            card1, card2 = self.tarjetas_seleccionadas
            
            if card1.icono_id == card2.icono_id:
                # ¡Punto conseguido!
                card1.resuelta = True
                card2.resuelta = True
                self.asignar_punto_actual()
                self.tarjetas_seleccionadas.clear()
                return True  # Éxito (Mantiene turno o cambia según diseño; aquí mantiene por el acierto)
            else:
                return False # Error (Las tarjetas se deben volver a voltear en el loop principal)
                
        return None

    def cambiar_turno(self):
        """Alterna estrictamente el flujo de turnos."""
        self.turno_jugador = 2 if self.turno_jugador == 1 else 1

    def asignar_punto_actual(self):
        """Suma el puntaje al jugador que posee el token de turno."""
        if self.turno_jugador == 1:
            self.puntuacion_p1 += 1
        else:
            self.puntuacion_p2 += 1

    def verificar_victoria(self, tablero):
        """Si todas las tarjetas están resueltas, finaliza la partida."""
        return all(card.resuelta for card in tablero)

    def reiniciar_logica(self):
        self.puntuacion_p1 = 0
        self.puntuacion_p2 = 0
        self.turno_jugador = 1
        self.tarjetas_seleccionadas.clear()