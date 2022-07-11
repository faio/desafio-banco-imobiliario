from .factor import (
    factor_impulsive,
    factor_property
)


class TestImpulsivePlayer:

    def test_strategy(self):
        assert factor_impulsive()._strategy == 'impulsivo'

    def test_rule_to_buy(self):
        assert factor_impulsive().rule_to_buy(factor_property()) is True

    def test_buy(self):
        """
        Verificando a regra de compra do jogador impulsivo

        Regra: O jogador impulsivo compra qualquer propriedade sobre a qual ele parar
        """

        property = factor_property(price=100)
        player = factor_impulsive(balance=150)

        assert player.properties == []
        player.buy(property)
        assert len(player.properties) == 1

        # Sem saldo ele não pode comprar outra propriedade
        property = factor_property(price=160)
        player.buy(property)
        assert len(player.properties) == 1

        assert player.balance == 50
        assert player.is_alive() is True

    def test_pay_rent(self):
        owner = factor_impulsive(balance=0)
        property = factor_property(price=100, rent=100, owner=owner)
        player = factor_impulsive(balance=150)

        player.pay_rent(property)
        assert player.balance == 50
        assert player.is_alive() is True
        assert owner.balance == property.rent

        player.pay_rent(property)
        assert player.balance == -50
        assert player.is_alive() is False
        assert owner.balance == property.rent * 2
