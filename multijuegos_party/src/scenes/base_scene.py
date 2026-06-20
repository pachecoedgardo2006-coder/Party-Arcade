from abc import ABC, abstractmethod

class BaseScene(ABC):
    def __init__(self, manager):
        self.manager = manager  # Permite a la escena pedir un cambio de pantalla

    @abstractmethod
    def manejar_eventos(self, eventos):
        pass

    @abstractmethod
    def actualizar(self):
        pass

    @abstractmethod
    def dibujar(self, pantalla):
        pass