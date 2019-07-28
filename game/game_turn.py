from cards.card import Card
from coins.coin_types import CoinTypes
from coins.coins_table import CoinsTable
from game.player import Player

class GameTurn:
    def __init__(self, taken_coins, taken_card):
        self.taken_coins = taken_coins
        self.taken_card = taken_card
        self.paid_coins_count = {
            CoinTypes.WHITE : 0, 
            CoinTypes.BLUE : 0, 
            CoinTypes.GREEN : 0, 
            CoinTypes.RED : 0, 
            CoinTypes.BLACK : 0, 
            CoinTypes.ANY_COLOR : 0
        }
    
    def getTakenCard(self):
        return self.taken_card

    def getTakenCoins(self):
        return self.taken_coins

    def payForPurchasedCard(self, player : Player, coins_table : CoinsTable):
        for coin in CoinTypes:
            if coin != CoinTypes.UNKNOWN and coin != CoinTypes.ANY_COLOR:
                assert(player.getMaxBuyPrice(coin) >= self.taken_card.getCost(coin)), "not enough coins ({0}) to buy card {1}".format(coin.name, self.taken_card)
                coins_to_pay = self.taken_card.getCost(coin) - player.getPurchasedCardsCount(coin)
                if coins_to_pay < 0:
                    coins_to_pay = 0
                    
                coins_remainder = player.getCoinsCount(coin) - coins_to_pay

                if coins_remainder < 0:
                    self.paid_coins_count[coin] = player.getCoinsCount(coin)
                    player.returnCoins(coin, player.getCoinsCount(coin))
                    coins_table.returnCoins(coin, player.getCoinsCount(coin))
                    self.paid_coins_count[coin] = -coins_remainder
                    player.returnCoins(CoinTypes.ANY_COLOR, -coins_remainder)
                    coins_table.returnCoins(CoinTypes.ANY_COLOR, -coins_remainder)
                else:
                    self.paid_coins_count[coin] = coins_to_pay
                    player.returnCoins(coin, coins_to_pay)
                    coins_table.returnCoins(coin, coins_to_pay)
                
    def returnPaymentForPurchasedCard(self, player : Player, coins_table : CoinsTable):
        for coin, coin_count in self.paid_coins_count.items():
            player.receiveCoins(coin, coin_count)
            self.paid_coins_count[coin] = 0
            coins_table.takeCoins(coin, coin_count)

    def getPaidCoinsCount(self, coinType):
        return self.paid_coins_count[coinType]

    def __str__(self):
        return "coins: {0}, cards: {1}".format(self.taken_coins, self.taken_card)

    def __repr__(self):
        returnedString = "< coins: "

        for coin_type in self.taken_coins:
            returnedString += "{0}, ".format(coin_type.name)
        return returnedString + " | card: " + self.taken_card.__repr__() + " >"

    def __eq__(self, other):
        if not isinstance(other, GameTurn):
            return NotImplemented

        return self.taken_coins == other.taken_coins and self.taken_card == other.taken_card

