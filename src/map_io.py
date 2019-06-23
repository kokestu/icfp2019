
from map import Map, Booster
from ast import literal_eval as make_tuple
from shapely.geometry import MultiPoint
from map_utils import *
import re

class MalformedPointException(Exception):
    pass

class MalformedBoosterStringException(Exception):
    pass

def read_input(filepath):
    lines = []
    with open(filepath) as input:
        for line in input:
            lines.append(line)

    assert len(lines) == 1, "Should only have exactly one line in the input"

    map_str, location_str, obstacles_str, boosters_str = lines[0].split('#')

    corners = parse_points(map_str)
    initial_location = parse_point(location_str)
    obstacles = [parse_points(points) for points in obstacles_str.split(";") if points != '']
    boosters = [parse_booster(points) for points in boosters_str.split(";") if points != '']


    return Map(corners, initial_location, obstacles, boosters)

def write_output(solution, filename):
    pass   #TODO

def parse_points(string):
    points = re.split('(?<=\)),', string)
    return MultiPoint(list(map(parse_point, points)))

def parse_point(string):
    try:
        return make_tuple(string)
    except SyntaxError:
        raise MalformedPointException(string)

def parse_booster(string):
    try:
        booster_type = parse_booster_type(string[0])
        location = parse_point(string[1:])
        return Booster(booster_type, location)
    except IndexError:
        raise MalformedBoosterStringException(string)

def parse_booster_type(char):
    if char == 'B':
        return BoosterType.B
    elif char == 'F':
        return BoosterType.F
    elif char == 'L':
        return BoosterType.L
    elif char == 'X':
        return BoosterType.X
    else:
        raise UnknownBoosterTypeException(char)

