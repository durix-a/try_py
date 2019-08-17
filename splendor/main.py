import datetime
import itertools
from game.best_turn_finder import BestTurnFinder
from multiprocessing.pool import Pool
import os
import cProfile

def not_main():
    start_time = datetime.datetime.now()
    finder = BestTurnFinder()
    finder.findHighestValueTurnsSequence(8)
    end_time = datetime.datetime.now()
    print(end_time - start_time)
    print(finder.best_turns_sequences)
    print(finder.best_turns_sequence_points)

def findBestTurnsAsync(turns_sequence):
    best_turn_finder = BestTurnFinder()
    best_turn_finder.findTurnsHighestValueSequenceWithPrecalculatedBegginng(6, turns_sequence)
    print(datetime.datetime.now())
    return (best_turn_finder.best_turns_sequences, best_turn_finder.best_turns_sequence_points)

def main_async():
    start_time = datetime.datetime.now()
    finder = BestTurnFinder()
    finder.enumerateAllValidTurnSequences(2)
    first_turns_sequences = finder.all_first_turns_sequences
    p = Pool(os.cpu_count())
    results_map = p.map(findBestTurnsAsync, first_turns_sequences)

    max_points = 0
    for result in results_map:
        if result[1] >= max_points:
            max_points = result[1]

    best_results = list(filter(lambda result: True if result[1] >= max_points else False, results_map))
    end_time = datetime.datetime.now()
    print(end_time - start_time)
    print(best_results)

# cProfile.run("not_main()")

# not_main()

if __name__ == '__main__':
    main_async()