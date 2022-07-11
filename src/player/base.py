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
    def __init__(self, balance: int, id: int):

        self._balance = balance  # Saldo
        self.properties = []  # Propriedades compradas
        self.position = 0  # Posição no tabuleiro
        self.__loser = False  # Variável para controlar se o player perdeu ou não a partida
        self._id = id  # Ordem da criação

    def __repr__(self) -> str:
        return f'{self._strategy.title()} - {self.id}, Balance: {self.balance}, position: {self.position}'

    def __eq__(self, o: object) -> bool:
        return self.id == o.id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        raise ValueError("O ID não pode ser alterado")

    @property
    def balance(self) -> int:
        return self._balance

    @balance.setter
    def balance(self, value: int) -> None:

        if isinstance(value, (int,)):
            self._balance = value
        else:
            raise ValueError("O saldo para atribuição precisa ser um valor númerico interio")

    def _add_property(self, property: Property) -> None:
        self.properties.append(property)
        property.owner = self

    def is_alive(self) -> bool:
        """ Verifica se o jogador ainda está no jogo """
        return self.__loser is False and self.balance >= 0

    def is_can_buy(self, property: Property) -> bool:
        """ Valida se o jogador pode ou não comprar a propriedade informada """
        return property.available and property.price <= self.balance

    def buy(self, property: Property) -> None:
        """
        Faz a compra da propriedade caso o usuário queira e possa
        """

        # Jogadores só podem comprar propriedades caso ela não tenha dono e o jogador tenha o dinheiro da venda.
        if not self.is_can_buy(property):
            return

        # Verificando se o jogador quer comprar o imóvel
        if not self.rule_to_buy(property):
            return

        self.balance -= property.price
        self._add_property(property)
        self.__loser = self.balance < 0

    def pay_rent(self, property: Property) -> None:
        self.balance -= property.rent
        property.owner.balance += property.rent

        self.__loser = self.balance < 0

    @abstractmethod
    def rule_to_buy(self, property: Property) -> bool:
        """
        Regras para efetuar a compra de cada tipo de jogador
        :return: Retorna true caso o jogador vá efetuar a compra do imóvel
        """
        raise NotImplementedError

    @abstractmethod
    def _strategy(self) -> str:
        """ Nome da estratégia que está sendo utilizada"""
        raise NotImplementedError
