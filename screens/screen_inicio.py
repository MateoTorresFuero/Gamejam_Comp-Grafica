import math

import pygame

from settings import ALTO, AMARILLO, ANCHO, BLANCO, NARANJA, NEGRO
from utils.assets import get_asset_manager


class ScreenInicio:
    def __init__(self, gm):
        self.gm = gm
        self.fuente_titulo = pygame.font.SysFont("Arial", 56, bold=True)
        self.fuente_subtitulo = pygame.font.SysFont("Arial", 28, italic=True)
        self.fuente_instruccion = pygame.font.SysFont("Arial", 22)
        self._tiempo = 0.0  # acumulador para animaciones

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                self.gm.iniciar_partida()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                self.gm.iniciar_partida()

    def actualizar(self, dt):
        self._tiempo += dt

    def dibujar(self, pantalla):
        am = get_asset_manager()

        # --- Fondo: imagen del restaurante ---
        fondo = am.get("fondo_restaurante")
        if fondo:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill((40, 20, 10))

        # --- Overlay oscuro semi-transparente para legibilidad ---
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        pantalla.blit(overlay, (0, 0))

        # --- Título con sombra ---
        titulo_texto = "Don Humano"
        sombra = self.fuente_titulo.render(titulo_texto, True, (0, 0, 0))
        titulo = self.fuente_titulo.render(titulo_texto, True, NARANJA)
        cx = ANCHO // 2
        pantalla.blit(sombra, sombra.get_rect(center=(cx + 3, 193)))
        pantalla.blit(titulo, titulo.get_rect(center=(cx, 190)))

        # --- Subtítulo ---
        sub = self.fuente_subtitulo.render("¡El crujiente sabor de la humanidad!", True, AMARILLO)
        pantalla.blit(sub, sub.get_rect(center=(cx, 255)))

        # --- Separador decorativo ---
        linea_y = 295
        pygame.draw.line(pantalla, NARANJA, (cx - 180, linea_y), (cx + 180, linea_y), 2)

        # --- Texto de instrucción con efecto parpadeo suave (fade in/out) ---
        # alpha oscila entre 80 y 255 con seno
        alpha = int(167 + 88 * math.sin(self._tiempo * 3.0))
        alpha = max(60, min(255, alpha))
        instruccion_surf = self.fuente_instruccion.render(
            "Presiona ESPACIO o haz clic para jugar", True, BLANCO
        )
        instruccion_surf.set_alpha(alpha)
        pantalla.blit(instruccion_surf, instruccion_surf.get_rect(center=(cx, 370)))
