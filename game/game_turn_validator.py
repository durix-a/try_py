from game.game_turn import GameTurn
from game.player import Player
from coins.coin_types import CoinTypes
from cards.card import Card
from coins.coins_table import CoinsTable

class GameTurnValidator:
    max_coins_per_player = 10

    def isTurnValid(self, turn : GameTurn, player : Player):
        if turn.getTakenCard():
            return self.__canPlayerTakeCoins(turn.getTakenCoins(), player) and self.__canPlayerBuyCard(player, turn.getTakenCard())
        else:
            return self.__canPlayerTakeCoins(turn.getTakenCoins(), player)
    
    def __canPlayerTakeCoins(self, coins, player : Player):
        if (player.getAllCoinsCount() + len(coins)) > GameTurnValidator.max_coins_per_player:
            return False

        return True
        
    def __canPlayerBuyCard(self, player : Player, card : Card):
        all_coins_list = []
        for coin in CoinTypes:
            if coin != CoinTypes.UNKNOWN and coin != CoinTypes.ANY_COLOR:
                all_coins_list.append(coin)

        for coin in all_coins_list:
            if player.getMaxBuyPrice(coin) < card.getCost(coin):
                return False
        
        return True
    
    def canPlayerSaveCard(self, turn : GameTurn, player : Player, coins_table : CoinsTable):
        if self.__canPlayerBuyCard(player, turn.getTakenCard()) or not self.__canPlayerTakeCoins([CoinTypes.ANY_COLOR], player):
            return False

        return coins_table.getCoinsCount(CoinTypes.ANY_COLOR) > 0

        

