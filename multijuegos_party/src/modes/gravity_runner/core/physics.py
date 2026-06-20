# src/modes/gravity_runner/core/physics.py
from config import settings

class PhysicsEngine:
    @staticmethod
    def aplicar_gravedad(entidad):
        """
        Calcula el movimiento aplicando gravedad y evalúa colisiones basándose 
        en la dirección real del movimiento físico (vel_y).
        """
        # 1. Aplicar aceleración
        entidad.vel_y += entidad.f_gravedad * entidad.direccion_gravedad
        
        # 2. Predicción de posición
        siguiente_y = entidad.y + entidad.vel_y

        # 3. Evaluar colisiones basándose en el vector de movimiento real (vel_y)
        if entidad.vel_y > 0:  # El cuerpo se está moviendo hacia ABAJO
            limite_inferior = settings.SUELO_Y - entidad.alto
            if siguiente_y >= limite_inferior:
                entidad.y = limite_inferior
                entidad.vel_y = 0
                entidad.en_suelo = True
            else:
                entidad.y = siguiente_y

        elif entidad.vel_y < 0:  # El cuerpo se está moviendo hacia ARRIBA
            limite_superior = settings.TECHO_Y
            if siguiente_y <= limite_superior:
                entidad.y = limite_superior
                entidad.vel_y = 0
                entidad.en_suelo = True
            else:
                entidad.y = siguiente_y
        
        else:
            # Si vel_y es exactamente 0, mantenemos la posición predicha de forma segura
            entidad.y = siguiente_y