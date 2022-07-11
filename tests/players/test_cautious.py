from .factor import (
    factor_cautious,
    factor_property
)


class TestCautiousPlayer:

    def test_strategy(self):
        assert factor_cautious()._strategy == 'cauteloso'

    def test_rule_to_buy(self):
        """
        Jogador cauteloso compra qualquer propriedade desde que ele tenha uma reserva de 80
        saldo sobrando depois de realizada a compra.
        """
        property = factor_property(price=100)
        player = factor_cautious(balance=200)

        assert player.rule_to_buy(property) is True

        player.balance = 180
        assert player.rule_to_buy(property) is True

        player.balance = 100
        assert player.rule_to_buy(property) is False

        player.balance = 80
        assert player.rule_to_buy(property) is False

    def test_buy(self):
        """
        Verificando a regra de compra do jogador cauteloso

        Regra: jogador cauteloso compra qualquer propriedade desde que ele tenha uma reserva de 80
        saldo sobrando depois de realizada a compra.
        """

        property = factor_property(price=100)
        player = factor_cautious(balance=200)

        assert player.properties == []
        player.buy(property)
        assert len(player.properties) == 1
        assert player.is_alive() is True

        # Sem saldo ele não pode comprar outra propriedade
        property = factor_property(price=160)
        player.buy(property)
        assert len(player.properties) == 1

        assert player.balance == 100
        assert player.is_alive() is True

        property = factor_property(price=60)
        player.buy(property)
        assert len(player.properties) == 1

        property = factor_property(price=20)
        player.buy(property)
        assert len(player.properties) == 2

    def test_pay_rent(self):
        owner = factor_cautious(balance=0)
        property = factor_property(price=100, rent=100, owner=owner)
        player = factor_cautious(balance=150)

        player.pay_rent(property)
        assert player.balance == 50
        assert player.is_alive() is True
        assert owner.balance == property.rent

        player.pay_rent(property)
        assert player.balance == -50
        assert player.is_alive() is False
        assert owner.balance == property.rent * 2
