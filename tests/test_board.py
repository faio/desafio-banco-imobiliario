import pytest

from src import settings
from src.board import Board
from collections import Counter
from .players.factor import factor_impulsive


def test_create_params():

    board = Board()
    assert board.players == []
    assert board.properties == []
    assert board.losers_players == []
    assert board.winner is None
    assert board.current_round == 0


def test_roll_dict() -> None:
    """ Verificando se os valores realmente são aleatorios """

    board = Board()

    values = Counter(board.roll_dice() for i in range(0, 100))

    # O dado tem o valor de 1 a 6, portanto, tem que ter 6 chaves
    assert len(values) == 6

    # Tem que ter os 6 valores nos retornos
    for i in range(1, 7):
        values[i]


def test_create_random_players():
    """
    Validando se os players estão realmente sendo criados em ordem aleatorio e
    com os valores corretos
    """

    board = Board()
    board.create_random_players()
    players = board.players

    assert len(players) == 4
    is_random = False
    # Rodo algumas interações e verifico se a ordem foi aleatorio
    for i in range(0, 100):
        board.create_random_players()

        is_random = board.players[0].__class__ == players[0].__class__
        if is_random:
            break

        players = board.players

    assert is_random is True

    assert all(p.balance == settings.INITIAL_BALANCE for p in players) is True

    assert len(Counter(p.id for p in players)) == 4


def test_create_properties():
    """
    Validando a criação das propriedades e os seus valores
    """
    board = Board()
    board.create_properties()

    assert len(board.properties) == settings.PROPERTY_MAX_QTD

    assert len(board.properties) == settings.PROPERTY_MAX_QTD

    for property in board.properties:
        assert property.price in range(settings.PROPERTY_MIN_PRICE, settings.PROPERTY_MAX_PRICE + 1)
        assert property.rent in range(settings.PROPERTY_MIN_RENT, settings.PROPERTY_MAX_RENT + 1)
        assert property.position in range(1, settings.PROPERTY_MAX_QTD + 1)

    # Verificando se os ids são diferentes
    counter_properties = Counter(p.position for p in board.properties)
    assert len(counter_properties) == settings.PROPERTY_MAX_QTD


def test_walk():
    board = Board()
    board.create_random_players()

    player = factor_impulsive(balance=settings.INITIAL_BALANCE)
    assert player.position == 0

    with pytest.raises(RuntimeError):
        board.walk(player)

    assert player.position == 0

    # Após criar as propriedades, deve conseguir avançar no jogo
    board.create_properties()
    board.walk(player)
    assert player.position > 0  # Verificando se andou
    assert player.position <= 6  # Verificando se não está avançando mais de 6 casas

    # Validando se ao chegar na ultima casa está adicionando o saldo
    assert player.balance == settings.INITIAL_BALANCE
    player.position = settings.PROPERTY_MAX_QTD
    board.walk(player)
    assert player.balance == settings.INITIAL_BALANCE + 100


def test_pay_property():
    board = Board()
    board.create_random_players()
    board.create_properties()

    # Movendo o jogador
    player = factor_impulsive(balance=settings.INITIAL_BALANCE)
    player.position = 5
    property = board.properties[4]

    assert property.available is True
    assert player.properties == []
    assert player.balance == settings.INITIAL_BALANCE

    # Deve comprar a propriedade
    board.pay_property(player)
    assert len(player.properties) == 1
    assert player.balance == settings.INITIAL_BALANCE - property.price

    # Imóvel já é desse proprietario, portanto, não pode ter alterado o saldo
    board.pay_property(player)
    assert len(player.properties) == 1
    assert player.balance == settings.INITIAL_BALANCE - property.price

    player_2 = board.players[1]
    assert player_2.properties == []
    assert player_2.balance == settings.INITIAL_BALANCE

    player_2.position = 5
    # Quando cai em um imóvel já comprado, precisa pagar o aluguel
    board.pay_property(player_2)
    assert player_2.balance == settings.INITIAL_BALANCE - property.rent
    assert player_2.properties == []


def test_remove_loser():
    board = Board()
    board.create_random_players()
    board.create_properties()
    player = board.players[0]
    property = board.properties[0]

    assert player.balance == settings.INITIAL_BALANCE

    player._add_property(property)
    player.balance = -50

    assert player.is_alive() is False
    assert len(player.properties) == 1
    assert property.owner is player

    board.remove_loser(player)

    assert player.is_alive() is False
    assert player.balance == -50
    assert len(board.players) == 3
    assert len(board.losers_players) == 1


def test_play():
    board = Board()
    board.play()

    if board.current_round != settings.MAX_ROUND:
        assert len(board.players) in (0, 1)
        assert len(board.losers_players) != 0

    assert len(board.players) + len(board.losers_players) == 4
    assert len(board.properties) == settings.PROPERTY_MAX_QTD
    assert board.current_round > 0
    assert board.winner is not None
