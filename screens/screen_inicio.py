import pygame

from settings import AMARILLO, BLANCO, NARANJA, NEGRO


class ScreenInicio:
    def __init__(self, gm):
        self.gm = gm
        self.fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        self.fuente_sub = pygame.font.SysFont("Arial", 24)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                self.gm.iniciar_partida()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                self.gm.iniciar_partida()

    def actualizar(self, dt):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(NEGRO)

        titulo = self.fuente_titulo.render("Pollería del Revés", True, NARANJA)
        subtitulo = self.fuente_sub.render("La vida da vueltas...", True, AMARILLO)
        instruccion = self.fuente_sub.render("Presiona ESPACIO o clic para jugar", True, BLANCO)

        pantalla.blit(titulo, titulo.get_rect(center=(400, 200)))
        pantalla.blit(subtitulo, subtitulo.get_rect(center=(400, 260)))
        pantalla.blit(instruccion, instruccion.get_rect(center=(400, 380)))
