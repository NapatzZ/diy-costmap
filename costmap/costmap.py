"""
Implementation of the Costmap class, storing a 2D grid of cell states.
"""

import numpy as np
import imageio
from const import *


class Costmap:
    """
    Costmap holds a 2D grid (width x height). Each cell is one of several states:
    FREE=255, OBSTACLE=0, UNKNOWN=128, VISITED=254, START=200, GOAL=50.

    Attributes:
        width (int): The width of the grid.
        height (int): The height of the grid.
        grid (np.ndarray): A 2D numpy array holding cell values.
        start (tuple or None): (x, y) for the start cell.
        goal (tuple or None): (x, y) for the goal cell.
    """

    def __init__(self, width: int = 100, height: int = 100):
        """
        Initialize a costmap of the given size. All cells start as UNKNOWN.

        Args:
            width (int, optional): Width of the grid. Defaults to 100.
            height (int, optional): Height of the grid. Defaults to 100.
        """
        self.width = width
        self.height = height
        self.grid = np.full((self.height, self.width), UNKNOWN, dtype=np.uint8)
        self.start = None
        self.goal = None

    def is_within_bounds(self, x: int, y: int) -> bool:
        """
        Check if (x, y) is inside the grid boundaries.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.

        Returns:
            bool: True if within bounds, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def is_free(self, x: int, y: int) -> bool:
        """
        Check if the cell is not an obstacle.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.

        Returns:
            bool: True if the cell is not OBSTACLE (0).
        """
        return self.grid[y][x] != OBSTACLE

    def toggle_obstacle(self, x: int, y: int) -> None:
        """
        Toggle between UNKNOWN (128) and OBSTACLE (0).
        Cells that are FREE (255), VISITED (254), START/GOAL remain unchanged.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.
        """
        if self.is_within_bounds(x, y):
            val = self.grid[y][x]
            if val == OBSTACLE:
                self.grid[y][x] = UNKNOWN
            elif val == UNKNOWN:
                self.grid[y][x] = OBSTACLE

    def set_start(self, x: int, y: int) -> None:
        """
        Set the start cell if it is free. Clears any existing start.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.
        """
        if self.is_within_bounds(x, y) and self.is_free(x, y):
            if self.start:
                sx, sy = self.start
                if self.grid[sy][sx] == START:
                    self.grid[sy][sx] = UNKNOWN
            self.start = (x, y)
            self.grid[y][x] = START

    def set_goal(self, x: int, y: int) -> None:
        """
        Set the goal cell if it is free. Clears any existing goal.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.
        """
        if self.is_within_bounds(x, y) and self.is_free(x, y):
            if self.goal:
                gx, gy = self.goal
                if self.grid[gy][gx] == GOAL:
                    self.grid[gy][gx] = UNKNOWN
            self.goal = (x, y)
            self.grid[y][x] = GOAL

    def load_map(self, filename: str) -> None:
        """
        Load a map from a PGM file. If dimensions differ, clip.

        Args:
            filename (str): The PGM file name.
        """
        try:
            loaded_img = imageio.imread(filename)
            h, w = loaded_img.shape
            min_h = min(h, self.height)
            min_w = min(w, self.width)
            self.grid[:min_h, :min_w] = loaded_img[:min_h, :min_w]
            print(f"Loaded map from '{filename}'")
        except Exception as e:
            print(f"Error loading map: {e}")

    def reset(self) -> None:
        """
        Reset the entire grid to UNKNOWN. Clears start and goal.
        """
        self.grid[:] = UNKNOWN
        self.start = None
        self.goal = None

    def reset_path(self, map_file: str) -> None:
        """
        Reload the map file to restore the original map.
        Keep the same start and goal coordinates and re-assign them.

        Args:
            map_file (str): The map file to reload.
        """
        old_start = self.start
        old_goal = self.goal

        self.load_map(map_file)

        # Re-assign the old start/goal if they are within bounds
        # (But only do so if the old positions are still valid.)
        if old_start:
            sx, sy = old_start
            if self.is_within_bounds(sx, sy) and self.is_free(sx, sy):
                self.set_start(sx, sy)
            else:
                self.start = None

        if old_goal:
            gx, gy = old_goal
            if self.is_within_bounds(gx, gy) and self.is_free(gx, gy):
                self.set_goal(gx, gy)
            else:
                self.goal = None