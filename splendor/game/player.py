from coins.coin_types import CoinTypes
from cards.card import Card

class Player:
    max_coins_count = 10

    def __init__(self):
        self.coins_count = {
            CoinTypes.WHITE : 0, 
            CoinTypes.BLUE : 0, 
            CoinTypes.GREEN : 0, 
            CoinTypes.RED : 0, 
            CoinTypes.BLACK : 0, 
            CoinTypes.ANY_COLOR : 0
        }

        self.purchased_cards = {
            CoinTypes.WHITE : [], 
            CoinTypes.BLUE : [], 
            CoinTypes.GREEN : [], 
            CoinTypes.RED : [], 
            CoinTypes.BLACK : [], 
            CoinTypes.ANY_COLOR : []
        }

        self.saved_cards = []

    def receivePurchasedCard(self, card : Card):
        self.purchased_cards[card.discount].append(card)

    def getPurchasedCardsCount(self, discountCoin):
        return len(self.purchased_cards[discountCoin])

    def getPurchasedCard(self, discountCoin, cardIndex):
        return self.purchased_cards[discountCoin][cardIndex]

    def returnPurchasedCard(self, card : Card):
        self.purchased_cards[card.discount].remove(card)

    def receiveSavedCard(self, card : Card):
        self.saved_cards.append(card)

    def getSavedCardsCount(self):
        return len(self.saved_cards)

    def getSavedCard(self, cardIndex):
        return self.saved_cards[cardIndex]

    def getAllCoinsCount(self):
        total_coins_count = 0
        for coin_count in self.coins_count.values():
            total_coins_count += coin_count
        
        return total_coins_count

    def receiveCoins(self, coin, coins_count=1):
        assert((self.getAllCoinsCount() + coins_count) <= Player.max_coins_count), "player can't take more than {0} coins".format(Player.max_coins_count)
        self.coins_count[coin] += coins_count

    def getCoinsCount(self, coinType):
        return self.coins_count[coinType]

    def getMaxBuyPrice(self, coinType):
        return self.coins_count[coinType] + len(self.purchased_cards[coinType]) + self.coins_count[CoinTypes.ANY_COLOR]

    def returnCoins(self, coin, coins_count=1):
        assert((self.coins_count[coin] - coins_count) >= 0), "player doesn't have any more {0} coins".format(coin.name)
        self.coins_count[coin] -= coins_count

