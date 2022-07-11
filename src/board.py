from random import randint


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
        pass

    def roll_dice(self):
        return randint(1, 6)
