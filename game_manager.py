from entities.pedido import Pedido
from settings import META_DINERO, PRECIO_MINIMO_COBRO, TIEMPO_LIMITE

PEDIDOS_EN_COLA = 3


class GameManager:
    def __init__(self):
        self.dinero_acumulado = 0
        self.tiempo_restante = TIEMPO_LIMITE
        self.pedidos_disponibles: list[Pedido] = []
        self.pedido_activo: Pedido | None = None
        self.estado = "inicio"
        self.minijuego_actual = None
        self.indice_minijuego = 0
        self._llenar_cola_pedidos()

    def reiniciar(self) -> None:
        self.dinero_acumulado = 0
        self.tiempo_restante = TIEMPO_LIMITE
        self.pedidos_disponibles.clear()
        self.pedido_activo = None
        self.estado = "inicio"
        self.minijuego_actual = None
        self.indice_minijuego = 0
        self._llenar_cola_pedidos()

    def actualizar_timer(self, dt: float) -> None:
        if self.estado not in ("juego", "minijuego"):
            return

        self.tiempo_restante -= dt
        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0
            self.estado = "victoria" if self.dinero_acumulado >= META_DINERO else "derrota"

    def seleccionar_pedido(self, pedido: Pedido) -> bool:
        if self.estado != "juego" or self.pedido_activo is not None:
            return False
        if pedido not in self.pedidos_disponibles:
            return False

        self.pedidos_disponibles.remove(pedido)
        self.pedido_activo = pedido
        self.indice_minijuego = 0
        self.estado = "minijuego"
        self.minijuego_actual = None
        return True

    def registrar_resultado_minijuego(self, exito: bool) -> None:
        if self.pedido_activo is None:
            return

        if not exito:
            self.pedido_activo.aplicar_penalizacion()
            if self.pedido_activo.cancelado:
                self._cancelar_pedido_activo()
                return

        self.indice_minijuego += 1
        if self.indice_minijuego >= len(self.pedido_activo.minijuegos):
            self.cobrar_pedido()

    def cobrar_pedido(self) -> None:
        if self.pedido_activo is None:
            return

        if self.pedido_activo.precio_actual > PRECIO_MINIMO_COBRO:
            self.dinero_acumulado += self.pedido_activo.precio_actual

        self.pedido_activo = None
        self.indice_minijuego = 0
        self.minijuego_actual = None
        self.estado = "juego"
        self.generar_nuevo_pedido()

    def generar_nuevo_pedido(self) -> None:
        self.pedidos_disponibles.append(Pedido.generar_aleatorio())

    def get_minijuego_actual_id(self) -> str | None:
        if self.pedido_activo is None:
            return None
        if self.indice_minijuego >= len(self.pedido_activo.minijuegos):
            return None
        return self.pedido_activo.minijuegos[self.indice_minijuego]

    def _cancelar_pedido_activo(self) -> None:
        self.pedido_activo = None
        self.indice_minijuego = 0
        self.minijuego_actual = None
        self.estado = "juego"
        self._llenar_cola_pedidos()

    def _llenar_cola_pedidos(self) -> None:
        while len(self.pedidos_disponibles) < PEDIDOS_EN_COLA:
            self.generar_nuevo_pedido()

    def iniciar_partida(self) -> None:
        self.reiniciar()
        self.estado = "juego"
