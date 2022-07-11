from src.property.base import Property
from src.player import (
    BasePlayer,
    PlayerCautious,
    PlayerImpulsive,
    PlayerDemanding,
    PlayerRandom,
)


def factor_property(price: int = 0, position: int = 0, rent: int = 0, owner: BasePlayer = None):
    property = Property(
        price=price,
        position=position,
        rent=rent
    )

    if owner:
        property.owner = owner

    return property


def factor_player(class_type, balance: int = 0, id: int = 0):
    return class_type(
        balance=balance,
        id=id
    )


def factor_impulsive(balance: int = 0, id: int = 0) -> PlayerImpulsive:
    return factor_player(PlayerImpulsive, balance=balance, id=id)


def factor_cautious(balance: int = 0, id: int = 0) -> PlayerCautious:
    return factor_player(PlayerCautious, balance=balance, id=id)


def factor_demanding(balance: int = 0, id: int = 0) -> PlayerDemanding:
    return factor_player(PlayerDemanding, balance=balance, id=id)


def factor_random(balance: int = 0, id: int = 0) -> PlayerRandom:
    return factor_player(PlayerRandom, balance=balance, id=id)
