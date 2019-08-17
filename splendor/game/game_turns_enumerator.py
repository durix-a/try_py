import itertools
from cards.card import Card
from cards.cards_table import CardsTable
from cards.card_level import CardLevel
from coins.coin_types import CoinTypes
from coins.coins_table import CoinsTable
from game.game_turn import GameTurn
from game.player import Player


class GameTurnsEnumerator:
    def __init__(self, coins_table, cards_table):
        self.coins_table = coins_table
        self.cards_table = cards_table
        self.possible_turns = []

    def enumerateAllPossibleTurns(self):
        self.possible_turns = []
        self.__enumerateTakeCoinsTurns()
        self.__enumerateTakeCardsTurns()
        return self.possible_turns

    def __enumerateTakeCoinsTurns(self):
        availableCoins = self.coins_table.getAvailableCoins(1)
        if len(availableCoins) > 3:
            treeCoinsCombinations = itertools.combinations(availableCoins, 3)
            self.possible_turns += map(lambda x: GameTurn(x, None), treeCoinsCombinations)
        else:
            self.possible_turns.append(GameTurn(availableCoins, None))
    
    def __enumerateTakeCardsTurns(self):
        self.possible_turns += map(lambda card: GameTurn((), card), self.cards_table.getAllOpenCards())

