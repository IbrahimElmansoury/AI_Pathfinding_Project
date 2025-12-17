# src/algorithms/astar.py

import heapq
from src.problems.grid_problem import Node, get_neighbors, reconstruct_path


def heuristic(r, c, goal_pos):
    """
    Manhattan Distance Heuristic.
    Formula: |x1 - x2| + |y1 - y2|
    Admissible for 4-directional grid movement.
    """
    return abs(r - goal_pos[0]) + abs(c - goal_pos[1])


def solve(start_pos, goal_pos, grid, rows, cols, update_ui=None):
    """
    A* Search Implementation.
    Uses a Priority Queue ordered by f(n) = g(n) + h(n).
    """
    # Calculate initial heuristic
    h_start = heuristic(start_pos[0], start_pos[1], goal_pos)
    start_node = Node(start_pos[0], start_pos[1], cost=0, heuristic=h_start)

    pq = []
    heapq.heappush(pq, start_node)

    visited = set()
    nodes_explored = 0

    while pq:
        current = heapq.heappop(pq)

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
                new_cost = current.cost + 1
                new_h = heuristic(nr, nc, goal_pos)

                # Create node with f(n) calculated inside __init__
                new_node = Node(nr, nc, parent=current, cost=new_cost, heuristic=new_h)
                heapq.heappush(pq, new_node)

    return None, nodes_explored