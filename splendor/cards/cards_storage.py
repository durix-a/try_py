import csv
from cards.card import Card
from cards.card_level import CardLevel
from coins.coin_types import CoinTypes
import os.path


class CardsStorage:

    cards_levels_count = 3

    def __init__(self):
        self.cards_storage = []

        db_file_path = os.path.join("data", "cards - main cards.csv")
        with open(db_file_path) as cards_db:
            cards_db_reader = csv.reader(cards_db, delimiter=",")
            header_line_skipped = False

            for row in cards_db_reader:
                if not header_line_skipped:
                    header_line_skipped = True
                    continue

                card = Card(row[1], row[2], row[3], row[4], row[5], CardsStorage.parseLevel(row[6]), row[7], CardsStorage.parseCoinType(row[8]))

                self.cards_storage.append(card)

    @staticmethod
    def parseLevel(level):
        return {
            1: CardLevel.ONE, 
            2: CardLevel.TWO, 
            3: CardLevel.THREE 
        }[int(level)]

    @staticmethod
    def parseCoinType(coin):
        return {
            "white": CoinTypes.WHITE, 
            "blue": CoinTypes.BLUE, 
            "green": CoinTypes.GREEN,  
            "red": CoinTypes.RED, 
            "black": CoinTypes.BLACK  
        }[coin]

    def getCard(self, index):
        return self.cards_storage[index - 1]

