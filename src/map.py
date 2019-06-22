
from enum import Enum
from shapely.geometry import Polygon
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

class UnknownBoosterTypeException(Exception):
    pass

class BoosterType(Enum):
    B = 'extension'
    F = 'fastwheels'
    L = 'drill'
    X = 'mysterious'

def draw_obstacle(fig, obstacle):
    x, y = obstacle.exterior.xy
    ax = fig.add_subplot(111)
    ax.plot(x, y, 'r')

class Ground:
    def __init__(self, location):
        self.isWrapped = False
        self.location = location

    def wrap(self):
        self.isWrapped = True

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
        x, y = self.location
        ax = fig.add_subplot(111)
        ax.plot(x+0.5, y+0.5, color=self.get_booster_colour(), marker='o')

class Map:
    def __init__(self, corners, initial_location, obstacles, boosters):
        self.map = Polygon(corners)
        self.location = initial_location
        self.obstacles = [Polygon(obstacle) for obstacle in obstacles]
        self.boosters = boosters

    def _draw_map(self):
        fig = plt.figure(1, figsize=(5,5), dpi=90)

        # plot map
        x,y = self.map.exterior.xy
        ax = fig.add_subplot(111)
        ax.plot(x, y, 'b')

        # plot start location
        x, y = self.location
        ax = fig.add_subplot(111)
        ax.plot(x+0.5, y+0.5, 'gx')

        # plot boosters
        for booster in self.boosters:
            booster.draw_booster(fig)

        # plot obstacles
        for obstacle in self.obstacles:
            draw_obstacle(fig, obstacle)

        # add grid lines
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.grid(which='major')
        fig.show()

    def solve_map(self):
        return None   #TODO