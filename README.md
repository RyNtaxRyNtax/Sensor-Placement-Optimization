# Sensor Placement Optimization: A Metaheuristic Approach

_[**Github Repository**](https://github.com/RyNtaxRyNtax/Sensor-Placement-Optimization.git)_
_[README in Persian](README_FA.md)_

**Course:** Artificial Intelligence  
**Professor:** Dr. Nasiri
**University:** University of Isfahan

---

## 1. Abstract and Problem Definition

In a post-apocalyptic scenario set in 2145, survival depends on deploying a network of smart sensors to monitor vital signals and energy sources. This project formulates the "Sensor Placement" problem as a combinatorial optimization task within a 2D Grid Environment containing obstacles, valid operational nodes, and static targets.

### 1.1. Mathematical Modeling

Let $G = (V, E)$ be the grid where each cell $(x, y) \in V$.

- Let $T = \{t_1, t_2, ..., t_k\}$ be the set of Target coordinates.
- Let $S = \{s_1, s_2, ..., s_n\}$ be a proposed State (set of deployed sensors), where $n \le S_{max}$.
- The coverage radius is defined by Manhattan Distance. A target $t_i = (x_t, y_t)$ is considered covered by a sensor $s_j = (x_s, y_s)$ if:
  $$|x_t - x_s| + |y_t - y_s| \le R_{sensor}$$

### 1.2. Cost Function (Objective)

The problem requires a delicate trade-off between maximizing target coverage and minimizing resource (sensor) consumption. The objective function to be minimized is defined as:
$$\text{Cost}(S) = (W_{penalty} \times |T_{uncovered}|) + (W_{resource} \times |S|)$$
Where $W_{penalty} \gg W_{resource}$ (e.g., 100 vs. 10) to prioritize coverage over sensor conservation.

---

## 2. Algorithmic Implementations

### 2.1. Steepest-Ascent Hill Climbing (HC)

A purely greedy exploitative search. In each iteration, HC samples $N$ random neighbors and unconditionally transitions to the neighbor $S'$ that yields the lowest cost, provided $\text{Cost}(S') < \text{Cost}(S)$. It terminates upon reaching the first local minimum.

### 2.2. Simulated Annealing (SA)

Inspired by metallurgy, SA balances exploration and exploitation. It accepts cost-increasing states (worse configurations) with a probability derived from the Boltzmann distribution:
$$P(\text{accept}) = e^{-\frac{\Delta \text{Cost}}{T}}$$
An inner loop (Markov Chain length) was implemented to ensure sufficient exploration at each temperature level before applying the cooling schedule $T_{new} = T_{old} \times \alpha$.

### 2.3. Genetic Algorithm (GA) [Bonus]

A population-based evolutionary approach:

- **Selection:** Tournament selection ($k=3$) to choose robust parents while preserving diversity.
- **Crossover:** A set-union-based crossover combining sensors from both parents, then randomly sampling a subset to respect the $S_{max}$ constraint.
- **Mutation:** Utilizing the domain-specific neighbor function to randomly move, add, or remove a sensor.
- **Elitism:** Directly transferring the top 2 configurations to the next generation to prevent regression.

---

## 3. Experimental Results

The algorithms were tested across 7 maps with varying obstacle densities and target distributions. Results indicate the Final Cost:

| Map Complexity                    | Hill Climbing | Simulated Annealing | Genetic Algorithm |
| :-------------------------------- | :------------ | :------------------ | :---------------- |
| **Map 1** (Standard)              | 460.0         | 130.0               | 190.0             |
| **Map 2** (Dense Obstacles)       | 1380.0        | 780.0               | 880.0             |
| **Map 3**                         | 450.0         | 250.0               | 350.0             |
| **Map 4**                         | 340.0         | 240.0               | 240.0             |
| **Map 5** (High Target Dispersal) | 650.0         | 350.0               | 780.0             |
| **Map 6** (Large Grid)            | 2260.0        | 1560.0              | 1560.0            |
| **Map 7** (Small Grid)            | 90.0          | 60.0                | 80.0              |

---

## 4. Comprehensive Analysis & Discussion

### 4.1. The Vulnerability of Greedy Search (Local Optima)

Hill Climbing systematically failed across all topographies. Because it lacks a mechanism to traverse "uphill" (accepting temporary worse states), it invariably halted at suboptimal valleys. The highest disparity was observed in Map 6, where HC's cost (2260) was a staggering 700 points worse than both SA and GA. This proves that pure exploitation is inadequate for non-convex search spaces with high obstacle density.

### 4.2. Thermodynamic Behavior and Hyperparameter Tuning in SA

SA demonstrated the most consistent and superior performance. The success of SA relied heavily on its hyperparameters. A high initial temperature $T_0$ allowed the algorithm to behave like a random walk in its initial phase (Exploration), bouncing out of early local optima. As $T$ decayed, the probability $e^{-\frac{\Delta E}{T}}$ approached zero, naturally transitioning the algorithm into a fine-tuning Hill Climbing phase (Exploitation). The addition of an inner loop allowed the system to reach thermal equilibrium at each temperature step, leading to its dominance in complex maps like Map 5 (350.0 cost).

### 4.3. Population Dynamics and Genetic Anomalies

The Genetic Algorithm showcased massive potential but revealed high sensitivity to spatial topologies.

- **Successes:** In Maps 4 and 6, the GA's crossover mechanism effectively merged the best sub-networks from different parents, perfectly matching SA's performance (240 and 1560 respectively).
- **The Map 5 Anomaly:** In Map 5, GA achieved a cost of 780, performing worse than HC (650). This indicates a _Premature Convergence_ failure. The spatial distribution of targets in Map 5 likely caused the crossover operator to produce destructive offspring (breaking apart good spatial clusters). A higher mutation rate or a spatially-aware crossover mechanism is required for such dispersed maps.

### 4.4. Neighborhood Operators: The Necessity of Deletion

The Neighbor Function was engineered with three stochastic operators: `Move` (Position adjustment), `Add` (Coverage expansion), and `Remove` (Resource optimization).
Without the `Remove` operator, the algorithms would suffer from "Resource Bloat." An initial state might randomly deploy 15 sensors. Even if 8 sensors are sufficient to cover all targets, without `Remove`, the remaining 7 sensors would permanently inflate the cost function. The dynamic inclusion of `Remove` enabled both SA and GA to autonomously prune the network topology to its most resource-efficient state.
