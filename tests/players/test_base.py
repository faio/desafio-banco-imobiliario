from random import randint
from src import settings
from pytest import raises


from .factor import (
    factor_cautious,
    factor_demanding,
    factor_impulsive,
    factor_random,
    factor_property
)


class TestBasePlayer:

    def test_create_all_type(self):
        factor_impulsive()
        factor_cautious()
        factor_demanding()
        factor_random()

    def test_create_params(self):
        balance = 100
        id = 99

        impulsive = factor_impulsive(balance, id)
        cautious = factor_cautious(balance, id)
        demanding = factor_demanding(balance, id)
        random = factor_random(balance, id)

        assert impulsive.balance == balance
        assert impulsive.id == id
        assert impulsive.position == 0
        assert impulsive.properties == []
        assert impulsive._strategy == 'impulsivo'

        assert cautious.balance == balance
        assert cautious.id == id
        assert cautious.position == 0
        assert cautious.properties == []
        assert cautious._strategy == 'cauteloso'

        assert demanding.balance == balance
        assert demanding.id == id
        assert demanding.position == 0
        assert demanding.properties == []
        assert demanding._strategy == 'exigente'

        assert random.balance == balance
        assert random.id == id
        assert random.position == 0
        assert random.properties == []
        assert random._strategy == 'aleatorio'

    def test_equals_player(self):

        impulsive = factor_impulsive(id=1)
        impulsive_2 = factor_impulsive(id=2)
        cautious = factor_cautious(id=1)
        cautious_2 = factor_cautious(id=2)

        assert impulsive != impulsive_2
        assert impulsive != cautious_2
        assert impulsive == cautious
        assert impulsive == impulsive

        assert cautious != impulsive_2
        assert cautious != cautious_2
        assert cautious == impulsive
        assert cautious == cautious

    def test_id(self):
        id = 10

        player = factor_random(id=id)
        assert player.id == id

        with raises(ValueError) as e:
            player.id = id

        assert str(e.value) == "O ID não pode ser alterado"

    def test_balance(self):
        balance = randint(0, settings.INITIAL_BALANCE)
        str_msg = "O saldo para atribuição precisa ser um valor númerico interio"
        player = factor_random(balance=balance)
        assert player.balance == balance

        with raises(ValueError) as e:
            player.balance = "dasdasdas"

        assert str(e.value) == str_msg

        with raises(ValueError) as e:
            player.balance = 10.5

        assert str(e.value) == str_msg

    def test_add_property(self):
        property = factor_property()
        player = factor_random()

        assert player.properties == []

        player._add_property(property)

        assert len(player.properties) == 1
        assert player == property.owner

    def test_is_alive(self):
        property = factor_property(rent=100, owner=factor_cautious())
        player = factor_impulsive(balance=60)

        assert player.is_alive() is True
        player.pay_rent(property)
        assert player.is_alive() is False

    def test_is_can_buy(self):
        property = factor_property(price=100)
        balance = 50

        impulsive = factor_impulsive(balance, 1)
        cautious = factor_cautious(balance, 2)
        demanding = factor_demanding(balance, 3)
        random = factor_random(balance, 4)
        owner = factor_cautious()

        # Quando o saldo é a abaixo do valor do valor de compra, não pode comprar o imóvel
        assert impulsive.is_can_buy(property) is False
        assert cautious.is_can_buy(property) is False
        assert demanding.is_can_buy(property) is False
        assert random.is_can_buy(property) is False

        # Se o valor dor menor ou igual ao saldo atual, pode comprar
        for balance in [100, 150]:
            impulsive.balance = balance
            cautious.balance = balance
            demanding.balance = balance
            random.balance = balance

            assert impulsive.is_can_buy(property) is True
            assert cautious.is_can_buy(property) is True
            assert demanding.is_can_buy(property) is True
            assert random.is_can_buy(property) is True

        # Imóvel com dono não pode ser comprado
        property.owner = owner
        assert impulsive.is_can_buy(property) is False
        assert cautious.is_can_buy(property) is False
        assert demanding.is_can_buy(property) is False
        assert random.is_can_buy(property) is False
