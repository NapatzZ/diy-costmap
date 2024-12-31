"""
Interactive visualization for path planning using A*, Dijkstra, or RRT.
"""

import matplotlib.pyplot as plt
import numpy as np

from visualizer.visualizer import Visualizer
from planner.planners import AStarPlanner, DijkstraPlanner, RRTPlanner
from const import (
    FREE,
    OBSTACLE,
    UNKNOWN,
    VISITED,
    START,
    GOAL
)

class PathVisualizer(Visualizer):
    """
    Displays the costmap in a Matplotlib window. Allows the user to set start/goal,
    choose among A*, Dijkstra, or RRT, and see the resulting path. 
    After drawing the path, path cells become FREE in the grid.
    """

    def __init__(self, costmap, map_file: str):
        """
        Initialize the PathVisualizer.

        Args:
            costmap: An instance of the Costmap class to visualize.
            map_file (str): The path to the map file used for reloading if needed.
        """
        super().__init__(costmap, fig_size=(12, 6))

        self.map_file = map_file

        # Create figure with two subplots (reuse left subplot from Visualizer)
        gridspec = self.fig.add_gridspec(1, 2, width_ratios=[3, 1])
        self.ax_map = self.ax  # Reuse the axis from Visualizer
        self.ax_menu = self.fig.add_subplot(gridspec[0, 1])
        self.ax_menu.set_axis_off()

        # Default planner is A*
        self.planner = AStarPlanner(self.costmap)
        self.current_planner_name = 'A*'

        # Path and mode
        self.path = None
        self.mode = 'start'

        # Connect Matplotlib events
        self.cid_click = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.onkey)

        self.update_menu()

    def onclick(self, event):
        """
        Handle mouse clicks on the map. Depending on self.mode,
        set the start or goal on the clicked cell.
        """
        if event.inaxes != self.ax_map:
            return

        x = int(round(event.xdata))
        y = int(round(event.ydata))

        if not self.costmap.is_within_bounds(x, y):
            return

        if self.mode == 'start':
            self.costmap.set_start(x, y)
        elif self.mode == 'goal':
            self.costmap.set_goal(x, y)

        self.update_display()

    def onkey(self, event):
        """
        Handle keyboard shortcuts:

        - '1': Set mode to 'start'
        - '2': Set mode to 'goal'
        - '3': Run the planner
        - 'p': Switch to A* Planner
        - 'd': Switch to Dijkstra Planner
        - 'r': Switch to RRT Planner
        - 'c': Reload the map (if you want to restore or reset path)
        - 'q': Exit the visualization
        """
        if event.key == '1':
            self.mode = 'start'
            print("Mode: Set Start")
        elif event.key == '2':
            self.mode = 'goal'
            print("Mode: Set Goal")
        elif event.key == '3':
            self.run_planner()
        elif event.key == 'p':
            self.switch_planner('A*')
        elif event.key == 'd':
            self.switch_planner('Dijkstra')
        elif event.key == 'r':
            self.switch_planner('RRT')
        elif event.key == 'c':
            self.reset_map()
        elif event.key == 'q':
            plt.close(self.fig)

        self.update_menu()

    def switch_planner(self, planner_name: str):
        """
        Switch among the available planners: 'A*', 'Dijkstra', 'RRT'.

        Args:
            planner_name (str): The name of the planner to switch to.
        """
        if planner_name == 'A*':
            self.planner = AStarPlanner(self.costmap)
        elif planner_name == 'Dijkstra':
            self.planner = DijkstraPlanner(self.costmap)
        elif planner_name == 'RRT':
            self.planner = RRTPlanner(self.costmap)
        else:
            print(f"Unknown planner: {planner_name}")
            return

        self.current_planner_name = planner_name
        print(f"Switched to {planner_name} Planner")

    def run_planner(self):
        """
        Run the selected planner from start to goal. If a path is found,
        self.path is updated, then all path cells (except START/GOAL) are
        set to FREE in the grid, and a green line is drawn on the map.
        """
        if not self.costmap.start or not self.costmap.goal:
            print("Please set both start and goal first.")
            return

        path = self.planner.plan(self.costmap.start, self.costmap.goal)
        if path:
            print("Path found:", path)
            self.path = path

            # ---- Update the costmap so that path cells become FREE ----
            for (px, py) in self.path:
                if self.costmap.grid[py][px] not in [START, GOAL]:
                    self.costmap.grid[py][px] = FREE
        else:
            print("No path found.")
            self.path = None

        self.update_display()

    def reset_map(self):
        """
        Reload the map file or reset the costmap.
        """
        if hasattr(self.costmap, 'reset_path'):
            self.costmap.reset_path(self.map_file)
            print("Map has been reloaded from file.")
        else:
            print("No 'reset_path' method found; fallback to costmap.reset()")
            self.costmap.reset()

        self.path = None
        self.update_display()
        print("Path has been reset (map reloaded if implemented).")

    def update_display(self):
        """
        Refresh the map display. Plots the costmap grid, the path (if any),
        and the start/goal markers.
        """
        super().update_display()

        # Remove old path lines
        old_lines = [line for line in self.ax_map.lines if line.get_label() == 'Path']
        for line in old_lines:
            line.remove()

        # Plot the path (green line)
        if self.path:
            xs = [p[0] for p in self.path]
            ys = [p[1] for p in self.path]
            self.ax_map.plot(xs, ys, color='green', linewidth=2, label='Path')

        # Plot start as a blue circle
        if self.costmap.start:

            # Remove specific scatter elements by label
            old_scatters = [
                scatter for scatter in self.ax_map.collections
                if scatter.get_label() in ['Start']
            ]

            for scatter in old_scatters:
                scatter.remove()

            sx, sy = self.costmap.start
            self.ax_map.scatter(sx, sy, c='blue', marker='o', s=100, label='Start', zorder=3)

        # Plot goal as a red 'x'
        if self.costmap.goal:

            # Remove specific scatter elements by label
            old_scatters = [
                scatter for scatter in self.ax_map.collections
                if scatter.get_label() in ['Goal']
            ]

            for scatter in old_scatters:
                scatter.remove()

            gx, gy = self.costmap.goal
            self.ax_map.scatter(gx, gy, c='red', marker='x', s=100, label='Goal', zorder=3)

        # Update legend
        handles, labels = self.ax_map.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        self.ax_map.legend(by_label.values(), by_label.keys(), loc='upper right')

        self.fig.canvas.draw_idle()
        self.update_menu()

    def update_menu(self):
        """
        Redraw the right-hand menu with current information:
        planner name, mode, start, goal, etc.
        """
        self.ax_menu.clear()
        self.ax_menu.set_axis_off()

        self.ax_menu.text(0.05, 0.95, "Path Planning Menu", fontsize=14, va='top', fontweight='bold')
        lines = [
            f"Planner: {self.current_planner_name}",
            f"Mode: {self.mode}",
            f"Start: {self.costmap.start}",
            f"Goal: {self.costmap.goal}",
            f"Path length: {len(self.path) if self.path else None}"
        ]
        y_pos = 0.85
        for line in lines:
            self.ax_menu.text(0.05, y_pos, line, fontsize=12, va='top')
            y_pos -= 0.07

        self.ax_menu.text(0.05, y_pos, "[Keys]", fontsize=12, va='top', fontweight='bold')
        y_pos -= 0.07

        cmds = [
            "1: Set Start",
            "2: Set Goal",
            "3: Run Planner",
            "p: A*",
            "d: Dijkstra",
            "r: RRT",
            "c: Reset map",
            "q: Exit"
        ]
        for cmd in cmds:
            self.ax_menu.text(0.05, y_pos, cmd, fontsize=10, va='top')
            y_pos -= 0.06

        self.fig.canvas.draw_idle()

    def show(self):
        """
        Print instructions and display the interactive window.
        """
        print("=== Path Planner ===")
        print("Keys:")
        print(" 1 = Set Start")
        print(" 2 = Set Goal")
        print(" 3 = Run Planner")
        print(" p = Switch to A*")
        print(" d = Switch to Dijkstra")
        print(" r = Switch to RRT")
        print(" c = Reset (reload map)")
        print(" q = Exit")
        plt.show()
