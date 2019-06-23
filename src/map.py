
from enum import Enum
from shapely.geometry import Polygon, Point, MultiPoint
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.collections import PatchCollection


class UnknownBoosterTypeException(Exception):
    pass

class BoosterType(Enum):
    B = 'extension'
    F = 'fastwheels'
    L = 'drill'
    X = 'mysterious'

class PointStatus(Enum):
    OUT_OF_MAP = 0
    IN_OBSTACLE = 1
    UNWRAPPED = 2
    WRAPPED = 3

class PointContents(Enum):
    BOOSTER_B = 0
    BOOSTER_F = 1
    BOOSTER_L = 2
    BOOSTER_X = 3
    ROBOT = 4
    NOTHING = 5

def draw_obstacle(fig, obstacle):
    x, y = obstacle.xy
    ax = fig.add_subplot(111)
    ax.plot(x, y, 'r')

def get_square(point):
    """Get the centre of the square"""
    x, y = point
    return x+0.5, y+0.5

class Booster:
    def __init__(self, type, location):
        self.type = type
        self.location = location

    # colors from https://blog.xkcd.com/2010/05/03/color-survey-results/
    def get_booster_colour(self):
        if self.type == BoosterType.B:
            return '#650021'   # maroon
        elif self.type == BoosterType.F:
            return '#01ff07'   # bright green
        elif self.type == BoosterType.L:
            return '#ff028d'   # hot pink
        elif self.type == BoosterType.X:
            return '#f97306'   # orange
        else:
            raise UnknownBoosterTypeException(self.type.value)

    def draw_booster(self, fig):
        x, y = get_square(self.location)
        ax = fig.add_subplot(111)
        ax.plot(x, y, color=self.get_booster_colour(), marker='o')

class Map:
    def __init__(self, corners, initial_location, obstacles, boosters):
        self.wrapped = set()
        self.map = Polygon(corners)
        self.location = initial_location
        for obstacle in obstacles:
            self.map = self.map.difference(Polygon(obstacle))
        self.boosters = boosters

    def check_point(self, point):
        # check point in map
        x, y = get_square(point)
        p = Point(x, y)
        if not self.map.contains(p):
            return (PointStatus.OUT_OF_MAP, PointContents.NOTHING)

        # check point in obstacle
        for obstacle in self.obstacles:
            if obstacle.contains(p):
                return (PointStatus.IN_OBSTACLE, PointContents.NOTHING)

        boosters = [b for b in self.boosters if b.location == point]
        # check contents
        if point == self.location:
            contents = PointContents.ROBOT
        elif len(boosters) != 0:
            type = boosters[0].type
            if type == BoosterType.B:
                contents = PointContents.BOOSTER_B
            elif type == BoosterType.F:
                contents = PointContents.BOOSTER_F
            elif type == BoosterType.L:
                contents = PointContents.BOOSTER_L
            elif type == BoosterType.X:
                contents = PointContents.BOOSTER_X
            else:
                raise UnknownBoosterTypeException(type.value)
        else:
            contents = PointContents.NOTHING

        # check if wrapped
        if point in self.wrapped:
            return (PointStatus.WRAPPED, contents)
        else:
            return (PointStatus.UNWRAPPED, contents)

    def _draw_map(self):
        fig = plt.figure(1, figsize=(5,5), dpi=90)

        # plot map
        x,y = self.map.exterior.xy
        ax = fig.add_subplot(111)
        ax.plot(x, y, 'b')

        # plot wrapped area
        self._draw_wrapped(ax)

        # plot start location
        x, y = get_square(self.location)
        ax = fig.add_subplot(111)
        ax.plot(x, y, 'gx')

        # plot boosters
        for booster in self.boosters:
            booster.draw_booster(fig)

        # plot obstacles
        for obstacle in self.map.interiors:
            draw_obstacle(fig, obstacle)

        # add grid lines
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.grid(which='major')
        fig.show()

    def _draw_wrapped(self, ax):
        patches = [plt.Rectangle(point,width=1,height=1) for point in self.wrapped]
        collection = PatchCollection(patches, facecolor='k')
        ax.add_collection(collection)

    def wrap_points(self, points):
        self.wrapped.update(points)

    def check_map(self):
        raise NotImplementedError()   # TODO

    def wrap_points(self, points):
        self.wrapped.update(points)

    def solve_map(self):
        return None   #TODO
