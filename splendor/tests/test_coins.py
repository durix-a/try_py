import unittest
from coins.coin_types import CoinTypes
from coins.coins_table import CoinsTable


class TestCoins(unittest.TestCase):
    def test_coins_table(self):
        coins_table = CoinsTable()

        self.assertEqual(CoinsTable.max_coins_count, coins_table.getCoinsCount(CoinTypes.BLACK))

        coins_table.takeCoins(CoinTypes.RED)
        coins_table.takeCoins(CoinTypes.RED)
        self.assertEqual(CoinsTable.max_coins_count - 2, coins_table.getCoinsCount(CoinTypes.RED))
        coins_table.returnCoins(CoinTypes.RED)
        coins_table.returnCoins(CoinTypes.RED)
        with self.assertRaises(AssertionError):
            coins_table.returnCoins(CoinTypes.RED)

        i = CoinsTable.max_coins_count
        while(i > 0):
            coins_table.takeCoins(CoinTypes.GREEN)
            i -= 1
        
        with self.assertRaises(AssertionError):
            coins_table.takeCoins(CoinTypes.GREEN)
        
        self.assertEqual(0, coins_table.getCoinsCount(CoinTypes.GREEN))

if __name__ == '__main__':
    unittest.main()

    