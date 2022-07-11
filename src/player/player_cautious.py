from ..property.base import Property
from .base import BasePlayer


class PlayerCautious(BasePlayer):
    """
    Jogador cauteloso.

    Regra:

        * O jogador cauteloso compra qualquer propriedade desde que ele tenha uma reserva de 80
            saldo sobrando depois de realizada a compra.
        * Jogadores só podem comprar propriedades caso ela não tenha dono e o jogador tenha o dinheiro da venda.
    """

    _strategy = 'cauteloso'

    def rule_to_buy(self, property: Property) -> bool:
        remmant = self.balance - property.price
        return remmant >= 80
