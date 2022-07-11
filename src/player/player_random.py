import random
from ..property.base import Property
from .base import BasePlayer


class PlayerRandom(BasePlayer):
    """
    Jogador aleatório.

    Regra:

        * O jogador aleatório compra a propriedade que ele parar em cima com probabilidade de 50%.
        * Jogadores só podem comprar propriedades caso ela não tenha dono e o jogador tenha o dinheiro da venda.
    """

    def rule_to_buy(self, property: Property) -> bool:
        return random.choice([True, False])
