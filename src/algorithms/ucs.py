# src/algorithms/ucs.py

import heapq
from src.problems.grid_problem import Node, get_neighbors, reconstruct_path


def solve(start_pos, goal_pos, grid, rows, cols, update_ui=None):
    """
    Uniform-Cost Search (UCS) Implementation.
    Uses a Priority Queue ordered by path cost g(n).
    """
    start_node = Node(start_pos[0], start_pos[1], cost=0)

    # Priority Queue stores tuples or objects. Node class handles comparison.
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

        if update_ui and nodes_explored % 10 == 0:
            update_ui(current)

        if (current.r, current.c) == goal_pos:
            return reconstruct_path(current), nodes_explored

        for nr, nc in get_neighbors(current, grid, rows, cols):
            if (nr, nc) not in visited:
                # Cost is incremented by 1 for each step
                new_cost = current.cost + 1
                new_node = Node(nr, nc, parent=current, cost=new_cost)
                heapq.heappush(pq, new_node)

    return None, nodes_explored