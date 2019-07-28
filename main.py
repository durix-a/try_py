import datetime
from game.best_turn_finder import BestTurnFinder
from multiprocessing.pool import ThreadPool
from multiprocessing.pool import Pool
import os

finder = BestTurnFinder()
# finder.findHighestValueTurnsSequence(12)
# print(finder.best_turns_sequence)
# print(finder.best_turns_sequence_points)

def findBestTurnsAsync(turn):
    finder = BestTurnFinder()
    finder.findTurnsHighestValueSequenceWithPrecalculatedBegginng(9, [turn])
    print(finder.best_turns_sequence)
    print(finder.best_turns_sequence_points)
    return finder.best_turns_sequence_points

first_turns = finder.enumerateAllValidTurns()
# p = ThreadPool(os.cpu_count())
p = Pool(os.cpu_count())
print(p.map(findBestTurnsAsync, first_turns))

# b = a.copy()

# b.remove(3)

# print(a)
# print(b)

print(datetime.datetime.now())
