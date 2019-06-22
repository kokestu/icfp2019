#!/usr/bin/env python3

from map_io import read_input, write_output

import sys

def solve_map(map):
    pass   #TODO

def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        print('Program requires input file!')
    map = read_input(filename)
    map._draw_map()

    solution = map.solve_map()
    write_output(solution, "{}.sol".format(filename))


if __name__== "__main__":
    main()