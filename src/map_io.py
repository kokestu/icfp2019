
from map import Map, BoosterType, Booster
from ast import literal_eval as make_tuple
from shapely.geometry import MultiPoint
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

    # print(map_str, location_str, obstacles_str, boosters_str)

    corners = parse_points(map_str)
    initial_location = parse_point(location_str)
    obstacles = map(parse_points, filter(lambda x: x, obstacles_str.split(";")))
    boosters = map(parse_booster, filter(lambda x: x, obstacles_str.split(";")))

    # for corner in corners:
    #     print(corner)
    # print(initial_location)
    # for obstacle in obstacles:
    #     print(obstacle)
    # for booster in boosters:
    #     print(booster)

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
    class UnknownBoosterTypeException(Exception):
        pass

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

