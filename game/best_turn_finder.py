from game.player import Player
from game.game_turns_enumerator import GameTurnsEnumerator
from game.game_turn_validator import GameTurnValidator
from game.game_turn import GameTurn
from cards.cards_storage import CardsStorage
from cards.cards_table import CardsTable
from cards.cards_stack import CardsStack
from cards.card_level import CardLevel
from coins.coins_table import CoinsTable
from coins.coin_types import CoinTypes

class BestTurnFinder:
    def __init__(self):
        self.player = Player()
        cards_storage = CardsStorage()
        stack_level1 = CardsStack(CardLevel.ONE, cards_storage.cards_storage)
        stack_level2 = CardsStack(CardLevel.TWO, cards_storage.cards_storage)
        stack_level3 = CardsStack(CardLevel.THREE, cards_storage.cards_storage)
        self.cards_table = CardsTable(stack_level1, stack_level2, stack_level3)
        self.coins_table = CoinsTable()
        self.turn_validator = GameTurnValidator()
        self.turns_enumerator = GameTurnsEnumerator(self.coins_table, self.cards_table)
        self.current_turns_sequence = []
        self.best_turns_sequence = []
        self.best_turns_sequence_points = 0

    def __updateBestTurnsSequence(self):
        current_turns_sequence_points = 0

        for turn in self.current_turns_sequence:
            taken_card = turn.getTakenCard()
            if taken_card:
                current_turns_sequence_points += taken_card.points
        
        if current_turns_sequence_points > self.best_turns_sequence_points:
            self.best_turns_sequence_points = current_turns_sequence_points
            self.best_turns_sequence = self.current_turns_sequence.copy()
            print("best {0} turns. points {1}".format(len(self.best_turns_sequence), self.best_turns_sequence_points))

    def enumerateAllValidTurns(self):
        turns = self.turns_enumerator.enumerateAllPossibleTurns()
        valid_turns = []
        for turn in turns:
            if self.turn_validator.isTurnValid(turn, self.player):
                valid_turns.append(turn)

        return valid_turns

    def findTurnsHighestValueSequenceWithPrecalculatedBegginng(self, sequenceLength, valid_turns):
        for turn in valid_turns:
            self.__playerTakeTurn(turn)
            self.current_turns_sequence.append(turn)
        
        self.findHighestValueTurnsSequence(sequenceLength - 1)

        for turn in valid_turns:
            self.__playerUndoTurn(turn)
            self.current_turns_sequence.pop()

    def findHighestValueTurnsSequence(self, sequenceLength):
        if sequenceLength == 0:
            self.__updateBestTurnsSequence()
            return
        
        valid_turns = self.enumerateAllValidTurns()
        
        if(sequenceLength >= 8):
            print("enumerated {0} valid turns. sequence {1}".format(len(valid_turns), sequenceLength))

        for turn in valid_turns:
            self.__playerTakeTurn(turn)
            self.current_turns_sequence.append(turn)
            self.findHighestValueTurnsSequence(sequenceLength - 1)
            self.__playerUndoTurn(turn)
            self.current_turns_sequence.pop()
    
    def __playerTakeTurn(self, turn : GameTurn):
        for coin in turn.getTakenCoins():
            self.coins_table.takeCoins(coin)
            self.player.receiveCoins(coin)

        if turn.getTakenCard():
            takken_card = turn.getTakenCard()
            self.cards_table.takeCard(takken_card)
            turn.payForPurchasedCard(self.player, self.coins_table)
            self.player.receivePurchasedCard(takken_card)

    def __playerUndoTurn(self, turn):
        for coin in turn.getTakenCoins():
            self.coins_table.returnCoins(coin)
            self.player.returnCoins(coin)

        if turn.getTakenCard():
            self.player.returnPurchasedCard(turn.getTakenCard())
            turn.returnPaymentForPurchasedCard(self.player, self.coins_table)
            self.cards_table.undoTakeCard()

