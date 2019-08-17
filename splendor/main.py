import datetime
import itertools
from game.best_turn_finder import BestTurnFinder
from multiprocessing.pool import Pool
import os
import cProfile
import getopt
import sys

turns_sequence_length = 0

def main_sync():
    global turns_sequence_length
    start_time = datetime.datetime.now()
    finder = BestTurnFinder()
    finder.findHighestValueTurnsSequence(turns_sequence_length)
    end_time = datetime.datetime.now()
    print(end_time - start_time)
    print(finder.best_turns_sequences)
    print(finder.best_turns_sequence_points)

def findBestTurnsAsync(turns_sequence):
    global turns_sequence_length
    best_turn_finder = BestTurnFinder()
    best_turn_finder.findTurnsHighestValueSequenceWithPrecalculatedBegginng(turns_sequence_length, turns_sequence)
    print(datetime.datetime.now())
    return (best_turn_finder.best_turns_sequences, best_turn_finder.best_turns_sequence_points)

def main_async(precalculated_turns_sequence_length):
    start_time = datetime.datetime.now()
    finder = BestTurnFinder()
    finder.enumerateAllValidTurnSequences(precalculated_turns_sequence_length)
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

def print_usage():
    print("main.py [-a <precalculated-turns-sequence-length>] -l <turns-sequence-length>")
    print("\t -a - run asynchronously")
    print("\t\t <precalculated-turns-sequence-length> - each asynchronous process will start with this number of turns and will looks for the rest of turns")
    print("\t -l - search for sequences of <turns-sequence-length> turns long at maximum")

def main(argv):
    global turns_sequence_length
    precalculated_turns_sequence_length = 0
    run_profiling = False

    try:
        opts = getopt.getopt(argv,"hpa:l:")
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts[0]:
        if opt == "-h":
            print_usage()
            sys.exit()
        if opt == "-p":
            run_profiling = True
        elif opt == "-a":
            precalculated_turns_sequence_length = int(arg)
        elif opt == "-l":
            turns_sequence_length = int(arg)

    if precalculated_turns_sequence_length > 0:
        turns_sequence_length -= precalculated_turns_sequence_length
        main_async(precalculated_turns_sequence_length)
    else:
        if run_profiling:
            cProfile.run("main_sync()")
        else:
            main_sync()

if __name__ == "__main__":
    main(sys.argv[1:])

