from __future__ import annotations

import pygame

import settings
from utils.assets import get_asset_manager


class AnimacionClientePedido:
    """Pollo mesero recibe el pedido (globo con el plato solicitado)."""

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
        sprite = self._assets.get("pollo_cocinero")
        if sprite is None:
            return

        progreso = min(1.0, self.tiempo / max(0.001, self.duracion * 0.6))
        x_inicio = -40
        x_fin = settings.ANCHO // 2 - 60
        x = int(x_inicio + (x_fin - x_inicio) * progreso)
        y = settings.HUD_ALTO + 200

        rect = sprite.get_rect(center=(x, y))
        pantalla.blit(sprite, rect)

        if self.tiempo > self.duracion * 0.35:
            texto = self.fuente_bocadillo.render(self.nombre_pedido, True, settings.NEGRO)
            padding = 10
            bocadillo = texto.get_rect()
            bocadillo.inflate_ip(padding * 2, padding * 2)
            bocadillo.center = (x + 130, y - 70)
            pygame.draw.rect(pantalla, settings.BLANCO, bocadillo, border_radius=8)
            pygame.draw.rect(pantalla, settings.NARANJA, bocadillo, width=2, border_radius=8)
            pantalla.blit(texto, texto.get_rect(center=bocadillo.center))

        titulo = self.fuente.render("Pollo mesero toma el pedido...", True, settings.BLANCO)
        pantalla.blit(titulo, titulo.get_rect(center=(settings.ANCHO // 2, settings.HUD_ALTO + 40)))


class AnimacionHumanoHorno:
    """Humano se acerca al horno en línea recta (horno estático)."""

    def __init__(self) -> None:
        self.tiempo = 0.0
        self.duracion = settings.ANIM_HORNO_DURACION
        self.terminada = False
        self._assets = get_asset_manager()
        self.fuente = pygame.font.SysFont("Arial", 22, bold=True)

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
        humano_img = self._assets.get("humano_horno")
        if humano_img is None:
            return

        cx = settings.ANCHO // 2
        cy = settings.HUD_ALTO + 260

        # Humano se desliza y se encoge para simular entrar al horno en el fondo de la cocina
        progreso = min(1.0, self.tiempo / max(0.001, self.duracion * 0.85))
        x_inicio = 60
        x_fin = cx + 120
        x_humano = int(x_inicio + (x_fin - x_inicio) * progreso)
        y_humano = cy

        """
        # Reducir escala gradualmente
        escala = 1.0 - 0.6 * progreso
        ancho = max(8, int(humano_img.get_width() * escala))
        alto = max(8, int(humano_img.get_height() * escala))
        
        humano_esc = pygame.transform.smoothscale(humano_img, (ancho, alto))
        humano_rect = humano_esc.get_rect(center=(x_humano, y_humano))
        pantalla.blit(humano_esc, humano_rect)"""

        # Mantener el tamaño original del personaje
        humano_rect = humano_img.get_rect(center=(x_humano, y_humano))
        pantalla.blit(humano_img, humano_rect)

        titulo = self.fuente.render("¡Al horno!", True, settings.BLANCO)
        pantalla.blit(titulo, titulo.get_rect(center=(settings.ANCHO // 2, settings.HUD_ALTO + 40)))


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

        # Dibujar cliente enojado si no fue exitoso
        if not self.feliz:
            sprite = self._assets.get("cliente_enojado")
            if sprite is not None:
                pantalla.blit(sprite, sprite.get_rect(center=(cx, cy)))

        if self.feliz:
            mensaje = "¡Cliente satisfecho! Pedido entregado."
            color = settings.AMARILLO
        else:
            mensaje = "¡Cliente enojado! Se fue sin pagar."
            color = settings.ROJO

        titulo = self.fuente.render(mensaje, True, color)
        pantalla.blit(titulo, titulo.get_rect(center=(settings.ANCHO // 2, settings.HUD_ALTO + 40)))

        # Dibujar los platos completados directamente sobre el mostrador
        if self.feliz and self.tipo_pedido:
            y_base = 400
            
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
                    pantalla.blit(lbl_h, lbl_h.get_rect(center=(x_humano, y_base + 80)))
                
                # 3. Dibujar maíz
                img_maiz = self._assets.get("pedido_maiz")
                if img_maiz:
                    rect_m = img_maiz.get_rect(center=(x_maiz, y_base))
                    pantalla.blit(img_maiz, rect_m)
                    
                    lbl_m = self.fuente.render("Maíz", True, settings.BLANCO)
                    pantalla.blit(lbl_m, lbl_m.get_rect(center=(x_maiz, y_base + 80)))
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
                    pantalla.blit(lbl_h, lbl_h.get_rect(center=(x_humano, y_base + 80)))
