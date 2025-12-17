# src/problems/grid_problem.py

class Node:
    """
    Represents a single cell (state) in the grid.
    Used by search algorithms to track costs and parents.
    """

    def __init__(self, r, c, parent=None, cost=0, heuristic=0):
        self.r = r  # Row index
        self.c = c  # Column index
        self.parent = parent  # The previous node (used to reconstruct the path)

        self.cost = cost  # g(n): Cost from start to current node
        self.heuristic = heuristic  # h(n): Estimated cost from current node to goal
        self.total_cost = cost + heuristic  # f(n) = g(n) + h(n)

    def __lt__(self, other):
        """
        Comparison method for Priority Queues (used in A*, UCS, Greedy).
        Nodes with lower 'total_cost' are prioritized.
        """
        return self.total_cost < other.total_cost


def get_neighbors(node, grid, rows, cols):
    """
    Returns a list of valid adjacent coordinates (neighbors) for a given node.
    It checks grid boundaries and obstacles.
    """
    # Directions: Down, Right, Up, Left
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    neighbors = []

    for dr, dc in directions:
        nr, nc = node.r + dr, node.c + dc

        # Check 1: Within Grid Boundaries
        if 0 <= nr < rows and 0 <= nc < cols:
            # Check 2: Not an Obstacle (0 = Empty, 1 = Wall)
            if grid[nr][nc] == 0:
                neighbors.append((nr, nc))

    return neighbors


def reconstruct_path(node):
    """
    Backtracks from the goal node to the start node using 'parent' pointers
    to generate the final path list.
    """
    path = []
    curr = node
    while curr:
        path.append((curr.r, curr.c))
        curr = curr.parent  # Move back to the previous node
    return path[::-1]  # Reverse list to show path from Start -> Goal