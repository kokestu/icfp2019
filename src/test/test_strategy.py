import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from map_io import read_input, write_output
from strategy import RandomMovesStrategy, ToAndFroStrategy

import sys

class InvalidStrategyException(Exception):
    pass

def get_strategy(str):
    if str == 'random':
        return RandomMovesStrategy
    elif str == 'to_and_fro':
        return ToAndFroStrategy
    else:
        raise InvalidStrategyException(str)

def main():
    try:
        filename = sys.argv[1]
        strategy_str = sys.argv[2]
    except IndexError:
        print('Program requires input file and strategy!')
    try:
        draw_map = sys.argv[3] == '--draw'
    except IndexError:
        draw_map = False
    strat = get_strategy(strategy_str)
    map = read_input(filename)
    print('{}:'.format(os.path.basename(filename)))
    s = strat(map)
    s.solve_map()
    if draw_map:
        map._draw_map(is_interactive=True)
    return map, s

if __name__== "__main__":
    main()