from map import Map
from map_utils import *

class Strategy:
    def __init__(self, map, move_limit=1000):
        self.moves = []
        self.map = map
        self.move_limit = move_limit

    def solve_map(self):
        """
        Solve the map within the move_limit, if possible, and print the
        success state and move count.
        """
        raise NotImplementedError('Implement in child class!')


class ToAndFroStrategy(Strategy):

    def solve_map(self):
        count = 0
        action = Action.RIGHT
        while not self.map.check_map or count < self.move_limit:
            can_move = True
            while can_move:  # while we can, move along
                can_move = self.map.move(action)
                if can_move:
                    self.moves.append(action)
                    count = count + 1
            if not self.map.move(Action.DOWN):
                break   # try to move down. if we can't, stop
            action = Action((-action.value[0], action.value[1]))  # flip the direction
        status = 'SUCCESS!' if self.map.check_map() else 'FAILURE'
        print('Status: {status}, Count: {count}'.format(status=status, count=count))