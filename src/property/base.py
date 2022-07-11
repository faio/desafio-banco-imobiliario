from typing import Any


class Property(object):
    """
    Regras:

        * Cada propriedade tem um custo de venda
        * Um valor de aluguel
        * um proprietário caso já estejam compradas
        * Seguem uma determinada ordem no tabuleiro.

    OBS: para facilitar a resolução, se utiliza apenas valores inteiros para os campos price e rent

    """

    def __init__(self, price: int, rent: int) -> None:

        self._price = price
        self._rent = rent
        self._owner = None
        self.position = None

    @property
    def available(self) -> bool:
        return self._owner is None

    @property
    def price(self) -> int:
        return self._price

    @price.setter
    def price(self, value: Any) -> Exception:
        raise ValueError("Não se pode alterar o valor da propriedade")

    @property
    def rent(self) -> int:
        return self._rent

    @rent.setter
    def rent(self, value: Any) -> Exception:
        raise ValueError("Não se pode alterar o valor do aluguel da propriedade")

    @property
    def owner(self) -> object:
        return self._owner

    @owner.setter
    def owner(self, value: object) -> None:
        self._owner = value
