# src/algorithms/bfs.py

import collections
from src.problems.grid_problem import Node, get_neighbors, reconstruct_path


def solve(start_pos, goal_pos, grid, rows, cols, update_ui=None):
    """
    Breadth-First Search (BFS) Implementation.
    Guarantees the shortest path in an unweighted grid.
    """
    # Initialize the starting node
    start_node = Node(start_pos[0], start_pos[1])

    # Use a Queue (First-In-First-Out) for BFS
    queue = collections.deque([start_node])

    # Keep track of visited nodes to avoid cycles
    visited = set()
    visited.add(start_pos)

    nodes_explored = 0

    while queue:
        current = queue.popleft()
        nodes_explored += 1

        # Update the UI every 10 steps for visualization speed
        if update_ui and nodes_explored % 10 == 0:
            update_ui(current)

        # Check if the goal is reached
        if (current.r, current.c) == goal_pos:
            return reconstruct_path(current), nodes_explored

        # Expand neighbors
        for nr, nc in get_neighbors(current, grid, rows, cols):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                new_node = Node(nr, nc, parent=current)
                queue.append(new_node)

                # Optional: visual update for the frontier
                if update_ui: update_ui(new_node)

    # Goal not found
    return None, nodes_explored