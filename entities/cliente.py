from __future__ import annotations

import pygame

import settings
from utils.assets import get_asset_manager


class AnimacionClientePedido:
    """El cliente realiza el pedido (globo con el plato solicitado)."""

    def __init__(self, nombre_pedido: str) -> None:
        self.nombre_pedido = nombre_pedido
        self.tiempo = 0.0
        self.duracion = settings.ANIM_CLIENTE_DURACION
        self.terminada = False
        self._assets = get_asset_manager()
        self.fuente = pygame.font.SysFont("Arial", 22, bold=True)
        self.fuente_bocadillo = pygame.font.SysFont("Arial", 18)

    def reiniciar(self, nombre_pedido: str) -> None:
        self.nombre_pedido = nombre_pedido
        self.tiempo = 0.0
        self.terminada = False

    def actualizar(self, dt: float) -> None:
        if self.terminada:
            return
        self.tiempo += dt
        if self.tiempo >= self.duracion:
            self.terminada = True

    def dibujar(self, pantalla: pygame.Surface) -> None:
        # El globo de diálogo aparece directamente sobre el cliente de fondo en el mostrador
        progreso = min(1.0, self.tiempo / max(0.001, self.duracion * 0.4))

        if progreso >= 1.0:
            bx = settings.ANCHO // 2
            by = 190
            
            # Dibujar el globo
            txt = self.fuente_bocadillo.render(self.nombre_pedido, True, settings.NEGRO)
            tw, th = txt.get_size()
            pad_x, pad_y = 15, 10
            rect_globo = pygame.Rect(bx - tw // 2 - pad_x, by - th // 2 - pad_y, tw + pad_x * 2, th + pad_y * 2)
            
            # Dibujar globo blanco con borde naranja
            pygame.draw.rect(pantalla, settings.BLANCO, rect_globo, border_radius=10)
            pygame.draw.rect(pantalla, settings.NARANJA, rect_globo, width=2, border_radius=10)
            
            # Dibujar colita del globo apuntando hacia abajo al cliente
            puntos_triangulo = [
                (bx - 10, rect_globo.bottom),
                (bx + 10, rect_globo.bottom),
                (bx, rect_globo.bottom + 12)
            ]
            pygame.draw.polygon(pantalla, settings.BLANCO, puntos_triangulo)
            pygame.draw.line(pantalla, settings.NARANJA, puntos_triangulo[0], puntos_triangulo[2], 2)
            pygame.draw.line(pantalla, settings.NARANJA, puntos_triangulo[1], puntos_triangulo[2], 2)
            
            pantalla.blit(txt, txt.get_rect(center=rect_globo.center))

        titulo = self.fuente.render("El cliente realiza un pedido...", True, settings.BLANCO)
        tw, th = titulo.get_size()
        pad_x, pad_y = 20, 10
        rx = settings.ANCHO // 2 - tw // 2 - pad_x
        ry = settings.HUD_ALTO + 25

        pill = pygame.Surface((tw + pad_x * 2, th + pad_y * 2), pygame.SRCALPHA)
        pill.fill((40, 30, 25, 210))  # Tono marrón oscuro del HUD
        pygame.draw.rect(pill, (*settings.NARANJA, 120), pill.get_rect(), width=2, border_radius=10)
        pantalla.blit(pill, (rx, ry))
        pantalla.blit(titulo, (rx + pad_x, ry + pad_y))


class AnimacionHumanoHorno:
    """Humano se acerca al horno en línea recta (horno estático) y cocinero lo persigue."""

    def __init__(self) -> None:
        self.tiempo = 0.0
        self.duracion = settings.ANIM_HORNO_DURACION
        self.terminada = False

    def reiniciar(self) -> None:
        self.tiempo = 0.0
        self.terminada = False

    def actualizar(self, dt: float) -> None:
        if self.terminada:
            return
        self.tiempo += dt
        if self.tiempo >= self.duracion:
            self.terminada = True

    def dibujar(self, pantalla: pygame.Surface) -> None:
        # Solo muestra el fondo de cocina (gestionado por _dibujar_fondo).
        # No se dibuja ningún sprite ni texto en esta transición.
        pass


class AnimacionResultadoCliente:
    """Cliente satisfecho o enojado según el resultado del pedido."""

    def __init__(self) -> None:
        self.tiempo = 0.0
        self.duracion = settings.ANIM_RESULTADO_DURACION
        self.terminada = False
        self.feliz = True
        self.tipo_pedido: str | None = None
        self.con_maiz = False
        self._assets = get_asset_manager()
        self.fuente = pygame.font.SysFont("Arial", 24, bold=True)

    def reiniciar(self, feliz: bool, tipo_pedido: str | None = None, con_maiz: bool = False) -> None:
        self.feliz = feliz
        self.tipo_pedido = tipo_pedido
        self.con_maiz = con_maiz
        self.tiempo = 0.0
        self.terminada = False

    def actualizar(self, dt: float) -> None:
        if self.terminada:
            return
        self.tiempo += dt
        if self.tiempo >= self.duracion:
            self.terminada = True

    def dibujar(self, pantalla: pygame.Surface) -> None:
        cx = settings.ANCHO // 2
        cy = settings.HUD_ALTO + 240

        if self.feliz:
            mensaje = "¡Cliente satisfecho! Pedido entregado."
            color_texto = settings.AMARILLO
            color_fondo = (30, 25, 10, 200)   # ámbar muy oscuro semitransparente
        else:
            # El cliente enojado ya está dibujado como fondo a pantalla completa
            mensaje = "¡Cliente enojado! Se fue sin pagar."
            color_texto = settings.BLANCO
            color_fondo = (80, 10, 10, 210)   # rojo oscuro semitransparente

        titulo = self.fuente.render(mensaje, True, color_texto)
        tw, th = titulo.get_size()
        pad_x, pad_y = 20, 10
        rx = settings.ANCHO // 2 - tw // 2 - pad_x
        ry = settings.HUD_ALTO + 25

        # Fondo semitransparente tipo pill detrás del texto
        pill = pygame.Surface((tw + pad_x * 2, th + pad_y * 2), pygame.SRCALPHA)
        pill.fill(color_fondo)
        pygame.draw.rect(pill, (*color_texto[:3], 120), pill.get_rect(), width=2, border_radius=10)
        pantalla.blit(pill, (rx, ry))
        pantalla.blit(titulo, (rx + pad_x, ry + pad_y))

        # Dibujar los platos completados directamente sobre el mostrador
        if self.feliz and self.tipo_pedido:
            y_base = 490  # Altura del mostrador de madera en fondo_resultado
            
            if self.con_maiz:
                x_humano = 310
                x_maiz = 490
                
                # 1. Dibujar platos (elipses simulando platos planos en el mostrador)
                pygame.draw.ellipse(pantalla, (220, 220, 220), (x_humano - 75, y_base + 35, 150, 30))
                pygame.draw.ellipse(pantalla, (180, 180, 180), (x_humano - 75, y_base + 35, 150, 30), width=2)
                
                pygame.draw.ellipse(pantalla, (220, 220, 220), (x_maiz - 75, y_base + 35, 150, 30))
                pygame.draw.ellipse(pantalla, (180, 180, 180), (x_maiz - 75, y_base + 35, 150, 30), width=2)
                
                # 2. Dibujar porción humana
                clave_humano = f"pedido_{self.tipo_pedido}"
                img_humano = self._assets.get(clave_humano)
                if img_humano:
                    rect_h = img_humano.get_rect(center=(x_humano, y_base))
                    pantalla.blit(img_humano, rect_h)
                    
                    from entities.pedido import NOMBRES_PLATO
                    nombre_plato = NOMBRES_PLATO.get(self.tipo_pedido, "")
                    lbl_h = self.fuente.render(nombre_plato, True, settings.BLANCO)
                    pantalla.blit(lbl_h, lbl_h.get_rect(center=(x_humano, y_base - 55)))
                
                # 3. Dibujar maíz
                img_maiz = self._assets.get("pedido_maiz")
                if img_maiz:
                    rect_m = img_maiz.get_rect(center=(x_maiz, y_base))
                    pantalla.blit(img_maiz, rect_m)
                    
                    lbl_m = self.fuente.render("Maíz", True, settings.BLANCO)
                    pantalla.blit(lbl_m, lbl_m.get_rect(center=(x_maiz, y_base - 55)))
            else:
                x_humano = 400
                
                # 1. Dibujar plato plano en el mostrador
                pygame.draw.ellipse(pantalla, (220, 220, 220), (x_humano - 85, y_base + 35, 170, 34))
                pygame.draw.ellipse(pantalla, (180, 180, 180), (x_humano - 85, y_base + 35, 170, 34), width=2)
                
                # 2. Dibujar porción humana
                clave_humano = f"pedido_{self.tipo_pedido}"
                img_humano = self._assets.get(clave_humano)
                if img_humano:
                    rect_h = img_humano.get_rect(center=(x_humano, y_base))
                    pantalla.blit(img_humano, rect_h)
                    
                    from entities.pedido import NOMBRES_PLATO
                    nombre_plato = NOMBRES_PLATO.get(self.tipo_pedido, "")
                    lbl_h = self.fuente.render(nombre_plato, True, settings.BLANCO)
                    pantalla.blit(lbl_h, lbl_h.get_rect(center=(x_humano, y_base - 55)))

