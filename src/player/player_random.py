import random
from ..property.base import Property
from .base import BasePlayer


class PlayerRandom(BasePlayer):
    """
    Jogador aleatório.

    Regra:

        * O jogador aleatório compra a propriedade que ele parar em cima com probabilidade de 50%.
    """

    def rule_to_buy(self, property: Property) -> bool:
        return random.choice([True, False])
