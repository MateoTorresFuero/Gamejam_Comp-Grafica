import pygame

from settings import BLANCO, NEGRO, ROJO


class ScreenDerrota:
    def __init__(self, gm):
        self.gm = gm
        self.fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        self.fuente_info = pygame.font.SysFont("Arial", 24)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                self.gm.reiniciar()

    def actualizar(self, dt):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(NEGRO)

        titulo = self.fuente_titulo.render("Derrota", True, ROJO)
        info = self.fuente_info.render(
            f"Solo acumulaste ${self.gm.dinero_acumulado}. Presiona ESPACIO para reintentar.",
            True,
            BLANCO,
        )
        pantalla.blit(titulo, titulo.get_rect(center=(400, 240)))
        pantalla.blit(info, info.get_rect(center=(400, 310)))
