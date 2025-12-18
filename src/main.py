import sys
import os
import time
import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt  # Used for comparison charts

# Try importing Pillow for screenshots; handle the case if it's not installed
try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None
    print("Pillow library not found. Screenshots will be disabled. (Run 'pip install Pillow' to enable)")

# Add the project root directory to the system path to allow module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the implemented algorithms
from src.algorithms import bfs, dfs, ucs, ids, astar, greedy, hill_climbing

# --- UI Colors ---
COLOR_EMPTY = "white"
COLOR_WALL = "black"
COLOR_START = "green"
COLOR_GOAL = "red"
COLOR_PATH = "yellow"
COLOR_VISITED = "lightblue"


class PathFindingApp:
    def __init__(self, root):
        """
        Initialize the Main Application Window and Grid Settings.
        """
        self.root = root
        self.root.title("AI Pathfinding Project - Search Algorithms Comparison")

        # Grid Configuration (20x20)
        self.rows = 20
        self.cols = 20
        self.cell_size = 30

        # Initialize grid data (0 = Empty, 1 = Wall)
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.rects = [[None] * self.cols for _ in range(self.rows)]

        self.start_pos = None
        self.goal_pos = None

        # Dictionary to store performance metrics for comparison
        self.comparison_data = {}

        self.setup_ui()
        self.draw_grid()

    def setup_ui(self):
        """
        Setup the User Interface (Side Panel, Buttons, Labels, Canvas).
        """
        # --- Control Panel (Right Side) ---
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(control_frame, text="Select Algorithm:", font=("Arial", 11, "bold")).pack(pady=5)

        self.algo_var = tk.StringVar()
        # Map friendly names to actual algorithm modules
        self.algos = {
            "BFS (Breadth-First)": bfs,
            "DFS (Depth-First)": dfs,
            "UCS (Uniform-Cost)": ucs,
            "IDS (Iterative Deepening)": ids,
            "A* Search (Manhattan)": astar,
            "Greedy Best-First": greedy,
            "Hill Climbing": hill_climbing
        }
        self.cb = ttk.Combobox(control_frame, textvariable=self.algo_var, values=list(self.algos.keys()),
                               state="readonly")
        self.cb.current(0)
        self.cb.pack(pady=5)

        # Action Buttons
        tk.Button(control_frame, text="Run Search", command=self.run, bg="#4CAF50", fg="white",
                  font=("Arial", 10, "bold")).pack(pady=10, fill=tk.X)
        tk.Button(control_frame, text="Compare Charts", command=self.show_charts, bg="#2196F3", fg="white").pack(pady=5,
                                                                                                                 fill=tk.X)
        tk.Button(control_frame, text="Clear Path", command=self.clear_path).pack(pady=2, fill=tk.X)
        tk.Button(control_frame, text="Reset Grid", command=self.reset).pack(pady=2, fill=tk.X)

        # Metrics Display Section
        self.stats_frame = tk.LabelFrame(control_frame, text="Metrics", padx=5, pady=5, font=("Arial", 10))
        self.stats_frame.pack(pady=20, fill=tk.X)

        self.l_time = tk.Label(self.stats_frame, text="Time: 0 ms", fg="blue")
        self.l_time.pack(anchor="w")
        self.l_nodes = tk.Label(self.stats_frame, text="Nodes Explored: 0")
        self.l_nodes.pack(anchor="w")
        self.l_cost = tk.Label(self.stats_frame, text="Path Cost: 0")
        self.l_cost.pack(anchor="w")
        self.l_status = tk.Label(self.stats_frame, text="Status: Ready", fg="gray")
        self.l_status.pack(pady=5)

        tk.Label(control_frame, text="Controls:\nRight Click: Start\nShift+Click: Goal\nLeft Click: Wall",
                 justify=tk.LEFT, fg="gray").pack(side=tk.BOTTOM)

        # --- Grid Canvas (Left Side) ---
        self.canvas = tk.Canvas(self.root, width=self.cols * self.cell_size, height=self.rows * self.cell_size,
                                bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        # Bind Mouse Events
        self.canvas.bind("<Button-1>", self.handle_click)  # Left Click -> Wall
        self.canvas.bind("<B1-Motion>", self.handle_click)  # Drag -> Wall
        self.canvas.bind("<Button-3>", self.set_start)  # Right Click -> Start
        self.canvas.bind("<Shift-Button-1>", self.set_goal)  # Shift+Left -> Goal

    def draw_grid(self):
        """Initial drawing of the grid cells."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.rects[r][c] = self.canvas.create_rectangle(
                    c * 30, r * 30, (c + 1) * 30, (r + 1) * 30,
                    fill=COLOR_EMPTY, outline="lightgray"
                )

    def handle_click(self, event):
        """Handles placing walls (Obstacles)."""
        r, c = event.y // 30, event.x // 30
        if 0 <= r < self.rows and 0 <= c < self.cols:
            # Prevent overwriting Start or Goal
            if (r, c) != self.start_pos and (r, c) != self.goal_pos:
                self.grid[r][c] = 1
                self.canvas.itemconfig(self.rects[r][c], fill=COLOR_WALL)

    def set_start(self, event):
        """Sets the Start Point (Green)."""
        r, c = event.y // 30, event.x // 30
        if 0 <= r < self.rows and 0 <= c < self.cols:
            if self.start_pos:
                # Reset old start position color
                self.canvas.itemconfig(self.rects[self.start_pos[0]][self.start_pos[1]], fill=COLOR_EMPTY)
            self.start_pos = (r, c)
            self.grid[r][c] = 0  # Start cannot be a wall
            self.canvas.itemconfig(self.rects[r][c], fill=COLOR_START)

    def set_goal(self, event):
        """Sets the Goal Point (Red)."""
        r, c = event.y // 30, event.x // 30
        if 0 <= r < self.rows and 0 <= c < self.cols:
            if self.goal_pos:
                # Reset old goal position color
                self.canvas.itemconfig(self.rects[self.goal_pos[0]][self.goal_pos[1]], fill=COLOR_EMPTY)
            self.goal_pos = (r, c)
            self.grid[r][c] = 0  # Goal cannot be a wall
            self.canvas.itemconfig(self.rects[r][c], fill=COLOR_GOAL)

    def reset(self):
        """Resets the entire grid and metrics history."""
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.start_pos = None
        self.goal_pos = None
        self.comparison_data = {}
        for r in range(self.rows):
            for c in range(self.cols):
                self.canvas.itemconfig(self.rects[r][c], fill=COLOR_EMPTY)
        self.reset_labels()

    def clear_path(self):
        """Clears only the path and visited nodes (keeps walls, Start, Goal)."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 0 and (r, c) != self.start_pos and (r, c) != self.goal_pos:
                    self.canvas.itemconfig(self.rects[r][c], fill=COLOR_EMPTY)
        self.reset_labels()

    def reset_labels(self):
        """Resets the metrics display labels."""
        self.l_time.config(text="Time: 0 ms")
        self.l_nodes.config(text="Nodes Explored: 0")
        self.l_cost.config(text="Path Cost: 0")
        self.l_status.config(text="Status: Ready", fg="gray")

    def ui_update(self, node):
        """Callback function to visualize visited nodes during search."""
        if node and (node.r, node.c) != self.start_pos:
            self.canvas.itemconfig(self.rects[node.r][node.c], fill=COLOR_VISITED)
        self.root.update()

    def save_experiment_data(self, algo_name, time_taken, nodes, cost, is_optimal):
        """
        Automatically saves experiment metrics to a CSV file and captures a screenshot of the maze.
        """
        # 1. Ensure the 'results' directory exists
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        results_dir = os.path.join(base_dir, 'results')

        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # 2. Save numerical metrics to a CSV file (Excel compatible)
        csv_file = os.path.join(results_dir, 'experiment_log.csv')
        file_exists = os.path.isfile(csv_file)

        try:
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                # If the file is new, write the headers first
                if not file_exists:
                    writer.writerow(
                        ['Timestamp', 'Algorithm', 'Time(ms)', 'Nodes Explored', 'Path Cost', 'Optimal?'])

                # Write the current experiment data
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([timestamp, algo_name, f"{time_taken:.4f}", nodes, cost, is_optimal])

            print(f"[-] Saved metrics to {csv_file}")
        except Exception as e:
            print(f"[!] Error saving CSV: {e}")

        # 3. Capture and save a screenshot of the canvas (if Pillow is installed)
        if ImageGrab:
            # Force the UI to update to ensure the drawing is complete
            self.root.update()

            # Generate a unique filename based on the current time
            timestamp_str = datetime.now().strftime('%H-%M-%S')
            img_name = f"{algo_name}_{timestamp_str}.png"
            img_path = os.path.join(results_dir, img_name)

            try:
                # Calculate the coordinates of the canvas on the screen
                x = self.root.winfo_rootx() + self.canvas.winfo_x()
                y = self.root.winfo_rooty() + self.canvas.winfo_y()
                x1 = x + self.canvas.winfo_width()
                y1 = y + self.canvas.winfo_height()

                # Capture the specific area and save it
                ImageGrab.grab().crop((x, y, x1, y1)).save(img_path)
                print(f"[-] Saved screenshot to {img_path}")
            except Exception as e:
                print(f"[!] Error taking screenshot: {e}")

    def run(self):
        """Executes the selected algorithm, updates metrics, and auto-saves results."""
        if not self.start_pos or not self.goal_pos:
            messagebox.showerror("Error", "Please set Start (Right Click) and Goal (Shift+Click)")
            return

        self.clear_path()
        algo_name = self.algo_var.get()
        algo_module = self.algos[algo_name]

        self.l_status.config(text=f"Running {algo_name}...", fg="orange")
        self.root.update()

        # Start Timer
        t0 = time.time()

        # Execute the Algorithm
        path, nodes_count = algo_module.solve(self.start_pos, self.goal_pos, self.grid, self.rows, self.cols,
                                              self.ui_update)

        # Stop Timer
        t1 = time.time()

        exec_time = round((t1 - t0) * 1000, 2)
        cost = len(path) - 1 if path else 0

        # Draw the final path if found
        if path:
            for r, c in path:
                if (r, c) != self.start_pos and (r, c) != self.goal_pos:
                    self.canvas.itemconfig(self.rects[r][c], fill=COLOR_PATH)
                    self.root.update()
                    time.sleep(0.01)  # Small delay for animation
            self.l_status.config(text="Goal Found!", fg="green")
        else:
            self.l_status.config(text="No Path Found!", fg="red")

        # Update UI Labels
        self.l_time.config(text=f"Time: {exec_time} ms")
        self.l_nodes.config(text=f"Nodes Explored: {nodes_count}")
        self.l_cost.config(text=f"Path Cost: {cost}")

        # Save data for chart comparison
        self.comparison_data[algo_name] = {'time': exec_time, 'nodes': nodes_count, 'cost': cost}

        # --- Auto-Save Data ---
        # Determine if the algorithm is theoretically optimal
        optimal_algos = ["BFS (Breadth-First)", "A* Search (Manhattan)", "UCS (Uniform-Cost)",
                         "IDS (Iterative Deepening)"]
        is_optimal = "Yes" if algo_name in optimal_algos else "No"

        # Call the save method
        self.save_experiment_data(algo_name, exec_time, nodes_count, cost, is_optimal)

    def show_charts(self):
        """Displays Bar Charts comparing the performance of executed algorithms and saves the image."""
        if not self.comparison_data:
            messagebox.showinfo("Info", "Run at least two algorithms to compare!")
            return

        names = list(self.comparison_data.keys())
        # Shorten names for the chart (e.g., "BFS (Breadth-First)" -> "BFS")
        short_names = [n.split()[0] for n in names]
        times = [d['time'] for d in self.comparison_data.values()]
        nodes = [d['nodes'] for d in self.comparison_data.values()]

        # Create Bar Charts using Matplotlib
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle('Algorithms Performance Comparison')

        # Chart 1: Execution Time
        ax1.bar(short_names, times, color='skyblue')
        ax1.set_title('Execution Time (ms)')
        ax1.set_ylabel('Milliseconds')

        # Chart 2: Nodes Explored
        ax2.bar(short_names, nodes, color='lightgreen')
        ax2.set_title('Nodes Explored')
        ax2.set_ylabel('Count')

        plt.tight_layout()

        # --- Save Chart to File ---
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        results_dir = os.path.join(base_dir, 'results')

        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        chart_path = os.path.join(results_dir, 'comparison_chart.png')

        # Save the figure
        plt.savefig(chart_path)
        print(f"[-] Chart saved to {chart_path}")

        # Show the chart window
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = PathFindingApp(root)
    root.mainloop()
