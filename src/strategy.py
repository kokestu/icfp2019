from map import Map
from map_utils import *

class ISurrenderException(Exception):
    pass

class Strategy:
    def __init__(self, map, move_limit=1000):
        self.moves = []
        self.count = 0
        self.map = map
        self.move_limit = move_limit

    def get_move(self):
        """Decide which move to make on the map."""
        raise NotImplementedError('Implement in child class!')

    def can_make_action(self, action):
        try:
            return self.check_move_action(action) != PointStatus.OUT_OF_MAP
        except Exception:
            return True

    def check_move_action(self, action):
        return self.map.check_move_action(action)

    def solve_map(self):
        """
        Solve the map within the move_limit, if possible, and print the
        success state and move count.
        """
        while not self.map.check_map() and self.count < self.move_limit:
            try:
                move = self.get_move()
                self.moves.append(move)
                self.count = self.count + 1
                self.map.move(move)
            except ISurrenderException:
                break
        status = 'SUCCESS!' if self.map.check_map() else 'FAILURE'
        print('Status: {status}, Count: {count}'.format(status=status, count=self.count))


class ToAndFroStrategy(Strategy):
    def __init__(self, map, **kwargs):
        super().__init__(map, **kwargs)
        self.action = Action.RIGHT

    def get_move(self):
        if self.can_make_action(self.action):
            return self.action   # while we can, move along
        elif self.can_make_action(Action.DOWN):  # move down
            self.action = Action(
                (-self.action.value[0], self.action.value[1])
            )  # flip the direction
            return Action.DOWN
        else:
            raise ISurrenderException()  # can't move down further. give up.

class RandomMovesStrategy(Strategy):
    def get_move(self):
        import random
        success = False
        while not success:
            action = random.choice(list(Action))  # choose a random action
            success = self.can_make_action(action)
        return action

class FollowWallStrategy(Strategy):
    def __init__(self, map, **kwargs):
        super().__init__(map, **kwargs)
        self.initialising = True
        self.action = Action.RIGHT
        self.hand_on_wall = Action.UP

    def get_move(self):
        if self.initialising:   # move up until we meet a wall
            self.initialising = self.map.can_make_action(Action.UP)
            return Action.UP
        if self.can_make_action(self.hand_on_wall):
            # reached a corner! go round anticlockwise
            self.action = self.hand_on_wall
            self.hand_on_wall = rotate_action_anticlockwise(self.hand_on_wall)
            return self.action
        if self.can_make_action(self.action):
            # haven't reached a corner, continue
            return self.action
        else:
            # reached a corner! go round clockwise
            self.hand_on_wall = self.action
            self.action = rotate_action_clockwise(self.action)
            return self.action
