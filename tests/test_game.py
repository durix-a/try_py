import unittest
from coins.coin_types import CoinTypes
from coins.coins_table import CoinsTable
from game.player import Player
from cards.card import Card
from cards.card_level import CardLevel
from cards.cards_stack import CardsStack
from cards.cards_table import CardsTable
from game.game_turns_enumerator import GameTurnsEnumerator
from game.game_turn import GameTurn
from game.game_turn_validator import GameTurnValidator


class TestGame(unittest.TestCase):
    def setUp(self):
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

    def testGameTurn(self):
        coins_table = CoinsTable()
        turn = GameTurn([], self.cards_db[0])
        player = Player()

        coins_table.takeCoins(CoinTypes.BLUE, 3)
        player.receiveCoins(CoinTypes.BLUE, 3)
        turn.payForPurchasedCard(player, coins_table)
        self.assertEqual(0, player.getCoinsCount(CoinTypes.BLUE))
        self.assertEqual(3, turn.getPaidCoinsCount(CoinTypes.BLUE))

        turn.returnPaymentForPurchasedCard(player, coins_table)
        self.assertEqual(3, player.getCoinsCount(CoinTypes.BLUE))
        self.assertEqual(0, turn.getPaidCoinsCount(CoinTypes.BLUE))

        turn = GameTurn([], self.cards_db[8])
        coins_table.takeCoins(CoinTypes.GREEN, 3)
        player.receiveCoins(CoinTypes.GREEN, 3)
        player.receivePurchasedCard(self.cards_db[1])
        player.receivePurchasedCard(self.cards_db[3])
        player.receivePurchasedCard(self.cards_db[4])
        turn.payForPurchasedCard(player, coins_table)
        self.assertEqual(3, player.getCoinsCount(CoinTypes.BLUE))
        self.assertEqual(2, player.getCoinsCount(CoinTypes.GREEN))
        self.assertEqual(0, turn.getPaidCoinsCount(CoinTypes.BLUE))
        self.assertEqual(1, turn.getPaidCoinsCount(CoinTypes.GREEN))

        turn.returnPaymentForPurchasedCard(player, coins_table)
        self.assertEqual(3, player.getCoinsCount(CoinTypes.BLUE))
        self.assertEqual(3, player.getCoinsCount(CoinTypes.GREEN))
        self.assertEqual(0, turn.getPaidCoinsCount(CoinTypes.BLUE))
        self.assertEqual(0, turn.getPaidCoinsCount(CoinTypes.GREEN))

        turn = GameTurn([], self.cards_db[8])
        player.receivePurchasedCard(self.cards_db[9])
        turn.payForPurchasedCard(player, coins_table)
        self.assertEqual(3, player.getCoinsCount(CoinTypes.BLUE))
        self.assertEqual(2, player.getCoinsCount(CoinTypes.GREEN))
        self.assertEqual(0, turn.getPaidCoinsCount(CoinTypes.BLUE))
        self.assertEqual(1, turn.getPaidCoinsCount(CoinTypes.GREEN))

        turn.returnPaymentForPurchasedCard(player, coins_table)
        self.assertEqual(3, player.getCoinsCount(CoinTypes.BLUE))
        self.assertEqual(3, player.getCoinsCount(CoinTypes.GREEN))
        self.assertEqual(0, turn.getPaidCoinsCount(CoinTypes.BLUE))
        self.assertEqual(0, turn.getPaidCoinsCount(CoinTypes.GREEN))

    def test_player(self):
        player = Player()

        self.assertEqual(0, player.getAllCoinsCount())
        player.receiveCoins(CoinTypes.RED)
        player.receiveCoins(CoinTypes.RED)
        player.receiveCoins(CoinTypes.WHITE)
        player.receiveCoins(CoinTypes.BLUE)
        player.receiveCoins(CoinTypes.BLACK)
        player.receiveCoins(CoinTypes.BLACK)
        player.receiveCoins(CoinTypes.BLACK)
        self.assertEqual(7, player.getAllCoinsCount())

        with self.assertRaises(AssertionError):
            player.returnCoins(CoinTypes.GREEN)

        player.receivePurchasedCard(self.cards_db[0])
        player.receivePurchasedCard(self.cards_db[2])
        self.assertEqual(2, player.getPurchasedCardsCount(CoinTypes.WHITE))
        self.assertEqual(self.cards_db[0], player.getPurchasedCard(CoinTypes.WHITE, 0))
        self.assertEqual(self.cards_db[2], player.getPurchasedCard(CoinTypes.WHITE, 1))

        player.receivePurchasedCard(self.cards_db[1])
        player.receivePurchasedCard(self.cards_db[3])
        player.receivePurchasedCard(self.cards_db[9])
        self.assertEqual(3, player.getPurchasedCardsCount(CoinTypes.BLUE))
        self.assertEqual(self.cards_db[1], player.getPurchasedCard(CoinTypes.BLUE, 0))
        self.assertEqual(self.cards_db[3], player.getPurchasedCard(CoinTypes.BLUE, 1))
        self.assertEqual(self.cards_db[9], player.getPurchasedCard(CoinTypes.BLUE, 2))

        player.returnPurchasedCard(self.cards_db[3])
        self.assertEqual(2, player.getPurchasedCardsCount(CoinTypes.BLUE))
        self.assertEqual(self.cards_db[1], player.getPurchasedCard(CoinTypes.BLUE, 0))
        self.assertEqual(self.cards_db[9], player.getPurchasedCard(CoinTypes.BLUE, 1))

        with self.assertRaises(ValueError):
            player.returnPurchasedCard(self.cards_db[3])

    def test_game_turns_enumerator(self):
        coins_table = CoinsTable()
        level1_stack = CardsStack(CardLevel.ONE, self.cards_db)
        level2_stack = CardsStack(CardLevel.TWO, self.cards_db)
        level3_stack = CardsStack(CardLevel.THREE, self.cards_db)
        cards_table = CardsTable(level1_stack, level2_stack, level3_stack)
        turns_enumerator = GameTurnsEnumerator(coins_table, cards_table)

        turns = turns_enumerator.enumerateAllPossibleTurns()
        self.assertEqual(10 + 12, len(turns))
        self.assertEqual(GameTurn([CoinTypes.WHITE, CoinTypes.BLUE, CoinTypes.GREEN], None), turns[0])
        self.assertEqual(GameTurn([CoinTypes.WHITE, CoinTypes.BLUE, CoinTypes.RED], None), turns[1])
        self.assertEqual(GameTurn([CoinTypes.BLUE, CoinTypes.GREEN, CoinTypes.RED], None), turns[6])
        self.assertEqual(GameTurn([CoinTypes.GREEN, CoinTypes.RED, CoinTypes.BLACK], None), turns[9])
        self.assertEqual(GameTurn([], self.cards_db[0]), turns[10])
        self.assertEqual(GameTurn([], self.cards_db[8]), turns[14])
        self.assertEqual(GameTurn([], self.cards_db[16]), turns[18])

    def test_game_turns_validator(self):
        turn_validator = GameTurnValidator()
        player = Player()
        
        self.assertTrue(turn_validator.isTurnValid(GameTurn([CoinTypes.GREEN, CoinTypes.RED, CoinTypes.BLACK], None), player))
        player.receiveCoins(CoinTypes.GREEN)
        player.receiveCoins(CoinTypes.RED)
        player.receiveCoins(CoinTypes.BLACK)
        # W: 0, B: 0, G: 1, R: 1, B:1

        self.assertTrue(turn_validator.isTurnValid(GameTurn([CoinTypes.GREEN, CoinTypes.RED, CoinTypes.BLACK], None), player))
        player.receiveCoins(CoinTypes.GREEN)
        player.receiveCoins(CoinTypes.RED)
        player.receiveCoins(CoinTypes.BLACK)
        # W: 0, B: 0, G: 2, R: 2, B:2
        
        self.assertTrue(turn_validator.isTurnValid(GameTurn([CoinTypes.WHITE, CoinTypes.BLUE, CoinTypes.BLACK], None), player))
        player.receiveCoins(CoinTypes.WHITE)
        player.receiveCoins(CoinTypes.BLUE)
        player.receiveCoins(CoinTypes.BLACK)
        # W: 1, B: 1, G: 2, R: 2, B:3
        
        self.assertFalse(turn_validator.isTurnValid(GameTurn([CoinTypes.WHITE, CoinTypes.BLUE], None), player))
        self.assertTrue(turn_validator.isTurnValid(GameTurn([], self.cards_db[7]), player))
        player.receivePurchasedCard(self.cards_db[7]) # W: 1, B: 1, G: 3, R: 2, B:3
        player.returnCoins(CoinTypes.BLACK)
        player.returnCoins(CoinTypes.BLACK)
        player.returnCoins(CoinTypes.BLACK)
        # W: 1, B: 1, G: 3, R: 2, B:0
        
        self.assertFalse(turn_validator.isTurnValid(GameTurn([], self.cards_db[5]), player))
        self.assertFalse(turn_validator.isTurnValid(GameTurn([], self.cards_db[9]), player))
        self.assertTrue(turn_validator.isTurnValid(GameTurn([CoinTypes.WHITE, CoinTypes.BLUE, CoinTypes.BLACK], None), player))
        player.receiveCoins(CoinTypes.WHITE)
        player.receiveCoins(CoinTypes.BLUE)
        player.receiveCoins(CoinTypes.BLACK)
        # W: 2, B: 2, G: 3, R: 2, B:1
        
        self.assertTrue(turn_validator.isTurnValid(GameTurn([], self.cards_db[9]), player))
        player.receivePurchasedCard(self.cards_db[9]) # W: 2, B: 3, G: 3, R: 2, B:1
        player.returnCoins(CoinTypes.WHITE)
        player.returnCoins(CoinTypes.WHITE)
        player.returnCoins(CoinTypes.GREEN)
        player.returnCoins(CoinTypes.GREEN)
        # W: 0, B: 3, G: 1, R: 2, B:1
        
        self.assertTrue(turn_validator.isTurnValid(GameTurn([], self.cards_db[0]), player))
        player.receivePurchasedCard(self.cards_db[0]) # W: 1, B: 3, G: 1, R: 2, B:1

        self.assertFalse(turn_validator.isTurnValid(GameTurn([], self.cards_db[3]), player))
        player.receivePurchasedCard(self.cards_db[3]) # W: 1, B: 4, G: 1, R: 2, B:1
        player.receivePurchasedCard(self.cards_db[2]) # W: 2, B: 4, G: 1, R: 2, B:1
        self.assertTrue(turn_validator.isTurnValid(GameTurn([], self.cards_db[11]), player))

