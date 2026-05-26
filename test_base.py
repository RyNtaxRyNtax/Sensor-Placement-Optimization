from env.grid_world import GridWorld
from search.local_search_base import LocalSearchBase

if __name__ == "__main__":
    world = GridWorld("map1")
    base = LocalSearchBase(world)

    print("--- Testing LocalSearchBase ---")

    initial_state = base.initialize_state()
    print(f"1. Initial State (Sensors): {initial_state}")

    initial_cost = base.evaluate(initial_state)
    print(f"2. Initial Cost: {initial_cost}")

    neighbor_state = base.get_neighbor(initial_state)
    neighbor_cost = base.evaluate(neighbor_state)

    print(f"3. Neighbor State: {neighbor_state}")
    print(f"4. Neighbor Cost: {neighbor_cost}")
    print("-------------------------------")
