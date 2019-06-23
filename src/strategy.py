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

    def do_move(self):
        """Make a single move on the map."""
        raise NotImplementedError('Implement in child class!')

    def solve_map(self):
        """
        Solve the map within the move_limit, if possible, and print the
        success state and move count.
        """
        while not self.map.check_map() and self.count < self.move_limit:
            try:
                move = self.do_move()
                self.moves.append(move)
                self.count = self.count + 1
            except ISurrenderException:
                break
        status = 'SUCCESS!' if self.map.check_map() else 'FAILURE'
        print('Status: {status}, Count: {count}'.format(status=status, count=self.count))


class ToAndFroStrategy(Strategy):
    def __init__(self, map, **kwargs):
        super().__init__(map, **kwargs)
        self.action = Action.RIGHT
        self.can_move = True

    def do_move(self):
        if self.can_move and self.map.move(self.action):
            return self.action   # while we can, move along
        elif self.map.move(Action.DOWN):  # move down
            self.action = Action(
                (-self.action.value[0], self.action.value[1])
            )  # flip the direction
            return Action.DOWN
        else:
            raise ISurrenderException()  # can't move down further. give up.

class RandomMovesStrategy(Strategy):
    def do_move(self):
        import random
        action = random.choice(list(Action))  # choose a random action
        self.map.move(action)
        return action

