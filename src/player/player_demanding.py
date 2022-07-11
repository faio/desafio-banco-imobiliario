from ..property.base import Property
from .base import BasePlayer


class PlayerDemanding(BasePlayer):
    """
    Jogador exigente.

    Regra:

        * O jogador exigente compra qualquer propriedade, desde que o valor do aluguel dela seja maior do que 50.
    """

    def rule_to_buy(self, property: Property) -> bool:
        return property.rent > 50
