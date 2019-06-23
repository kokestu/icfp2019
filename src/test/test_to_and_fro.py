import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from map_io import read_input, write_output
from strategy import ToAndFroStrategy

import sys

def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        print('Program requires input file!')
    try:
        draw_map = sys.argv[2] == '--draw'
    except IndexError:
        pass
    map = read_input(filename)
    print('{}:'.format(os.path.basename(filename)))
    s = ToAndFroStrategy(map)
    s.solve_map()
    if draw_map:
        map._draw_map()

if __name__== "__main__":
    main()