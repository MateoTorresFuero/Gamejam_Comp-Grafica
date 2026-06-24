import pygame

class MinijuegoBase:
    def __init__(self):
        # None = en juego, True = ÉXITO, False = FALLO
        self.resultado = None

    def manejar_eventos(self, eventos):
        """Procesa entradas de teclado/mouse específicas del minijuego."""
        pass

    def actualizar(self, dt):
        """Actualiza la lógica interna usando Delta Time (dt)."""
        pass

    def dibujar(self, pantalla):
        """Renderiza los elementos visuales en la pantalla usando pygame.draw."""
        pass

    def get_resultado(self):
        """Retorna el estado actual del minijuego (None, True o False)."""
        return self.resultado