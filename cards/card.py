from cards.card_level import CardLevel
from coins.coin_types import CoinTypes

class Card:

    def __init__(self, white_cost=0, blue_cost=0, green_cost=0, red_cost=0, black_cost=0, level=CardLevel.UNKNOWN, points=0, discount=CoinTypes.UNKNOWN):
        self.card_cost = {
            CoinTypes.WHITE : int(white_cost), 
            CoinTypes.BLUE : int(blue_cost), 
            CoinTypes.GREEN : int(green_cost), 
            CoinTypes.RED : int(red_cost), 
            CoinTypes.BLACK : int(black_cost)
        }

        self.level = level
        self.points = int(points)
        self.discount = discount
    
    def getCost(self, coin):
        return self.card_cost[coin]

    def __str__(self):
        returnedString = ""

        for coin_type, cost in self.card_cost.items():
            returnedString += "{0}: {1}, ".format(coin_type.name, cost)
        return returnedString + "level:{0}, points:{1}, discount:{2}".format(self.level, self.points, self.discount.name)

    def __repr__(self):
        returnedString = ""

        for coin_type, cost in self.card_cost.items():
            returnedString += "{0}: {1}, ".format(coin_type.name[0], cost)
        return returnedString + " | l:{0}, p:{1}, d:{2}".format(self.level, self.points, self.discount.name[:3])

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented

        return self.card_cost == other.card_cost and self.level == other.level and \
            self.points == other.points and self.discount == other.discount
