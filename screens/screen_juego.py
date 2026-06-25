import pygame

from entities.pedido import Pedido
from minijuegos.corte import Corte
from minijuegos.horno import Horno
from minijuegos.maiz import Maiz
from settings import AMARILLO, ANCHO, BLANCO, HUD_ALTO, META_DINERO, NARANJA


def _formatear_tiempo(segundos: float) -> str:
    total = max(0, int(segundos))
    minutos = total // 60
    resto = total % 60
    return f"{minutos:02d}:{resto:02d}"


class ScreenJuego:
    MINIJUEGOS_REGISTRO = {
        "horno": Horno,
        "corte": Corte,
        "maiz": Maiz,
    }

    def __init__(self, gm):
        self.gm = gm
        self.fuente_hud = pygame.font.SysFont("Arial", 28, bold=True)
        self.fuente_pedido = pygame.font.SysFont("Arial", 20)
        self.fuente_boton = pygame.font.SysFont("Arial", 18, bold=True)
        self._botones_pedido: list[tuple[pygame.Rect, Pedido]] = []

    def manejar_eventos(self, eventos):
        if self.gm.estado == "juego":
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    for rect, pedido in self._botones_pedido:
                        if rect.collidepoint(evento.pos):
                            self.gm.seleccionar_pedido(pedido)
                            self._iniciar_minijuego_actual()
                            break
        elif self.gm.estado == "minijuego" and self.gm.minijuego_actual is not None:
            self.gm.minijuego_actual.manejar_eventos(eventos)

    def actualizar(self, dt):
        self.gm.actualizar_timer(dt)

        if self.gm.estado != "minijuego":
            return

        if self.gm.minijuego_actual is not None:
            self.gm.minijuego_actual.actualizar(dt)
            resultado = self.gm.minijuego_actual.get_resultado()
            if resultado is not None:
                self.gm.registrar_resultado_minijuego(resultado)
                self.gm.minijuego_actual = None
        elif self.gm.pedido_activo is not None:
            self._iniciar_minijuego_actual()

    def dibujar(self, pantalla):
        pantalla.fill((40, 30, 25))
        self._botones_pedido.clear()

        if self.gm.estado == "juego":
            self._dibujar_cola_pedidos(pantalla)
        elif self.gm.estado == "minijuego" and self.gm.minijuego_actual is not None:
            self.gm.minijuego_actual.dibujar(pantalla)

        if self.gm.estado in ("juego", "minijuego"):
            self._dibujar_hud(pantalla)

    def _iniciar_minijuego_actual(self) -> None:
        id_minijuego = self.gm.get_minijuego_actual_id()
        if id_minijuego in self.MINIJUEGOS_REGISTRO:
            self.gm.minijuego_actual = self.MINIJUEGOS_REGISTRO[id_minijuego]()

    def _dibujar_hud(self, pantalla):
        tiempo = _formatear_tiempo(self.gm.tiempo_restante)
        texto_tiempo = self.fuente_hud.render(f"Tiempo: {tiempo}", True, BLANCO)
        texto_dinero = self.fuente_hud.render(
            f"Total: ${self.gm.dinero_acumulado} / ${META_DINERO}", True, AMARILLO
        )
        pygame.draw.rect(pantalla, (40, 30, 25), (0, 0, ANCHO, HUD_ALTO))
        pantalla.blit(texto_tiempo, (20, 20))
        pantalla.blit(texto_dinero, (480, 20))
        pygame.draw.line(pantalla, NARANJA, (0, HUD_ALTO), (ANCHO, HUD_ALTO), 2)

    def _dibujar_cola_pedidos(self, pantalla):
        inicio_x = 50
        ancho = 220
        separacion = 30

        for i, pedido in enumerate(self.gm.pedidos_disponibles):
            x = inicio_x + i * (ancho + separacion)
            y = 100
            rect = pygame.Rect(x, y, ancho, 160)
            self._botones_pedido.append((rect, pedido))

            pygame.draw.rect(pantalla, (60, 45, 35), rect, border_radius=8)
            pygame.draw.rect(pantalla, NARANJA, rect, width=2, border_radius=8)

            nombre = self.fuente_pedido.render(pedido.nombre, True, BLANCO)
            precio = self.fuente_pedido.render(f"${pedido.precio_actual}", True, AMARILLO)
            boton_rect = pygame.Rect(x + 40, y + 110, 140, 36)
            boton = self.fuente_boton.render("TOMAR", True, (0, 0, 0))

            pantalla.blit(nombre, nombre.get_rect(center=(x + ancho // 2, y + 45)))
            pantalla.blit(precio, precio.get_rect(center=(x + ancho // 2, y + 80)))
            pygame.draw.rect(pantalla, AMARILLO, boton_rect, border_radius=6)
            pantalla.blit(boton, boton.get_rect(center=boton_rect.center))
