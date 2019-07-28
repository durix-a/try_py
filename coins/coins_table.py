from coins.coin_types import CoinTypes

class CoinsTable:
    max_coins_count = 7
    max_any_color_count = 5

    def __init__(self):
        self.coins_count = {
            CoinTypes.WHITE : CoinsTable.max_coins_count, 
            CoinTypes.BLUE : CoinsTable.max_coins_count, 
            CoinTypes.GREEN : CoinsTable.max_coins_count, 
            CoinTypes.RED : CoinsTable.max_coins_count, 
            CoinTypes.BLACK : CoinsTable.max_coins_count, 
            CoinTypes.ANY_COLOR : CoinsTable.max_any_color_count
        }

    def getCoinsCount(self, coin):
        return self.coins_count[coin]

    def takeCoins(self, coin, coins_count=1):
        assert((self.coins_count[coin] - coins_count) >= 0), "no more {0} coins".format(coin.name)
        self.coins_count[coin] -= coins_count

        return True

    def returnCoins(self, coin, coins_count=1):
        if coin == CoinTypes.ANY_COLOR:
            assert((self.coins_count[CoinTypes.ANY_COLOR] + coins_count) <= CoinsTable.max_any_color_count), "all ANY_COLOR coins are at table"
        assert((self.coins_count[coin] + coins_count) <= CoinsTable.max_coins_count), "all {0} coins are at table".format(coin.name)
        self.coins_count[coin] += coins_count

        return True

