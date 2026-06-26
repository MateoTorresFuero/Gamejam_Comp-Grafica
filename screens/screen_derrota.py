import pygame

from settings import BLANCO, NEGRO, ROJO, ANCHO, ALTO
from utils.assets import get_asset_manager


class ScreenDerrota:
    def __init__(self, gm):
        self.gm = gm
        self.fuente_titulo = pygame.font.SysFont("Arial", 36, bold=True)
        self.fuente_subtitulo = pygame.font.SysFont("Arial", 20, bold=True)
        self.assets = get_asset_manager()

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                self.gm.reiniciar()

    def actualizar(self, dt):
        pass

    def dibujar(self, pantalla):
        # 1. Dibujar imagen de gameover como fondo a pantalla completa
        fondo = self.assets.get("gameover")
        if fondo is not None:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(NEGRO)

        # 2. Mensajes informativos sin mostrar dinero acumulado
        txt_gameover = self.fuente_titulo.render("GAME OVER", True, ROJO)
        txt_espacio = self.fuente_subtitulo.render("Presiona la tecla ESPACIO para reintentar", True, BLANCO)
        
        # Calcular el tamaño del pill contenedor
        w_go, h_go = txt_gameover.get_size()
        w_sp, h_sp = txt_espacio.get_size()
        
        ancho_pill = max(w_go, w_sp) + 40
        alto_pill = h_go + h_sp + 25
        
        rx = ANCHO // 2 - ancho_pill // 2
        ry = ALTO - alto_pill - 40
        
        pill = pygame.Surface((ancho_pill, alto_pill), pygame.SRCALPHA)
        pill.fill((30, 20, 20, 220))  # Fondo marrón/rojizo oscuro semitransparente
        pygame.draw.rect(pill, (*ROJO, 120), pill.get_rect(), width=2, border_radius=10)
        
        pantalla.blit(pill, (rx, ry))
        
        # Dibujar textos centrados
        pantalla.blit(txt_gameover, (ANCHO // 2 - w_go // 2, ry + 12))
        pantalla.blit(txt_espacio, (ANCHO // 2 - w_sp // 2, ry + 12 + h_go + 4))
