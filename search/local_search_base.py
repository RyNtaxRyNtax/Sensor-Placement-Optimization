import random
import copy
from typing import List, Tuple
from env.grid_world import GridWorld
from env.utils import random_position


class LocalSearchBase:
    def __init__(self, world: "GridWorld"):
        self.world = world

    def evaluate(self, state: List[Tuple[int, int]]) -> float:
        """
        Calculates the cost of the current sensor placement.
        Lower cost is better.
        """
        covered_targets = set()
        targets = self.world.get_targets()
        for sx, sy in state:
            for tx, ty in targets:
                if abs(sx - tx) + abs(sy - ty) <= self.world.sensor_range:
                    covered_targets.add((tx, ty))
        uncovered_count = len(targets) - len(covered_targets)
        sensor_count = len(state)
        cost = (uncovered_count * 100.0) + (sensor_count * 10.0)
        return cost

    def get_neighbor(self, state: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Generates a new valid state by applying a local change:
        Move, Add, ir Remove a sensor.
        """
        neighbor = copy.deepcopy(state)
        ops = [0]
        if len(neighbor) < self.world.max_sensors:
            ops.append(1)
        if len(neighbor) > 1:
            ops.append(2)
        op = random.choice(ops)
        if op == 0 and neighbor:
            idx = random.randint(0, len(neighbor) - 1)
            for _ in range(10):
                new_pos = random_position(self.world)
                if new_pos not in neighbor:
                    neighbor[idx] = new_pos
                    break
        elif op == 1:
            for _ in range(10):
                new_pos = random_position(self.world)
                if new_pos not in neighbor:
                    neighbor.append(new_pos)
                    break
        elif op == 2:
            idx = random.randint(0, len(neighbor) - 1)
            neighbor.pop(idx)
        return neighbor

    def initialize_state(self) -> List[Tuple[int, int]]:
        """
        Creates  a starting configuration of sensors randomly.
        """
        state = []
        initial_sensor_count = random.randint(1, self.world.max_sensors)
        for _ in range(initial_sensor_count):
            for _ in range(10):
                pos = random_position(self.world)
                if pos not in state:
                    state.append(pos)
                    break
        return state
