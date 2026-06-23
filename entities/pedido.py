import random

from settings import (
    PENALIZACION_FALLO,
    PRECIO_CUARTO,
    PRECIO_ENTERO,
    PRECIO_MAIZ,
    PRECIO_MEDIO,
    PRECIO_MINIMO_COBRO,
)

TIPOS_PLATO = {
    "cuarto": PRECIO_CUARTO,
    "medio": PRECIO_MEDIO,
    "entero": PRECIO_ENTERO,
}

NOMBRES_PLATO = {
    "cuarto": "1/4 de humano",
    "medio": "1/2 humano",
    "entero": "Humano entero",
}


def _secuencia_minijuegos(tipo: str, con_maiz: bool) -> list[str]:
    if tipo == "cuarto":
        secuencia = ["horno"]
    elif tipo == "medio":
        secuencia = ["horno", "corte"]
    else:
        secuencia = ["horno", "corte", "horno"]

    if con_maiz:
        secuencia.append("maiz")

    return secuencia


class Pedido:
    def __init__(self, tipo: str, con_maiz: bool = False):
        self.tipo = tipo
        self.con_maiz = con_maiz
        self.precio_base = TIPOS_PLATO[tipo] + (PRECIO_MAIZ if con_maiz else 0)
        self.precio_actual = self.precio_base
        self.minijuegos = _secuencia_minijuegos(tipo, con_maiz)
        self.cancelado = False

    @property
    def nombre(self) -> str:
        nombre = NOMBRES_PLATO[self.tipo]
        if self.con_maiz:
            nombre += " + maíz"
        return nombre

    def aplicar_penalizacion(self) -> None:
        self.precio_actual -= PENALIZACION_FALLO
        if self.precio_actual <= PRECIO_MINIMO_COBRO:
            self.cancelado = True

    @classmethod
    def generar_aleatorio(cls) -> "Pedido":
        tipo = random.choice(list(TIPOS_PLATO.keys()))
        con_maiz = random.choice([True, False])
        return cls(tipo, con_maiz)
