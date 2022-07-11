from .property.base import Property

from random import (
    randint,
    choices as random_choices
)

from .player import (
    BasePlayer,
    PlayerCautious,
    PlayerImpulsive,
    PlayerDemanding,
    PlayerRandom,
)


class Board(object):
    """
    Manipula as regras básicas do tabuleiro dentro do jogo, permitindo visualizar e controlar o andamento do jogo

    Regras:
        * Os jogadores se alteram em rodadas, numa ordem definida aleatoriamente no começo da partida
        * Os jogadores sempre começam uma partida com saldo de 300 para cada um
        * Nesse jogo, o tabuleiro é composto por 20 propriedades em sequência
        * No começo da sua vez o jogador joga um dado equiprovável de 6 faces que determina
            quantas espaços no tabuleiro o jogador vai andar.
        * Ao cair em uma propriedade sem proprietário, o jogador pode escolher entre comprar
            ou não a propriedade. Esse é a única forma pela qual uma propriedade pode ser comprada.
        * Ao cair em uma propriedade que tem proprietário, ele deve pagar ao proprietário o valor do aluguel
            da propriedade.
        * Ao completar uma volta no tabuleiro, o jogador ganha 100 de saldo.
        * Termina quando restar somente um jogador com saldo positivo, a qualquer momento da partida.
            Esse jogador é declarado o vencedor.
    """

    def __init__(self):
        self.players = list()
        self.properties = list()
        self.losers_players = list()
        self.winner = None  # Quem venceu essa partida

    def roll_dice(self):
        return randint(1, 6)

    def create_random_players(self):
        """
        Cria os jogadores de forma aleatório

        OBS: o saldo inicial é de 300
        """

        players_types = [
            PlayerCautious,
            PlayerImpulsive,
            PlayerDemanding,
            PlayerRandom,
        ]

        self.players = []

        while players_types:
            choice = random_choices(players_types)[0]
            player = choice(
                balance=300,
                id=len(self.players) + 1
            )

            self.players.append(player)
            players_types.remove(choice)

    def create_properties(self):
        """
        Cria as 20 propriedades necessarias para o jogo

        OBS: como não foi informado o valor de compra e de aluguel de cada propriedade,
        o mesmo é gerado de forma randonimaca com valores que começam em 50 até 300
        """

        self.properties = []

        for i in range(0, 20):
            price = randint(50, 300)
            rent = randint(50, 300)

            self.properties.append(Property(
                price=price,
                rent=rent,
                position=i + 1
            ))

    def walk(self, player: BasePlayer):
        """ Faz o jogador andar no tabuleiro """

        walk = self.roll_dice()
        position = player.position + walk
        length_board = len(self.properties)

        # Significa que o jogador chegou no final, e adiciona 100 ao saldo
        if position > length_board:
            player.balance += 100
            position -= length_board

        player.position = position

    def pay_property(self, player: BasePlayer) -> None:
        """ Define se o usuário vai comprar o imóvel ou só irá pagar o aluguel """

        property = self.properties[player.position - 1]

        # O jogador atual é o dono da propriedade, então não tem o que ser pago
        if property.owner and property.owner.id == player.id:
            pass

        if property.available:
            player.buy(property)
        else:
            player.pay_rent(property)

    def remove_loser(self, player: BasePlayer) -> None:
        """ Remove do jogo o jogador se ele tiver perdido a partida """

        if not player.is_alive():
            for prop in player.properties:
                prop.owner = None

            self.losers_players.append(player)
            self.players.remove(player)

    def play(self):
        """ Inicia o jogo """
        self.create_random_players()
        self.create_properties()

        MAX_ROUND = 1000  # Quantidade máxima de partida
        current_round = 0  # Round atual

        while current_round < MAX_ROUND and self.players:
            current_round += 1

            # Quando tem apenas um jogador, o jogo encerra
            if len(self.players) == 1:
                self.winner = self.players[0]
                break

            for player in self.players:
                self.walk(player)
                self.pay_property(player)
                self.remove_loser(player)

        # Chegou na rodada final, portanto o vencedor será decidido por quem tem o maior saldo e como
        # critério de desempate, a ordem de turno dos jogadores nesta partida
        if current_round == MAX_ROUND and not self.winner:
            self.players.sort(key=lambda p: (p.balance, -p.id), reverse=True)
