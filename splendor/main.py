import datetime
from game.best_turn_finder import BestTurnFinder
from multiprocessing.pool import Pool
import os

# finder = BestTurnFinder()
# finder.findHighestValueTurnsSequence(12)
# print(finder.best_turns_sequence)
# print(finder.best_turns_sequence_points)

def findBestTurnsAsync(turn):
    best_turn_finder = BestTurnFinder()
    best_turn_finder.findTurnsHighestValueSequenceWithPrecalculatedBegginng(13, [turn])
    print(best_turn_finder.best_turns_sequence)
    print(best_turn_finder.best_turns_sequence_points)
    print(datetime.datetime.now())
    return best_turn_finder.best_turns_sequence_points

def main():
    finder = BestTurnFinder()
    first_turns = finder.enumerateAllValidTurns()
    p = Pool(os.cpu_count())
    print(p.map(findBestTurnsAsync, first_turns))

if __name__ == '__main__':
    main()