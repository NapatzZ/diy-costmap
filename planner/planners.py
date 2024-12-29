"""
Implementation of three planners: A*, Dijkstra, and RRT.
"""

import heapq
import random
import numpy as np
from abc import ABC, abstractmethod
from const import (
    FREE,
    OBSTACLE,
    UNKNOWN,
    VISITED,
    START,
    GOAL
)


class BasePlanner(ABC):
    """
    Abstract base class for planners.
    """

    def __init__(self, costmap):
        """
        Initialize with a given costmap.
        """
        self.costmap = costmap

    @abstractmethod
    def plan(self, start: tuple, goal: tuple):
        """
        Plan a path from start to goal.

        Args:
            start (tuple): (x, y) of the start cell.
            goal (tuple): (x, y) of the goal cell.

        Returns:
            list or None: A list of (x, y) cells forming a path, or None if no path found.
        """
        pass


class AStarPlanner(BasePlanner):
    """
    A* planner using Manhattan distance.
    """

    def heuristic(self, a: tuple, b: tuple) -> float:
        """
        Manhattan distance.

        Args:
            a (tuple): (x, y)
            b (tuple): (x, y)

        Returns:
            float: Manhattan distance.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, node: tuple) -> list:
        """
        Get valid 4-direction neighbors.

        Args:
            node (tuple): (x, y)

        Returns:
            list: list of neighbor (x, y).
        """
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        x, y = node
        neighbors = []
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.costmap.width and 0 <= ny < self.costmap.height:
                if self.costmap.grid[ny][nx] != OBSTACLE:
                    neighbors.append((nx, ny))
        return neighbors

    def plan(self, start: tuple, goal: tuple):
        """
        A* search from start to goal.

        Args:
            start (tuple): (x, y)
            goal (tuple): (x, y)

        Returns:
            list or None: path as list of (x, y) or None if no path found.
        """
        open_set = []
        came_from = {}
        gscore = {start: 0}
        fscore = {start: self.heuristic(start, goal)}

        heapq.heappush(open_set, (fscore[start], start))

        while open_set:
            _, current = heapq.heappop(open_set)
            cx, cy = current
            if current == goal:
                return self._reconstruct_path(came_from, current)

            # Mark visited if not start or goal
            if self.costmap.grid[cy][cx] not in [START, GOAL]:
                self.costmap.grid[cy][cx] = VISITED

            for nbr in self.get_neighbors(current):
                tentative_g = gscore[current] + 1
                if nbr not in gscore or tentative_g < gscore[nbr]:
                    came_from[nbr] = current
                    gscore[nbr] = tentative_g
                    fscore[nbr] = tentative_g + self.heuristic(nbr, goal)
                    heapq.heappush(open_set, (fscore[nbr], nbr))

        return None

    def _reconstruct_path(self, came_from: dict, current: tuple) -> list:
        """
        Reconstruct path from came_from dict.

        Args:
            came_from (dict): map of node -> predecessor
            current (tuple): goal node

        Returns:
            list: list of nodes (x, y)
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path


class DijkstraPlanner(BasePlanner):
    """
    Dijkstra's algorithm for path planning.
    """

    def get_neighbors(self, node: tuple) -> list:
        """
        4-direction neighbors excluding obstacles.
        """
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        x, y = node
        neighbors = []
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.costmap.width and 0 <= ny < self.costmap.height:
                if self.costmap.grid[ny][nx] != OBSTACLE:
                    neighbors.append((nx, ny))
        return neighbors

    def plan(self, start: tuple, goal: tuple):
        """
        Run Dijkstra from start to goal.

        Args:
            start (tuple): (x, y)
            goal (tuple): (x, y)

        Returns:
            list or None: path or None if not found.
        """
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        dist = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)
            cx, cy = current

            if current == goal:
                return self._reconstruct_path(came_from, current)

            if self.costmap.grid[cy][cx] not in [START, GOAL]:
                self.costmap.grid[cy][cx] = VISITED

            for nbr in self.get_neighbors(current):
                cost = dist[current] + 1
                if nbr not in dist or cost < dist[nbr]:
                    dist[nbr] = cost
                    came_from[nbr] = current
                    heapq.heappush(open_set, (cost, nbr))

        return None

    def _reconstruct_path(self, came_from: dict, current: tuple) -> list:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path


class RRTPlanner(BasePlanner):
    """
    Rapidly-exploring Random Tree for grid-based path planning.
    """

    def __init__(self, costmap, max_iter: int = 1000):
        super().__init__(costmap)
        self.max_iter = max_iter

    def plan(self, start: tuple, goal: tuple):
        """
        RRT plan from start to goal. 
        Randomly samples cells, grows a tree step by step.
        """
        tree = {start: None}
        for _ in range(self.max_iter):
            rand_node = self._sample_node()
            nearest = self._nearest(rand_node, tree.keys())
            new_node = self._steer(nearest, rand_node)

            if self._is_free(new_node):
                tree[new_node] = nearest
                x, y = new_node
                if self.costmap.grid[y][x] not in [START, GOAL]:
                    self.costmap.grid[y][x] = VISITED

                if self._distance(new_node, goal) <= 1:
                    tree[goal] = new_node
                    return self._reconstruct_path(tree, goal)
        return None

    def _sample_node(self) -> tuple:
        """
        Randomly sample a node within the costmap.
        """
        x = random.randint(0, self.costmap.width - 1)
        y = random.randint(0, self.costmap.height - 1)
        return x, y

    def _nearest(self, rand_node: tuple, nodes: list) -> tuple:
        """
        Find the nearest node in 'nodes' to 'rand_node'.
        """
        return min(nodes, key=lambda n: self._distance(n, rand_node))

    def _steer(self, from_node: tuple, to_node: tuple) -> tuple:
        """
        Move one step from from_node towards to_node.
        """
        x1, y1 = from_node
        x2, y2 = to_node
        dx, dy = x2 - x1, y2 - y1
        step_x = x1 + np.sign(dx) if dx != 0 else x1
        step_y = y1 + np.sign(dy) if dy != 0 else y1
        return step_x, step_y

    def _is_free(self, node: tuple) -> bool:
        """
        Check if the cell is not obstacle.
        """
        x, y = node
        if 0 <= x < self.costmap.width and 0 <= y < self.costmap.height:
            return self.costmap.grid[y][x] != OBSTACLE
        return False

    def _distance(self, a: tuple, b: tuple) -> float:
        """
        Euclidean distance between two nodes.
        """
        return np.hypot(a[0] - b[0], a[1] - b[1])

    def _reconstruct_path(self, tree: dict, current: tuple) -> list:
        """
        Reconstruct the path from the tree dict.
        """
        path = [current]
        while tree[current] is not None:
            current = tree[current]
            path.append(current)
        path.reverse()
        return path