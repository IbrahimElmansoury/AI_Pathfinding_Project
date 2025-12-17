# src/algorithms/greedy.py

import heapq
from src.problems.grid_problem import Node, get_neighbors, reconstruct_path


def heuristic(r, c, goal_pos):
    # Manhattan Distance
    return abs(r - goal_pos[0]) + abs(c - goal_pos[1])


def solve(start_pos, goal_pos, grid, rows, cols, update_ui=None):
    """
    Greedy Best-First Search Implementation.
    Uses Priority Queue ordered ONLY by heuristic h(n).
    Ignores path cost g(n).
    """
    h_start = heuristic(start_pos[0], start_pos[1], goal_pos)

    # We pass cost=0 because Greedy doesn't care about the past cost
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
                new_h = heuristic(nr, nc, goal_pos)

                # Note: Cost remains 0, so sorting is purely based on h(n)
                new_node = Node(nr, nc, parent=current, cost=0, heuristic=new_h)
                heapq.heappush(pq, new_node)

    return None, nodes_explored