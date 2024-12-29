import numpy as np
import matplotlib.pyplot as plt
from heapq import heappush, heappop
from costmap.costmap import Costmap
from const import *


class Planner:
    """
    Planner class implements the A* algorithm for pathfinding on a given Costmap.

    Attributes:
        costmap (Costmap): An instance of the Costmap class representing the environment.
    """

    def __init__(self, costmap: Costmap):
        """
        Initializes the Planner with a specific Costmap.

        Args:
            costmap (Costmap): The Costmap instance to be used for planning.
        """
        self.costmap = costmap

    def heuristic(self, a: tuple, b: tuple):
        """
        Calculates the Manhattan distance heuristic between two points.

        Args:
            a (tuple): The first point as (x, y).
            b (tuple): The second point as (x, y).

        Returns:
            int: The Manhattan distance between point a and point b.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, node: tuple):
        """
        Retrieves all valid neighboring nodes (4-connected) for a given node.

        Args:
            node (tuple): The current node as (x, y).

        Returns:
            list: A list of neighboring nodes that are within bounds and free.
        """
        neighbors = []
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4-connected grid
        for dx, dy in dirs:
            x2, y2 = node[0] + dx, node[1] + dy
            if self.costmap.is_within_bounds(x2, y2) and self.costmap.is_free(x2, y2):
                neighbors.append((x2, y2))
        return neighbors

    def a_star(self, start: tuple, goal: tuple):
        """
        Executes the A* pathfinding algorithm from start to goal.

        Args:
            start (tuple): The starting node as (x, y).
            goal (tuple): The goal node as (x, y).

        Returns:
            list or None: A list of nodes representing the path from start to goal, or None if no path is found.
        """
        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        closed_set = set()

        while open_set:
            current = heappop(open_set)[1]

            if current == goal:
                return self.reconstruct_path(came_from, current)

            closed_set.add(current)
            self.costmap.grid[current[1]][current[0]
                                          ] = VISITED  # Mark as visited

            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue
                # Assume cost=1 for movement
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + \
                        self.heuristic(neighbor, goal)
                    heappush(open_set, (f_score[neighbor], neighbor))

        return None  # No path found

    def reconstruct_path(self, came_from: dict, current: tuple):
        """
        Reconstructs the path from the goal to the start using the came_from map.

        Args:
            came_from (dict): A mapping from nodes to their predecessors.
            current (tuple): The current node (typically the goal node).

        Returns:
            list: A list of nodes representing the path from start to goal.
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path


class PathVisualizer:
    """
    PathVisualizer class handles the visualization of the Costmap and the planned path using Matplotlib.

    Attributes:
        costmap (Costmap): An instance of the Costmap class representing the environment.
        planner (Planner): An instance of the Planner class used for pathfinding.
        fig (Figure): The Matplotlib figure object.
        ax (Axes): The Matplotlib axes object.
        cmap (Colormap): The color map used for displaying the Costmap.
        im (AxesImage): The image object representing the Costmap on the axes.
        mode (str): Current mode of the visualizer ('start' or 'goal').
        path (list or None): The planned path as a list of nodes, or None if no path is found.
    """

    def __init__(self, costmap: Costmap, planner: Planner):
        """
        Initializes the PathVisualizer with a specific Costmap and Planner.

        Args:
            costmap (Costmap): The Costmap instance to visualize.
            planner (Planner): The Planner instance to use for pathfinding.
        """
        self.costmap = costmap
        self.planner = planner
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.cmap = plt.cm.gray
        self.im = self.ax.imshow(
            self.costmap.grid, cmap=self.cmap, origin='lower', vmin=0, vmax=255)
        self.ax.set_xticks(np.arange(-0.5, self.costmap.width, 1), minor=True)
        self.ax.set_yticks(np.arange(-0.5, self.costmap.height, 1), minor=True)
        self.ax.grid(which='minor', color='lightgrey',
                     linestyle='-', linewidth=0.5)
        self.mode = 'start'
        self.path = None
        self.cid_click = self.fig.canvas.mpl_connect(
            'button_press_event', self.onclick)
        self.cid_key = self.fig.canvas.mpl_connect(
            'key_press_event', self.onkey)
        self.update_display()

    def onkey(self, event):
        """
        Handles key press events to switch modes or perform actions.

        Args:
            event (KeyEvent): The key press event.
        """
        if event.key == '1':
            self.mode = 'start'
            print("Mode: Set Start Point")
        elif event.key == '2':
            self.mode = 'goal'
            print("Mode: Set Goal Point")
        elif event.key == '3':
            self.run_planner()
        elif event.key == '4':
            self.reset_map()
        elif event.key == 'q':
            plt.close(self.fig)

    def onclick(self, event):
        """
        Handles mouse click events to set the start or goal point based on the current mode.

        Args:
            event (MouseEvent): The mouse click event.
        """
        if event.inaxes != self.ax:
            return
        x, y = int(round(event.xdata)), int(round(event.ydata))
        if not self.costmap.is_within_bounds(x, y):
            return
        if self.mode == 'start':
            self.costmap.set_start(x, y)
        elif self.mode == 'goal':
            self.costmap.set_goal(x, y)
        self.update_display()

    def run_planner(self):
        """
        Executes the A* planner to find a path from the start to the goal.
        """
        if not self.costmap.start or not self.costmap.goal:
            print("Please set both start point and goal before running the planner.")
            return
        self.costmap.reset_path()  # Reset previous path markings
        path = self.planner.a_star(self.costmap.start, self.costmap.goal)
        if path:
            print("Path found:")
            print(path)
            self.path = path
        else:
            print("No path found.")
            self.path = None
        self.update_display()

    def reset_map(self):
        """
        Resets the current path on the Costmap.
        """
        self.costmap.reset_path()
        self.path = None
        self.update_display()
        print("Path has been reset.")

    def update_display(self):
        """
        Updates the visualization to reflect the current state of the Costmap and the planned path.
        """
        # Update the grid data
        display_grid = np.copy(self.costmap.grid)
        self.im.set_data(display_grid)
        self.im.set_clim(vmin=0, vmax=255)

        # Remove existing path lines
        lines = [line for line in self.ax.lines if line.get_label() == 'Path']
        for line in lines:
            line.remove()

        # Plot the path if it exists
        if self.path:
            # Extract x and y coordinates
            x_coords = [x for (x, y) in self.path]
            y_coords = [y for (x, y) in self.path]
            self.ax.plot(x_coords, y_coords, color='green',
                         linewidth=2, label='Path', zorder=2)

        # Remove existing scatter plots for start and goal
        scatters = [scatter for scatter in self.ax.collections if scatter.get_label() in [
            'Start', 'Goal']]
        for scatter in scatters:
            scatter.remove()

        # Plot start and goal on top
        if self.costmap.start:
            self.ax.scatter(self.costmap.start[0], self.costmap.start[1],
                            c='blue', marker='o', s=100, label='Start', zorder=3)
        if self.costmap.goal:
            self.ax.scatter(self.costmap.goal[0], self.costmap.goal[1],
                            c='red', marker='x', s=100, label='Goal', zorder=3)

        # Update the legend
        handles, labels = self.ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        self.ax.legend(by_label.values(), by_label.keys(),
                       bbox_to_anchor=(1.05, 1), loc='upper left')

        self.fig.canvas.draw_idle()

    def show(self):
        """
        Displays the visualization window and prints instructions for the user.
        """
        # Instructions
        print("=== Path Planning Mode ===")
        print("Press '1' to set the Start Point")
        print("Press '2' to set the Goal Point")
        print("Press '3' to run the A* Planner")
        print("Press '4' to reset the Path")
        print("Press 'q' to exit")
        plt.show()


def main():
    """
    The main function to run the path planning visualization.
    """
    filename = input("Import Costmap file (e.g., 'obstacles.pgm'): ")
    costmap = Costmap()
    costmap.load_map(filename)
    planner = Planner(costmap)
    visualizer = PathVisualizer(costmap, planner)
    visualizer.show()


if __name__ == "__main__":
    main()
