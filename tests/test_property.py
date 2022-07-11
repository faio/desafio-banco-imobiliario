from random import randint
from src.property.base import Property
from src.player import PlayerImpulsive
from src import settings
from pytest import raises


def factor_property(price: int = 0, position: int = 0, rent: int = 0):
    return Property(
        price=price,
        position=position,
        rent=rent
    )


def factor_owner_impulsive(balance: int = 0, id: int = 0):
    return PlayerImpulsive(
        balance=0,
        id=0
    )


def test_create_params():
    property = factor_property()

    assert property.price == 0
    assert property.position == 0
    assert property.rent == 0
    assert property._owner is None


def test_available():
    property = factor_property()

    assert property.available is True

    property.owner = factor_owner_impulsive()
    assert property.available is False


def test_price():
    price = randint(settings.PROPERTY_MIN_PRICE, settings.PROPERTY_MAX_PRICE)
    property = factor_property(price=price)

    assert property.price == price

    with raises(ValueError) as e:
        property.price = price

    assert str(e.value) == 'Não se pode alterar o preço da propriedade'


def test_position():
    position = randint(0, settings.PROPERTY_MAX_QTD)
    property = factor_property(position=position)

    assert property.position == position

    with raises(ValueError) as e:
        property.position = position

    assert str(e.value) == 'Não se pode alterar a posição da propriedade'


def test_rent():
    rent = randint(settings.PROPERTY_MIN_RENT, settings.PROPERTY_MIN_RENT)
    property = factor_property(rent=rent)

    assert property.rent == rent

    with raises(ValueError) as e:
        property.rent = rent

    assert str(e.value) == 'Não se pode alterar o valor do aluguel da propriedade'


def test_owner():
    owner_1 = factor_owner_impulsive(id=1)
    owner_2 = factor_owner_impulsive(id=2)

    property = factor_property()
    property.owner = owner_1

    assert property.owner == owner_1

    property.owner = owner_2
    assert property.owner == owner_2
