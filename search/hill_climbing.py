from typing import List, Tuple, Any
from search.local_search_base import LocalSearchBase


class HillClimbing(LocalSearchBase):
    def run(
        self,
        initial_state: List[Tuple[int, int]],
        max_iterations: int = 1000,
        neighbors_samples: int = 30,
        **kwargs: Any
    ) -> Tuple[List[Tuple[int, int]], float, List[float], List[List[Tuple[int, int]]]]:
        current_state = list(initial_state)
        current_cost = self.evaluate(current_state)
        evaluations = [current_cost]
        states_history = [current_state]
        for _ in range(max_iterations):
            best_neighbor = None
            best_neighbor_cost = float("inf")
            for _ in range(neighbors_samples):
                neighbor = self.get_neighbor(current_state)
                cost = self.evaluate(neighbor)
                if cost < best_neighbor_cost:
                    best_neighbor_cost = cost
                    best_neighbor = neighbor
            if best_neighbor_cost >= current_cost:
                break
            current_state = best_neighbor
            current_cost = best_neighbor_cost
            evaluations.append(current_cost)
            states_history.append(current_state)
        return current_state, current_cost, evaluations, states_history
