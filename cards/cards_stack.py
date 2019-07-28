from cards.card import Card
import random


class CardsStack:

    def __init__(self, _stack_level, _cards=[]):
        self.top_card_index = 0
        self.stack_level = _stack_level
        self.setCards(_cards)

    def setCards(self, _cards):
        self.cards = []

        for card in _cards:
            if not isinstance(card, Card) or card.level != self.stack_level:
                continue

            self.cards.append(card)

    def shuffleCards(self):
        cards = self.cards
        self.cards = []

        while(cards):
            random_index = random.randint(0, len(cards) - 1)
            self.cards.append(cards[random_index])
            del cards[random_index]

    def getTopCard(self):
        if self.top_card_index < len(self.cards):
            return self.cards[self.top_card_index]
        else:
            return False

    def popCard(self):
        assert (len(self.cards) > 0), "Can't pop card from empty stack"
        assert ((self.top_card_index + 1) <= len(self.cards)), "Last card have already been popped - can't pop cards any more"

        self.top_card_index += 1
        return self.cards[self.top_card_index - 1]

    def restoreCard(self):
        assert (len(self.cards) > 0), "Can't restore card in empty stack"
        assert (self.top_card_index > 0), "Last card have already been restored - can't restore cards any more"
        self.top_card_index -= 1

    def getCardsCount(self):
        return len(self.cards)

    def getTopCardIndex(self):
        return self.top_card_index

    def getStackLevel(self):
        return self.stack_level

    def isStackEmpty(self):
        return self.top_card_index == len(self.cards)

    def isStackFull(self):
        return self.top_card_index == 0

    def __eq__(self, other):
        if not isinstance(other, CardsStack):
            return NotImplemented

        return self.top_card_index == other.top_card_index and \
            self.stack_level == other.stack_level and \
            self.cards == other.cards


