
from enum import Enum
from shapely.geometry import Polygon
from matplotlib import pyplot as plt

class BoosterType(Enum):
    B = 'extension'
    F = 'fastwheels'
    L = 'drill'
    X = 'mysterious'

def draw_obstacle(fig, obstacle):
    x, y = obstacle.exterior.xy
    ax = fig.add_subplot(111)
    ax.plot(x, y)

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

class Map:
    def __init__(self, corners, initial_location, obstacles, boosters):
        self.map = Polygon(corners)
        self.location = initial_location
        self.obstacles = list(map(Polygon, obstacles))
        self.boosters = boosters

    def _draw_map(self):
        x,y = self.map.exterior.xy
        fig = plt.figure(1, figsize=(5,5), dpi=90)
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        for obstacle in self.obstacles:
            draw_obstacle(fig, obstacle)
        fig.show()

    def solve_map(self):
        return None   #TODO