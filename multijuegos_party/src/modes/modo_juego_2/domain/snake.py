from src.modes.modo_juego_2.domain.constants import DIR_ARRIBA, DIR_ABAJO, DIR_IZQUIERDA, DIR_DERECHA

class Snake:
    def __init__(self, x, y, jugador_id):
        self.jugador_id = jugador_id
        self.reiniciar(x, y)

    def reiniciar(self, x, y):
        # Para evitar que aparezcan en el mismo sitio, se configuran según su ID
        if self.jugador_id == 1:
            self.cuerpo = [(x, y), (x - 1, y), (x - 2, y)]
            self.direccion = DIR_DERECHA
            self.proxima_direccion = DIR_DERECHA
        else:
            self.cuerpo = [(x, y), (x + 1, y), (x + 2, y)]
            self.direccion = DIR_IZQUIERDA
            self.proxima_direccion = DIR_IZQUIERDA
            
        self.viva = True

    def cambiar_direccion(self, nueva_dir):
        if nueva_dir == DIR_ARRIBA and self.direccion != DIR_ABAJO:
            self.proxima_direccion = nueva_dir
        elif nueva_dir == DIR_ABAJO and self.direccion != DIR_ARRIBA:
            self.proxima_direccion = nueva_dir
        elif nueva_dir == DIR_IZQUIERDA and self.direccion != DIR_DERECHA:
            self.proxima_direccion = nueva_dir
        elif nueva_dir == DIR_DERECHA and self.direccion != DIR_IZQUIERDA:
            self.proxima_direccion = nueva_dir

    def avanzar(self, crecer=False):
        self.direccion = self.proxima_direccion
        cabeza_x, cabeza_y = self.cuerpo[0]
        dir_x, dir_y = self.direccion
        
        nueva_cabeza = (cabeza_x + dir_x, cabeza_y + dir_y)
        self.cuerpo.insert(0, nueva_cabeza)
        
        if not crecer:
            self.cuerpo.pop()

    @property
    def cabeza(self):
        return self.cuerpo[0]