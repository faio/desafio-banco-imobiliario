from abc import abstractmethod, ABCMeta
from ..property.base import Property


class BasePlayer(metaclass=ABCMeta):
    """
    Regras dos jogadores:
        * Jogadores só podem comprar propriedades caso ela não tenha dono e o jogador tenha o dinheiro da venda.
        * Ao comprar uma propriedade, o jogador perde o dinheiro e ganha a posse da propriedade.
        * Um jogador que fica com saldo negativo perde o jogo, e não joga mais. Perde suas propriedades e
            portanto podem ser compradas por qualquer outro jogador.
    """
    def __init__(self):

        self._balance = 0  # Saldo
        self._properties = []  # Propriedades compradas
        self._position = None  # Posição no tabuleiro
        self.__loser = False  # Variável para controlar se o player perdeu ou não a partida

    @property
    def balance(self) -> int:
        return self._balance

    @balance.setter
    def balance(self, value: int) -> None:

        if isinstance(value, (int,)):
            self._balance += value
        else:
            raise ValueError("O saldo para atribuição precisa ser um valor númerico interio")

    def add_property(self, property: Property):
        self._properties.append(property)

    def is_alive(self):
        """ Verifica se o jogador ainda está no jogo """
        return self.__loser is False and self.balance >= 0

    def is_can_buy(self, property: Property):
        """ Valida se o jogador pode ou não comprar a propriedade informada """
        return property.available and property.price <= self.balance

    def buy(self, property: Property):
        self.balance -= property.price
        property.owner = self
        self.__loser = self.balance < 0

    def pay_rent(self, property: Property):
        self.balance -= property.rent
        self.__loser = self.balance < 0

    @abstractmethod
    def rule_to_buy(self, property: Property) -> bool:
        """
        Regras para efetuar a compra de cada tipo de jogador
        :return: Retorna true caso o jogador vá efetuar a compra do imóvel
        """
        raise NotImplementedError
