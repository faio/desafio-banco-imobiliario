from .factor import (
    factor_random,
    factor_property
)


class TestRandomPlayer:

    def test_strategy(self):
        assert factor_random()._strategy == 'aleatorio'

    def test_rule_to_buy(self):
        """
        O jogador aleatório compra a propriedade que ele parar em cima com probabilidade de 50%..
        """
        property = factor_property(price=100, rent=30)
        player = factor_random(balance=200)

        return_true = False
        return_false = False

        # Para testar a escolha que é aleatória, eu procuro uma ocorrencia true uma false da verificação
        for i in range(0, 20):
            result = player.rule_to_buy(property)

            if result is True:
                return_true = True
            elif result is False:
                return_false = True

            if return_true is True and return_false is True:
                break

        assert return_true is True and return_false is True

    def test_pay_rent(self):
        owner = factor_random(balance=0)
        property = factor_property(price=100, rent=100, owner=owner)
        player = factor_random(balance=150)

        player.pay_rent(property)
        assert player.balance == 50
        assert player.is_alive() is True
        assert owner.balance == property.rent

        player.pay_rent(property)
        assert player.balance == -50
        assert player.is_alive() is False
        assert owner.balance == property.rent * 2
