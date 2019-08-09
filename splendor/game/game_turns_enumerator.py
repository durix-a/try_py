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
        self.possible_turns += self.__getThreeCoinsTurns()

        oneTwoCoinsTurn = self.__getOneTwoCoinsTurn()
        if oneTwoCoinsTurn:
            self.possible_turns.append(oneTwoCoinsTurn)

    def __getThreeCoinsTurns(self):
        possible_turns = []
        all_coins_list = []

        for coin in CoinTypes:
            if coin != CoinTypes.UNKNOWN and coin != CoinTypes.ANY_COLOR:
                all_coins_list.append(coin)
        
        for firstCoinIndex in range(0, len(all_coins_list)):
            firstCoin = all_coins_list[firstCoinIndex]

            if self.coins_table.getCoinsCount(firstCoin) == 0:
                continue
            
            for secondCoinIndex in range(firstCoinIndex + 1, len(all_coins_list)):
                secondCoin = all_coins_list[secondCoinIndex]

                if secondCoin == firstCoin:
                    continue
                
                if self.coins_table.getCoinsCount(secondCoin) == 0:
                    continue
            
                for thirdCoinIndex in range(secondCoinIndex + 1, len(all_coins_list)):
                    thirdCoin = all_coins_list[thirdCoinIndex]

                    if thirdCoin == secondCoin or thirdCoin == firstCoin:
                        continue
                    
                    if self.coins_table.getCoinsCount(thirdCoin) == 0:
                        continue
            
                    possible_turns.append(GameTurn([firstCoin, secondCoin, thirdCoin], None))
        
        return possible_turns
    
    def __getOneTwoCoinsTurn(self):
        availableCoins = []

        for firstCoin in CoinTypes:
            if firstCoin == CoinTypes.UNKNOWN or self.coins_table.getCoinsCount(firstCoin) == 0:
                continue
            
            availableCoins.append(firstCoin)
        
        if len(availableCoins) == 1:
            return GameTurn([availableCoins[0]], None)
        if len(availableCoins) == 2:
            return GameTurn([availableCoins[0], availableCoins[1]], None)
        
        return None

    def __enumerateTakeCardsTurns(self):
        for card_level in CardLevel:
            if card_level != CardLevel.UNKNOWN:
                for open_card_index in range(CardsTable.open_cards_count):
                    card = self.cards_table.getCard(card_level, open_card_index)
                    if card:
                        self.possible_turns.append(GameTurn([], card))

