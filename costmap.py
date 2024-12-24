import numpy as np
import matplotlib.pyplot as plt 
import imageio  
from const import *


class Costmap:
    """
    Costmap class represents the environment grid for path planning, managing obstacles, start and goal points.

    Attributes:
        width (int): The width of the Costmap grid.
        height (int): The height of the Costmap grid.
        grid (numpy.ndarray): A 2D array representing the Costmap grid where each cell holds a value indicating its state.
        goal (tuple or None): Coordinates of the goal point (x, y).
        start (tuple or None): Coordinates of the start point (x, y).
    """

    def __init__(self, width=100, height=100):
        """
        Initializes the Costmap with a specified width and height. All cells are initially set to NOT_YET_VISITED.

        Args:
            width (int, optional): The width of the Costmap grid. Defaults to 100.
            height (int, optional): The height of the Costmap grid. Defaults to 100.
        """
        self.width = width
        self.height = height
        self.grid = np.full((height, width), NOT_YET_VISITED, dtype=np.uint8)
        self.goal = None
        self.start = None
                
    def add_obstacle(self, x, y):
        """
        Adds an obstacle at the specified (x, y) position if within bounds.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
        """
        if self.is_within_bounds(x, y):
            self.grid[y][x] = OBSTACLE
    
    def remove_obstacle(self, x, y):
        """
        Removes an obstacle from the specified (x, y) position if it exists and is within bounds.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
        """
        if self.is_within_bounds(x, y) and self.grid[y][x] == OBSTACLE:
            self.grid[y][x] = NOT_YET_VISITED
    
    def toggle_obstacle(self, x, y):
        """
        Toggles the obstacle state at the specified (x, y) position. If an obstacle exists, it is removed; otherwise, it is added.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
        """
        if self.is_within_bounds(x, y):
            if self.grid[y][x] == OBSTACLE:
                self.grid[y][x] = NOT_YET_VISITED
            else:
                self.grid[y][x] = OBSTACLE
    
    def is_within_bounds(self, x, y):
        """
        Checks whether the specified (x, y) position is within the bounds of the Costmap grid.

        Args:
            x (int): The x-coordinate to check.
            y (int): The y-coordinate to check.

        Returns:
            bool: True if within bounds, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def reset(self):
        """
        Resets the entire Costmap grid to NOT_YET_VISITED, removing all obstacles, start, and goal points.
        """
        self.grid = np.full((self.height, self.width), NOT_YET_VISITED, dtype=np.uint8)
        self.goal = None
        self.start = None

    def reset_path(self):
        """
        Resets cells marked as VISITED or PATH to NOT_YET_VISITED, excluding the start and goal points.
        """
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] in [VISITED, PATH]:
                    self.grid[y][x] = NOT_YET_VISITED
    
    def is_free(self, x, y):
        """
        Determines if the cell at (x, y) is free (not an obstacle) or is the start/goal point.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            bool: True if the cell is free or is the start/goal point, False otherwise.
        """
        return self.grid[y][x] in [NOT_YET_VISITED, GOAL, START]
    
    def load_map(self, filename):
        """
        Loads a Costmap grid from a PGM file. If the loaded map size differs from the current Costmap size,
        it warns the user and loads as much as possible without exceeding the Costmap boundaries.

        Args:
            filename (str): The path to the PGM file to load.
        """
        try:
            loaded_grid = imageio.imread(filename)
            if loaded_grid.shape != (self.height, self.width):
                print(f"Warning: The map size in file '{filename}' does not match the specified size ({self.width}x{self.height}).")
            # Load as much as possible without exceeding the Costmap boundaries
            min_height = min(loaded_grid.shape[0], self.height)
            min_width = min(loaded_grid.shape[1], self.width)
            self.grid[:min_height, :min_width] = loaded_grid[:min_height, :min_width]
            print(f"Map successfully loaded from '{filename}'.")
        except Exception as e:
            print(f"Error loading map from '{filename}': {e}")
    
    def set_goal(self, x, y):
        """
        Sets the goal point at the specified (x, y) position if it is within bounds and free. 
        Removes the previous goal if it exists.

        Args:
            x (int): The x-coordinate of the goal cell.
            y (int): The y-coordinate of the goal cell.
        """
        if self.is_within_bounds(x, y) and self.is_free(x, y):
            if self.goal:
                self.grid[self.goal[1]][self.goal[0]] = NOT_YET_VISITED
            self.goal = (x, y)
            self.grid[y][x] = GOAL
    
    def set_start(self, x, y):
        """
        Sets the start point at the specified (x, y) position if it is within bounds and free. 
        Removes the previous start if it exists.

        Args:
            x (int): The x-coordinate of the start cell.
            y (int): The y-coordinate of the start cell.
        """
        if self.is_within_bounds(x, y) and self.is_free(x, y):
            if self.start:
                self.grid[self.start[1]][self.start[0]] = NOT_YET_VISITED
            self.start = (x, y)
            self.grid[y][x] = START