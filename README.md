# 🤖 AI Pathfinding Visualizer

An interactive Python application to visualize and compare various Artificial Intelligence search algorithms in a grid-based environment. This project demonstrates the theoretical and practical differences between Uninformed, Informed, and Local search strategies.

---

## 📋 Features

* **Interactive Grid:** User-friendly interface to draw obstacles (walls), set Start (Green), and Goal (Red) positions.
* **7 Implemented Algorithms:**
    * **Uninformed:** BFS, DFS, IDS.
    * **Informed:** A* Search (Manhattan Heuristic), Greedy Best-First Search, Uniform-Cost Search (UCS).
    * **Local Search:** Hill Climbing.
* **Real-Time Visualization:** Watch the algorithms explore the map step-by-step (visited nodes in light blue, final path in yellow).
* **Performance Metrics:** Displays execution time, number of nodes explored, and total path cost.
* **Comparison Charts:** Automatically generates bar charts to compare the efficiency of different algorithms.
* **Auto-Logging:** Saves experiment results to CSV and captures screenshots automatically for analysis.

---

## 🛠️ Prerequisites & Installation

Ensure you have **Python 3.x** installed. You will also need the following libraries:

1.  **Install Dependencies:**
    ```bash
    pip install matplotlib
    ```
    *(Optional: Install `Pillow` for automatic screenshot saving)*
    ```bash
    pip install Pillow
    ```

---

## 🚀 How to Run

### 1. Run the Main Application (GUI)
To launch the visualization interface:
```bash
python src/main.py
```

### 2. Run Unit Tests

To verify the correctness of the algorithms (optimality and obstacle avoidance):

```bash
python tests/test_algorithms.py
```

---

## 🎮 Controls

| Action | Control | Description |
| --- | --- | --- |
| **Set Start Node** | Right Click | Places the starting point (Green) |
| **Set Goal Node** | Shift + Left Click | Places the target point (Red) |
| **Draw Walls** | Left Click (Drag) | Draws obstacles/walls (Black) |
| **Run Search** | Button | Executes the selected algorithm |
| **Compare Charts** | Button | Generates performance comparison graphs |

---

## 📂 Project Structure

```text
AI_Pathfinding_Project/
├── src/
│   ├── algorithms/       # Implementation of BFS, DFS, A*, etc.
│   ├── problems/         # Node class and Grid definitions
│   └── main.py           # Main GUI application & entry point
├── tests/
│   └── test_algorithms.py # Automated Unit Tests
├── results/              # Auto-saved Screenshots, CSV logs, and Charts
├── README.md             # Project Documentation
└── CONTRIBUTORS.md       # Team roles and details
```

---



---

## 📊 Algorithm Comparison

This project allows you to compare the performance of different search algorithms across multiple metrics:

* **Time Complexity:** Actual execution time in seconds
* **Space Complexity:** Number of nodes explored during search
* **Path Optimality:** Total cost of the solution path found
* **Completeness:** Whether the algorithm finds a solution if one exists

---

## 🧪 Testing

The project includes comprehensive unit tests to ensure:

1. **Correctness:** All algorithms find valid paths when they exist
2. **Optimality:** Optimal algorithms (BFS, A*, UCS) find the shortest paths
3. **Obstacle Handling:** All algorithms properly avoid walls and obstacles
4. **Edge Cases:** Algorithms handle unreachable goals and edge scenarios

Run tests with:
```bash
python tests/test_algorithms.py
```

---

## 📈 Results & Analysis

All experiment results are automatically saved in the `results/` directory:

* **CSV Files:** Detailed performance metrics for each algorithm run
* **Screenshots:** Visual captures of the grid state and path found
* **Comparison Charts:** Bar graphs comparing time, nodes explored, and path cost

---

## 🔧 Customization

You can easily customize the project:

* **Grid Size:** Modify grid dimensions in `main.py`
* **Algorithm Parameters:** Adjust heuristics and cost functions in `algorithms/`
* **Visualization Speed:** Change animation delay for step-by-step visualization
* **New Algorithms:** Add custom search algorithms by following the existing structure

---

## 📝 Notes

* The **Manhattan Heuristic** is used for A* and Greedy Best-First Search (suitable for grid-based movement)
* **Hill Climbing** may get stuck in local optima and not always find the optimal path
* **IDS (Iterative Deepening Search)** combines the benefits of BFS and DFS with lower memory usage

---

### 🎯 Getting Started Commands

```bash
# Clone the repository
git clone <repository-url>

# Navigate to project directory
cd AI_Pathfinding_Project

# Install dependencies
pip install matplotlib

# Run the application
python src/main.py

# Run tests
python tests/test_algorithms.py
```

---

```