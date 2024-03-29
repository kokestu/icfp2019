#!/usr/bin/env python3

from map_io import read_input, write_output

import sys

def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        print('Program requires input file!')
    map = read_input(filename)
    # map._draw_map()

    solution = map.solve_map()   # TODO
    write_output(solution, "{}.sol".format(filename))   # TODO

def _test_map(filename):
    map = read_input(filename)
    map._draw_map()
    return map

if __name__== "__main__":
    main()