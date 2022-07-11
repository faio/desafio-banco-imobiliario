from .factor import (
    factor_demanding,
    factor_property
)


class TestCautiousPlayer:

    def test_strategy(self):
        assert factor_demanding()._strategy == 'exigente'

    def test_rule_to_buy(self):
        """
        O jogador exigente compra qualquer propriedade, desde que o valor do aluguel dela seja maior do que 50.
        saldo sobrando depois de realizada a compra.
        """
        property = factor_property(price=100, rent=30)
        player = factor_demanding(balance=200)

        assert player.rule_to_buy(property) is False

        property = factor_property(price=100, rent=50)
        assert player.rule_to_buy(property) is False

        property = factor_property(price=100, rent=51)
        assert player.rule_to_buy(property) is True

    def test_buy(self):
        """
        Verificando a regra de compra do jogador cauteloso

        Regra: O jogador exigente compra qualquer propriedade, desde que o valor do aluguel dela seja maior do que 50.
        """

        property = factor_property(price=100, rent=100)
        player = factor_demanding(balance=200)

        assert player.properties == []
        player.buy(property)
        assert len(player.properties) == 1
        assert player.is_alive() is True

        # Sem saldo ele não pode comprar outra propriedade
        property = factor_property(price=160, rent=60)
        player.buy(property)
        assert len(player.properties) == 1

        # Aluguel abaixo de 50 ele não pode comprar
        property = factor_property(price=160, rent=40)
        player.buy(property)
        assert len(player.properties) == 1

        assert player.balance == 100
        assert player.is_alive() is True

    def test_pay_rent(self):
        owner = factor_demanding(balance=0)
        property = factor_property(price=100, rent=100, owner=owner)
        player = factor_demanding(balance=150)

        player.pay_rent(property)
        assert player.balance == 50
        assert player.is_alive() is True
        assert owner.balance == property.rent

        player.pay_rent(property)
        assert player.balance == -50
        assert player.is_alive() is False
        assert owner.balance == property.rent * 2
