from map_utils import *
from shapely.geometry import Polygon, Point, MultiPoint
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.collections import PatchCollection
import operator
import numpy as np
from itertools import product
from matplotlib.widgets import Button, Slider

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
        self.map = Polygon(corners)
        self.location = initial_location   # location of the robot
        for obstacle in obstacles:
            self.map = self.map.difference(Polygon(obstacle))
        self.boosters = boosters   # the boosters on the map
        self.count = 0   # the move count
        self.direction = Direction.E   # direction the robot is facing
        self.wrapped = set()   # the points that have been wrapped
        self._set_unwrapped()   # the points remaining unwrapped
        self._wrap_points_with_manipulators()

    def _set_unwrapped(self):
        x_min,y_min,x_max,y_max=self.map.bounds
        x = np.arange(x_min+0.5, x_max+0.5)
        y = np.arange(y_min+0.5, y_max+0.5)
        all_possible_points = list(product(x, y))
        points_on_map = self.map.intersection(MultiPoint(all_possible_points))
        self.unwrapped = {(i.x - 0.5, i.y - 0.5) for i in points_on_map}

    def _wrap_points_with_manipulators(self):
        # TODO implement line of sight
        x, y = self.location
        if self.direction == Direction.N:
            self.wrap_points([(x, y), (x-1, y+1), (x, y+1), (x+1, y+1)])
        elif self.direction == Direction.E:
            self.wrap_points([(x, y), (x+1, y+1), (x+1, y), (x+1, y-1)])
        elif self.direction == Direction.S:
            self.wrap_points([(x, y), (x+1, y-1), (x, y-1), (x-1, y-1)])
        elif self.direction == Direction.W:
            self.wrap_points([(x, y), (x-1, y-1), (x-1, y), (x-1, y+1)])
        else:
            raise UnknownDirectionException(self.direction.value, self.direction.name)

    def move(self, action):
        if action == Action.NOTHING:
            pass
        elif action == Action.CLOCKWISE:
            self.direction = Direction((self.direction.value + 1) % 4)
        elif action == Action.ANTICLOCKWISE:
            self.direction = Direction((self.direction.value - 1) % 4)
        elif action in [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]:
            new_loc = tuple(map(operator.add, self.location, action.value))
            status, _ = self.check_point(new_loc)
            if status == PointStatus.OUT_OF_MAP:
                return False
            self.location = new_loc
        else:
            raise UnknownActionException(action.name)
        self._wrap_points_with_manipulators()
        self.count = self.count + 1
        return True

    def check_point(self, point):
        # check point in map
        x, y = get_square(point)
        p = Point(x, y)
        if not self.map.contains(p):
            return (PointStatus.OUT_OF_MAP, PointContents.NOTHING)

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

    def _draw_map(self, interactive = True):
        fig = plt.figure(1, figsize=(5,5), dpi=90)

        # plot map
        x,y = self.map.exterior.xy
        ax = fig.add_subplot(111)
        ax.plot(x, y, 'b')

        # plot wrapped area
        self.wrapped_plot = self._draw_wrapped(ax)

        # plot start location
        x, y = get_square(self.location)
        ax = fig.add_subplot(111)
        self.robot_marker, = ax.plot(x, y, 'gx')

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

        if interactive:
            self._plot_interactive(fig, ax)
        
        fig.show()


    def _plot_interactive(self, fig, ax): 
        plt.ion()
        fig.subplots_adjust(bottom=0.3)
        button_size=0.1
        x_corner=0.5
        y_corner=0.05
        ax_up = plt.axes([x_corner, y_corner+button_size, button_size, button_size])
        ax_down = plt.axes([x_corner, y_corner, button_size, button_size])
        ax_left = plt.axes([x_corner+button_size, y_corner, button_size, button_size])
        ax_right = plt.axes([x_corner-button_size, y_corner, button_size, button_size])
        ax_clockwise = plt.axes([x_corner+button_size, y_corner+button_size, button_size, button_size])
        ax_anticlockwise = plt.axes([x_corner-button_size, y_corner+button_size, button_size, button_size])

        self.button_up = Button(ax_up, u"\u25B2",color='r', hovercolor='g')
        self.button_down = Button(ax_down, u"\u25BC",color='r', hovercolor='g')
        self.button_left = Button(ax_left, u"\u25B6",color='r', hovercolor='g')
        self.button_right = Button(ax_right, u"\u25C0",color='r', hovercolor='g')
        self.button_clockwise = Button(ax_clockwise, u"\u21BB",color='r', hovercolor='g')
        self.button_anticlockwise = Button(ax_anticlockwise, u"\u21BA",color='r', hovercolor='g')

        def do_moving_wrapper(action):
            def do_moving(event):
                self.move(action)
                self.wrapped_plot.remove()
                self.wrapped_plot = self._draw_wrapped(ax)
                x, y = get_square(self.location)
                self.robot_marker.set_xdata(x)
                self.robot_marker.set_ydata(y)
            return do_moving

        self.button_up.on_clicked(do_moving_wrapper(Action.DOWN))
        self.button_down.on_clicked(do_moving_wrapper(Action.UP))
        self.button_left.on_clicked(do_moving_wrapper(Action.RIGHT))
        self.button_right.on_clicked(do_moving_wrapper(Action.LEFT))
        self.button_clockwise.on_clicked(do_moving_wrapper(Action.CLOCKWISE))
        self.button_anticlockwise.on_clicked(do_moving_wrapper(Action.ANTICLOCKWISE))

    def _draw_wrapped(self, ax):
        patches = [plt.Rectangle(point,width=1,height=1) for point in self.wrapped]
        collection = PatchCollection(patches, facecolor='k', alpha=0.5)
        return ax.add_collection(collection)

    def check_map(self):
        if self.unwrapped:
              return False
        else:
              return True

    def wrap_points(self, points):
        points = set(points).intersection(self.unwrapped)
        self.wrapped.update(points)
        self.unwrapped.difference_update(points)
