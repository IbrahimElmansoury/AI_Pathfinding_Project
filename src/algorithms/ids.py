# src/algorithms/ids.py

from src.problems.grid_problem import Node, get_neighbors, reconstruct_path


def dls(node, goal_pos, grid, rows, cols, limit, visited, count_ref):
    """
    Depth-Limited Search (Helper function for IDS).
    Returns path if found, otherwise None.
    """
    count_ref[0] += 1

    if (node.r, node.c) == goal_pos:
        return reconstruct_path(node)

    if limit <= 0:
        return None

    visited.add((node.r, node.c))

    for nr, nc in get_neighbors(node, grid, rows, cols):
        if (nr, nc) not in visited:
            # Recursive call with reduced limit
            # Note: We pass visited.copy() to allow other branches to visit these nodes in different paths
            res = dls(Node(nr, nc, parent=node), goal_pos, grid, rows, cols, limit - 1, visited.copy(), count_ref)
            if res:
                return res
    return None


def solve(start_pos, goal_pos, grid, rows, cols, update_ui=None):
    """
    Iterative Deepening Search (IDS).
    Repeatedly calls DLS with increasing depth limits.
    """
    depth = 0
    # Use a list for count_ref to pass by reference
    total_nodes = [0]

    # Safety limit to prevent infinite loops if goal is unreachable
    max_depth = rows * cols

    while depth <= max_depth:
        visited = set()

        # Force a UI update between iterations
        if update_ui: update_ui(None)

        result = dls(Node(start_pos[0], start_pos[1]), goal_pos, grid, rows, cols, depth, visited, total_nodes)

        if result is not None:
            return result, total_nodes[0]

        depth += 1

    return None, total_nodes[0]