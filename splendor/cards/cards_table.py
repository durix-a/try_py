from cards.card import Card
from cards.cards_stack import CardsStack
from cards.cards_storage import CardsStorage


class CardsTable:

    class TakenCardHistoryRecord:
        def __init__(self, taken_card, open_card_index):
            self.taken_card = taken_card
            self.open_card_index = open_card_index

    open_cards_count = 4

    def __init__(self, _cards_stack_level1, _cards_stack_level2, _cards_stack_level3):
        self.closed_cards = [_cards_stack_level1, _cards_stack_level2, _cards_stack_level3]
        self.open_cards = [[], [], []]
        self.taken_cards_history = []

        cards_left = CardsTable.open_cards_count
        while(cards_left):
            for level in range(CardsStorage.cards_levels_count):
                self.open_cards[level].append(self.closed_cards[level].popCard())
            cards_left -= 1

    def getCard(self, card_level, open_card_index):
        return self.open_cards[card_level - 1][open_card_index]

    def getAllOpenCards(self):
        return [card for card in (self.open_cards[0] + self.open_cards[1] + self.open_cards[2]) if card]

    def takeCard(self, takkenCard : Card):
        card_index = 0
        for card in self.open_cards[takkenCard.level - 1]:
            if card == takkenCard:
                return self.takeCardByIndex(takkenCard.level, card_index)

            card_index += 1

    def takeCardByIndex(self, card_level, open_card_index):
        card_level -= 1
        taken_card = self.open_cards[card_level][open_card_index]

        if self.closed_cards[card_level].isStackEmpty():
            self.open_cards[card_level][open_card_index] = None
        else:
            self.open_cards[card_level][open_card_index] = self.closed_cards[card_level].popCard()
        
        if taken_card:
            self.taken_cards_history.append(CardsTable.TakenCardHistoryRecord(taken_card, open_card_index))
        
        return taken_card

    def undoTakeCard(self):
        last_taken_card_record_index = len(self.taken_cards_history) - 1
        last_taken_card_record = self.taken_cards_history[last_taken_card_record_index]
        last_taken_card = last_taken_card_record.taken_card
        last_taken_card_level_index = last_taken_card.level - 1
        del self.taken_cards_history[last_taken_card_record_index]
        card_at_last_taken_index = self.open_cards[last_taken_card_level_index][last_taken_card_record.open_card_index]
        restored_card_stack = self.closed_cards[last_taken_card_level_index]

        if card_at_last_taken_index:
            restored_card_stack.restoreCard()
            assert(card_at_last_taken_index == restored_card_stack.getTopCard()), "restoring wrong card, card on table {0}, restored {1}".format(card_at_last_taken_index, restored_card_stack.getTopCard())
        
        self.open_cards[last_taken_card_level_index][last_taken_card_record.open_card_index] = last_taken_card

    def __eq__(self, other):
        if not isinstance(other, CardsTable):
            return NotImplemented

        return self.closed_cards == other.closed_cards and \
            self.open_cards == other.open_cards

