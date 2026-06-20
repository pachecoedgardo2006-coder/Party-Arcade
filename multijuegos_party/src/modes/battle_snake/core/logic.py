from src.modes.battle_snake.domain.constants import ANCHO_GRID, ALTO_GRID

class SnakeLogic:
    @staticmethod
    def verificar_colisiones(snake_actual, todas_las_serpientes):
        cabeza_x, cabeza_y = snake_actual.cabeza

        # 1. Colisión con bordes de la pantalla
        if cabeza_x < 0 or cabeza_x >= ANCHO_GRID or cabeza_y < 0 or cabeza_y >= ALTO_GRID:
            return True

        # 2. Colisión contra cualquier cuerpo en juego (Suyo o del rival)
        for otra_snake in todas_las_serpientes:
            if otra_snake.jugador_id == snake_actual.jugador_id:
                # Si es ella misma, evaluamos excluyendo su cabeza
                if snake_actual.cabeza in otra_snake.cuerpo[1:]:
                    return True
            else:
                # Si es la serpiente enemiga, evaluamos todo el cuerpo entero
                if snake_actual.cabeza in otra_snake.cuerpo:
                    return True

        return False

    @staticmethod
    def verificar_comida(snake, food):
        if snake.cabeza == food.posicion:
            return True
        return False