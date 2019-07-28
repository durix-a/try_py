import unittest
from cards.cards_storage import CardsStorage
from cards.card import Card
from cards.cards_stack import CardsStack
from cards.cards_table import CardsTable
from cards.card_level import CardLevel
from coins.coin_types import CoinTypes


class TestCards(unittest.TestCase):
    def setUp(self):
        self.cards = CardsStorage()
        self.level1_stack = CardsStack(1, self.cards.cards_storage)
        self.level2_stack = CardsStack(2, self.cards.cards_storage)
        self.level3_stack = CardsStack(3, self.cards.cards_storage)
        self.level1_cumulative_cost = 33
        self.level2_cumulative_cost = 41
        self.level3_cumulative_cost = 43
        self.level1_cards_count = 40
        self.level2_cards_count = 30
        self.level3_cards_count = 20

        self.cards_db = [Card(blue_cost=3, level=CardLevel.ONE, discount=CoinTypes.WHITE), Card(red_cost=3, level=CardLevel.ONE, discount=CoinTypes.BLUE),
                         Card(white_cost=3, level=CardLevel.ONE, discount=CoinTypes.WHITE), Card(green_cost=3, level=CardLevel.ONE, discount=CoinTypes.BLUE),
                         Card(green_cost=3, level=CardLevel.ONE, discount=CoinTypes.GREEN), Card(red_cost=3, level=CardLevel.ONE, discount=CoinTypes.RED),
                         Card(black_cost=3, level=CardLevel.ONE, discount=CoinTypes.BLACK), Card(black_cost=3, level=CardLevel.ONE, discount=CoinTypes.GREEN),

                         Card(blue_cost=2, green_cost=2, level=CardLevel.TWO, discount=CoinTypes.WHITE), Card(white_cost=2, green_cost=2, level=CardLevel.TWO, discount=CoinTypes.BLUE),
                         Card(red_cost=2, black_cost=2, level=CardLevel.TWO, discount=CoinTypes.GREEN), Card(white_cost=2, blue_cost=2, level=CardLevel.TWO, discount=CoinTypes.BLACK),
                         Card(blue_cost=2, red_cost=2, level=CardLevel.TWO, discount=CoinTypes.RED), Card(white_cost=2, red_cost=2, level=CardLevel.TWO, discount=CoinTypes.WHITE),
                         Card(green_cost=2, black_cost=2, level=CardLevel.TWO, discount=CoinTypes.GREEN), Card(white_cost=2, black_cost=2, level=CardLevel.TWO, discount=CoinTypes.BLACK),

                         Card(white_cost=2, blue_cost=4, level=CardLevel.THREE, discount=CoinTypes.WHITE), Card(white_cost=2, green_cost=4, level=CardLevel.THREE, discount=CoinTypes.BLUE),
                         Card(white_cost=2, red_cost=4, level=CardLevel.THREE, discount=CoinTypes.GREEN), Card(white_cost=2, black_cost=4, level=CardLevel.THREE, discount=CoinTypes.RED),
                         Card(blue_cost=2, green_cost=4, level=CardLevel.THREE, discount=CoinTypes.WHITE), Card(blue_cost=2, red_cost=4, level=CardLevel.THREE, discount=CoinTypes.BLACK),
                         Card(blue_cost=2, black_cost=4, level=CardLevel.THREE, discount=CoinTypes.BLUE), Card(red_cost=2, green_cost=4, level=CardLevel.THREE, discount=CoinTypes.GREEN)]
        self.cards_stack_lvl1 = CardsStack(1, self.cards_db)
        self.cards_stack_lvl2 = CardsStack(2, self.cards_db)
        self.cards_stack_lvl3 = CardsStack(3, self.cards_db)

    def test_cards_table(self):
        self.cards_table = CardsTable(self.cards_stack_lvl1, self.cards_stack_lvl2, self.cards_stack_lvl3)
        self.assertEqual(self.cards_db[0], self.cards_table.getCard(1, 0))
        self.assertEqual(self.cards_db[1], self.cards_table.getCard(1, 1))
        self.assertEqual(self.cards_db[9], self.cards_table.getCard(2, 1))
        self.assertEqual(self.cards_db[10], self.cards_table.getCard(2, 2))
        self.assertEqual(self.cards_db[18], self.cards_table.getCard(3, 2))
        self.assertEqual(self.cards_db[19], self.cards_table.getCard(3, 3))

        self.assertEqual(self.cards_db[0], self.cards_table.takeCardByIndex(1, 0))
        self.assertEqual(self.cards_db[4], self.cards_table.takeCardByIndex(1, 0))
        self.assertEqual(self.cards_db[5], self.cards_table.getCard(1, 0))

        self.assertEqual(self.cards_db[11], self.cards_table.takeCardByIndex(2, 3))
        self.assertEqual(self.cards_db[10], self.cards_table.takeCardByIndex(2, 2))
        self.assertEqual(self.cards_db[9], self.cards_table.takeCardByIndex(2, 1))
        self.assertEqual(self.cards_db[8], self.cards_table.takeCardByIndex(2, 0))
        self.assertEqual(self.cards_db[12], self.cards_table.takeCardByIndex(2, 3))
        self.assertEqual(self.cards_db[13], self.cards_table.takeCardByIndex(2, 2))
        self.assertEqual(self.cards_db[14], self.cards_table.takeCardByIndex(2, 1))
        self.assertEqual(self.cards_db[15], self.cards_table.takeCardByIndex(2, 0))
        self.assertEqual(None, self.cards_table.takeCardByIndex(2, 3))
        self.assertEqual(None, self.cards_table.takeCardByIndex(2, 2))
        self.assertEqual(None, self.cards_table.takeCardByIndex(2, 1))
        self.assertEqual(None, self.cards_table.takeCardByIndex(2, 0))

        self.cards_table.undoTakeCard()
        self.cards_table.undoTakeCard()
        self.assertEqual(self.cards_db[15], self.cards_table.getCard(2, 0))
        self.assertEqual(self.cards_db[14], self.cards_table.getCard(2, 1))
        self.assertEqual(None, self.cards_table.getCard(2, 2))
        self.assertEqual(None, self.cards_table.getCard(2, 3))
        self.cards_table.undoTakeCard()
        self.cards_table.undoTakeCard()
        self.cards_table.undoTakeCard()
        self.cards_table.undoTakeCard()
        self.cards_table.undoTakeCard()
        self.cards_table.undoTakeCard()
        self.assertEqual(self.cards_db[8], self.cards_table.getCard(2, 0))
        self.assertEqual(self.cards_db[9], self.cards_table.getCard(2, 1))
        self.assertEqual(self.cards_db[10], self.cards_table.getCard(2, 2))
        self.assertEqual(self.cards_db[11], self.cards_table.getCard(2, 3))

    def test_cards_stack(self):
        cards_count = self.cards_stack_lvl1.getCardsCount()
        self.assertEqual(8, cards_count)
        self.assertEqual(0, self.cards_stack_lvl1.getTopCardIndex())

        for i in range(cards_count):
            self.assertEqual(self.cards_db[i], self.cards_stack_lvl1.popCard())

        self.assertEqual(8, self.cards_stack_lvl1.getTopCardIndex())
        with self.assertRaises(AssertionError):
            self.cards_stack_lvl1.popCard()
        
        self.assertEqual(False, self.cards_stack_lvl1.getTopCard())

        for i in range(cards_count):
            self.cards_stack_lvl1.restoreCard()
            self.assertEqual(self.cards_db[cards_count - i - 1], self.cards_stack_lvl1.getTopCard())

        self.assertEqual(0, self.cards_stack_lvl1.getTopCardIndex())
        with self.assertRaises(AssertionError):
            self.cards_stack_lvl1.restoreCard()

    def test_cards_stack_level3_init(self):
        self.assertEqual(self.level3_stack.getTopCardIndex(), 0)
        self.assertEqual(self.level3_cards_count, self.level3_stack.getCardsCount())

        white_count = 0
        blue_count = 0
        green_count = 0
        red_count = 0
        black_count = 0

        for card in self.level3_stack.cards:
            self.assertEqual(3, card.level)
            white_count += card.getCost(CoinTypes.WHITE)
            blue_count += card.getCost(CoinTypes.BLUE)
            green_count += card.getCost(CoinTypes.GREEN)
            red_count += card.getCost(CoinTypes.RED)
            black_count += card.getCost(CoinTypes.BLACK)

        self.assertEqual(self.level3_cumulative_cost, white_count)
        self.assertEqual(self.level3_cumulative_cost, blue_count)
        self.assertEqual(self.level3_cumulative_cost, green_count)
        self.assertEqual(self.level3_cumulative_cost, red_count)
        self.assertEqual(self.level3_cumulative_cost, black_count)

    def test_cards_stack_level2_init(self):
        self.assertEqual(self.level2_stack.getTopCardIndex(), 0)
        self.assertEqual(self.level2_cards_count, self.level2_stack.getCardsCount())

        white_count = 0
        blue_count = 0
        green_count = 0
        red_count = 0
        black_count = 0

        for card in self.level2_stack.cards:
            self.assertEqual(2, card.level)
            white_count += card.getCost(CoinTypes.WHITE)
            blue_count += card.getCost(CoinTypes.BLUE)
            green_count += card.getCost(CoinTypes.GREEN)
            red_count += card.getCost(CoinTypes.RED)
            black_count += card.getCost(CoinTypes.BLACK)

        self.assertEqual(self.level2_cumulative_cost, white_count)
        self.assertEqual(self.level2_cumulative_cost, blue_count)
        self.assertEqual(self.level2_cumulative_cost, green_count)
        self.assertEqual(self.level2_cumulative_cost, red_count)
        self.assertEqual(self.level2_cumulative_cost, black_count)

    def test_cards_stack_level1_init(self):
        self.assertEqual(self.level1_stack.getTopCardIndex(), 0)
        self.assertEqual(self.level1_cards_count, self.level1_stack.getCardsCount())

        white_count = 0
        blue_count = 0
        green_count = 0
        red_count = 0
        black_count = 0

        for card in self.level1_stack.cards:
            self.assertEqual(1, card.level)
            white_count += card.getCost(CoinTypes.WHITE)
            blue_count += card.getCost(CoinTypes.BLUE)
            green_count += card.getCost(CoinTypes.GREEN)
            red_count += card.getCost(CoinTypes.RED)
            black_count += card.getCost(CoinTypes.BLACK)

        self.assertEqual(self.level1_cumulative_cost, white_count)
        self.assertEqual(self.level1_cumulative_cost, blue_count)
        self.assertEqual(self.level1_cumulative_cost, green_count)
        self.assertEqual(self.level1_cumulative_cost, red_count)
        self.assertEqual(self.level1_cumulative_cost, black_count)

    def test_cards_storage(self):
        self.assertEqual(self.cards.getCard(6), Card(white_cost=2, green_cost=2, level=CardLevel.ONE, discount=CoinTypes.BLACK))
        self.assertEqual(self.cards.getCard(21), Card(blue_cost=1, red_cost=2, black_cost=2, level=CardLevel.ONE, discount=CoinTypes.GREEN))
        self.assertEqual(self.cards.getCard(36), Card(white_cost=1, blue_cost=1, red_cost=1, black_cost=1, level=CardLevel.ONE, discount=CoinTypes.GREEN))
        self.assertEqual(self.cards.getCard(41), Card(blue_cost=5, level=CardLevel.TWO, points=2, discount=CoinTypes.BLUE))
        self.assertEqual(self.cards.getCard(70), Card(red_cost=6, level=CardLevel.TWO, points=3, discount=CoinTypes.RED))
        self.assertEqual(self.cards.getCard(90), Card(white_cost=3, black_cost=7, level=CardLevel.THREE, points=5, discount=CoinTypes.WHITE))

    def test_card(self):
        self.assertEqual(self.cards_db[4], Card(green_cost=3, level=CardLevel.ONE, discount=CoinTypes.GREEN))
        self.assertEqual(self.cards_db[12], Card(blue_cost=2, red_cost=2, level=CardLevel.TWO, discount=CoinTypes.RED))

if __name__ == '__main__':
    unittest.main(Card(white_cost=2, green_cost=2, level=CardLevel.ONE, discount=CoinTypes.BLACK))
