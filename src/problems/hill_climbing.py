# src/algorithms/hill_climbing.py

from src.problems.grid_problem import Node, get_neighbors


def heuristic(r, c, goal_pos):
    """
    Manhattan Distance Heuristic.
    """
    return abs(r - goal_pos[0]) + abs(c - goal_pos[1])


def solve(start_pos, goal_pos, grid, rows, cols, update_ui=None):
    """
    Hill Climbing Implementation (Steepest Ascent).

    Logic:
    1. Start at the initial state.
    2. Look at all neighbors.
    3. Move to the neighbor with the lowest heuristic (closest to goal).
    4. If no neighbor is better (or all are visited/blocked), STOP.

    * Note: This algorithm does NOT backtrack. It gets stuck in local optima easily.
    """

    # Initialize current node
    current = Node(start_pos[0], start_pos[1])

    path = []
    path.append((current.r, current.c))

    visited = set()
    visited.add((current.r, current.c))

    nodes_explored = 0

    while True:
        nodes_explored += 1

        if update_ui:
            update_ui(current)

        # Check if goal is reached
        if (current.r, current.c) == goal_pos:
            return path, nodes_explored

        # Get all valid neighbors
        neighbors = get_neighbors(current, grid, rows, cols)

        best_neighbor = None
        best_h = float('inf')

        # Find the best neighbor (lowest H)
        for nr, nc in neighbors:
            if (nr, nc) not in visited:
                h = heuristic(nr, nc, goal_pos)
                if h < best_h:
                    best_h = h
                    best_neighbor = Node(nr, nc, parent=current)

        # Decision logic
        if best_neighbor is not None:
            # Move to the best neighbor
            current = best_neighbor
            visited.add((current.r, current.c))
            path.append((current.r, current.c))
        else:
            # Dead end or Local Maximum reached (no better neighbors)
            # Hill Climbing fails here because it cannot backtrack
            return None, nodes_explored