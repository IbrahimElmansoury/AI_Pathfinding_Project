# src/algorithms/dfs.py

from src.problems.grid_problem import Node, get_neighbors, reconstruct_path


def solve(start_pos, goal_pos, grid, rows, cols, update_ui=None):
    """
    Depth-First Search (DFS) Implementation.
    Uses a Stack. Does NOT guarantee the shortest path.
    """
    start_node = Node(start_pos[0], start_pos[1])

    # Use a List as a Stack (Last-In-First-Out)
    stack = [start_node]
    visited = set()
    nodes_explored = 0

    while stack:
        current = stack.pop()

        # Skip if already visited
        if (current.r, current.c) in visited:
            continue

        visited.add((current.r, current.c))
        nodes_explored += 1

        if update_ui and nodes_explored % 5 == 0:
            update_ui(current)

        if (current.r, current.c) == goal_pos:
            return reconstruct_path(current), nodes_explored

        for nr, nc in get_neighbors(current, grid, rows, cols):
            if (nr, nc) not in visited:
                stack.append(Node(nr, nc, parent=current))

    return None, nodes_explored