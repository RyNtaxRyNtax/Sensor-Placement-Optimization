import math
import random
from typing import List, Tuple, Any
from search.local_search_base import LocalSearchBase


class SimulatedAnnealing(LocalSearchBase):
    def run(
        self,
        initial_state: List[Tuple[int, int]],
        initial_temperature: float = 1000.0,
        cooling_rate: float = 0.99,
        min_temperature: float = 0.1,
        **kwargs: Any
    ) -> Tuple[List[Tuple[int, int]], float, List[float], List[List[Tuple[int, int]]]]:
        current_state = list(initial_state)
        current_cost = self.evaluate(current_state)
        best_state = list(current_state)
        best_cost = current_cost
        evaluations = [current_cost]
        states_history = [current_state]
        temperature = initial_temperature
        while temperature > min_temperature:
            neighbor = self.get_neighbor(current_state)
            neighbor_cost = self.evaluate(neighbor)
            delta_e = neighbor_cost - current_cost
            if delta_e < 0 or random.random() < math.exp(-delta_e / temperature):
                current_state = neighbor
                current_cost = neighbor_cost
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_state = list(current_state)
            evaluations.append(current_cost)
            states_history.append(current_state)
            temperature *= cooling_rate
            return best_state, best_cost, evaluations, states_history
