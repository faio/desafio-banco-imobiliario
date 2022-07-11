from .base import BasePlayer
from ..property.base import Property


class PlayerImpulsive(BasePlayer):
    """
    Jogador impulsivo.

    Regra:

        * O jogador impulsivo compra qualquer propriedade sobre a qual ele parar.
        * Jogadores só podem comprar propriedades caso ela não tenha dono e o jogador tenha o dinheiro da venda.
    """

    def rule_to_buy(self, property: Property) -> bool:
        return True
