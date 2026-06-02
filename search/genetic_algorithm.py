import random
from typing import List, Tuple, Any
from search.local_search_base import LocalSearchBase


class GeneticAlgorithm(LocalSearchBase):
    def run(
        self,
        initial_state: List[Tuple[int, int]],
        population_size: int = 50,
        generations: int = 100,
        mutation_rate: float = 0.3,
        **kwargs: Any
    ) -> Tuple[List[Tuple[int, int]], float, List[float], List[List[Tuple[int, int]]]]:
        population = [initial_state]
        for _ in range(population_size - 1):
            population.append(self.initialize_state())
        best_state = None
        best_cost = float("inf")
        evaluations = []
        states_history = []
        for _ in range(generations):
            scored_population = []
            for state in population:
                cost = self.evaluate(state)
                scored_population.append((cost, state))
                if cost < best_cost:
                    best_cost = cost
                    best_state = list(state)
            evaluations.append(best_cost)
            states_history.append(list(best_state))
            scored_population.sort(key=lambda x: x[0])
            new_population = [scored_population[0][1], scored_population[1][1]]
            while len(new_population) < population_size:
                parent1 = self._tournament_selection(scored_population)
                parent2 = self._tournament_selection(scored_population)
                child = self._crossover(parent1, parent2)
                if random.random() < mutation_rate:
                    child = self.get_neighbor(child)
                new_population.append(child)
            population = new_population
        return best_state, best_cost, evaluations, states_history

    def _tournament_selection(
        self, scored_population: List[Tuple[float, List[Tuple[int, int]]]], k: int = 3
    ) -> List[Tuple[int, int]]:
        best = min(random.sample(scored_population, k), key=lambda x: x[0])
        return list(best[1])

    def _crossover(
        self, parent1: List[Tuple[int, int]], parent2: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        combined = list(set(parent1 + parent2))
        max_s = self.world.max_sensors
        child_size = random.randint(1, min(len(combined), max_s))
        child = random.sample(combined, child_size)
        return child
