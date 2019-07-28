import datetime
from game.best_turn_finder import BestTurnFinder

finder = BestTurnFinder()
finder.findHighestValueTurnsSequence(12)

print(finder.best_turns_sequence)
print(finder.best_turns_sequence_points)

print(datetime.datetime.now())

# a = [1, 3, 4, 5, 7, 8, 0]
# b = a.copy()

# b.remove(3)

# print(a)
# print(b)