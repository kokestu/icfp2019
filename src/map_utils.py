from enum import Enum

class UnknownBoosterTypeException(Exception):
    pass

class UnknownDirectionException(Exception):
    pass

class UnknownActionException(Exception):
    pass

class ActionCannotBePerformedException(Exception):
    pass

class Action(Enum):
    """
    Action the robot should take (on the plot, UP and DOWN are inverted).
    """
    UP = (0, -1)   # (move up)
    DOWN = (0, 1)   # (move down)
    LEFT = (-1, 0)   # (move left)
    RIGHT = (1, 0)   # (move right)
    NOTHING = 'Z'   # (do nothing)
    CLOCKWISE = 'E'   # (turn manipulators 90° clockwise)
    ANTICLOCKWISE = 'Q'   # (turn manipulators 90° counterclockwise)
    # TODO implement boosters

def rotate_action_clockwise(action):
    x, y = action.value
    return Action((-y, x))

def rotate_action_anticlockwise(action):
    x, y = action.value
    return Action((y, -x)) 

def action_string(move):
    if move == Action.UP:
        return 'W'
    elif move == Action.DOWN:
        return 'S'
    elif move == Action.LEFT:
        return 'A'
    elif move == Action.RIGHT:
        return 'D'
    # elif move == Action.NOTHING:
    #     return 'Z'
    elif move == Action.CLOCKWISE:
        return 'E'
    elif move == Action.ANTICLOCKWISE:
        return 'Q'
    else:
        raise UnknownActionException(move.name)

BUTTON_SIZE=0.1
X_CORNER=0.5
Y_CORNER=0.05

def action_button_props(action):
    if action == Action.UP:
        return (X_CORNER, Y_CORNER + BUTTON_SIZE, u"\u25B2")
    elif action == Action.DOWN:
        return (X_CORNER, Y_CORNER, u"\u25BC")
    elif action == Action.LEFT:
        return (X_CORNER - BUTTON_SIZE, Y_CORNER, u"\u25C0")
    elif action == Action.RIGHT:
        return (X_CORNER + BUTTON_SIZE, Y_CORNER, u"\u25B6")
    elif action == Action.CLOCKWISE:
        return (X_CORNER + BUTTON_SIZE, Y_CORNER + BUTTON_SIZE, u"\u21BB")
    elif action == Action.ANTICLOCKWISE:
        return (X_CORNER - BUTTON_SIZE, Y_CORNER + BUTTON_SIZE, u"\u21BA")
    else:
        raise Exception('No button for action {}!'.format(move.name))

class Direction(Enum):
    """
    Direction the robot is facing (on the plot, N and S are inverted).
    """
    N = 0
    E = 1
    S = 2
    W = 3

class BoosterType(Enum):
    B = 0   # 'extension'
    F = 1   # 'fastwheels'
    L = 2   # 'drill'
    X = 3   # 'mysterious'

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