import numpy as np
import matplotlib.pyplot as plt  # type: ignore
import imageio  # type: ignore
from const import *


class Costmap:
    def __init__(self, width: int = MAX_WIDHT_PIXEL, height: int = MAX_HEIGHT_PIXEL):
        self._width = width
        self._height = height
        self._grid = np.full((self._height, self._width),
                             NOT_YET_VISITED, dtype=np.uint8)

    def add_obstracle(self, x: int, y: int):
        if self._is_within_bound(x, y):
            self._grid[y][x] = OBSTACLE

    def remove_obstracle(self, x: int, y: int):
        if self._is_within_bound(x, y) and self._grid[y][x] == OBSTACLE:
            self._grid[y][x] == NOT_YET_VISITED

    def _is_within_bound(self, x: int, y: int):
        return 0 <= x < self._width and 0 <= y < self._height

    def reset(self):
        self._grid = np.full((self._height, self._width),
                             NOT_YET_VISITED, dtype=np.uint8)

    def toggle_obstacle(self, x: int, y: int):
        if self._grid[y][x] == OBSTACLE:
            self._grid[y][x] == NOT_YET_VISITED
        else:
            self._grid[y][x] == OBSTACLE


class CostmapVisualizer:
    def __init__(self, costmap: Costmap):
        self.costmap = costmap
        