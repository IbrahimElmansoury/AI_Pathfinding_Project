import unittest
import sys
import os

# Add the project root directory to the system path to allow importing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.algorithms import bfs, dfs, ucs, astar, greedy
from src.problems.grid_problem import Node


class TestAlgorithms(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment before each test case.
        We create a small 5x5 empty grid for testing purposes.
        """
        self.rows = 5
        self.cols = 5
        # Create a 5x5 grid filled with 0s (Empty)
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.start = (0, 0)
        self.goal = (4, 4)

    def test_bfs_optimality(self):
        """Test that BFS finds a path and that the path cost is optimal in an unweighted grid."""
        path, nodes = bfs.solve(self.start, self.goal, self.grid, self.rows, self.cols)

        self.assertIsNotNone(path, "BFS failed to find a path in an empty grid")

        # The optimal distance in a 5x5 grid from (0,0) to (4,4) is 8 steps (Manhattan distance)
        self.assertEqual(len(path) - 1, 8, "BFS path cost is not optimal")

    def test_astar_optimality(self):
        """Test that A* Search finds the optimal path."""
        path, nodes = astar.solve(self.start, self.goal, self.grid, self.rows, self.cols)

        self.assertIsNotNone(path, "A* failed to find a path")
        self.assertEqual(len(path) - 1, 8, "A* path cost is not optimal")

    def test_dfs_found(self):
        """Test that DFS finds a solution (optimality is not guaranteed)."""
        path, nodes = dfs.solve(self.start, self.goal, self.grid, self.rows, self.cols)
        self.assertIsNotNone(path, "DFS failed to find a path")

    def test_obstacle_avoidance(self):
        """Test that algorithms successfully navigate around obstacles."""
        # Fix: Move obstacles to the center (2,2) instead of trapping the start (0,0)
        # Old code trapped (0,0) by blocking (0,1) and (1,0)

        self.grid[2][2] = 1
        self.grid[2][3] = 1
        self.grid[3][2] = 1

        # BFS should find an alternative route around these center walls
        path, nodes = bfs.solve(self.start, self.goal, self.grid, self.rows, self.cols)
        self.assertIsNotNone(path, "Algorithm failed to navigate around obstacles")


if __name__ == '__main__':
    unittest.main()