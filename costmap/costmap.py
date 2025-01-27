from const import Config

class Costmap:
    """
    Stores occupancy grid data in a 2D list.
    Each cell can hold a color/state such as FREE, OBSTACLE, START, etc.
    """

    def __init__(self, rows, cols):
        """
        Initialize the costmap with the specified number of rows and columns.
        All cells start as FREE.
        """
        self.rows = rows
        self.cols = cols

        self.FREE = Config.get("FREE")
        self.OBSTACLE = Config.get("OBSTACLE")
        self.VISITED = Config.get("VISITED")
        self.START = Config.get("START")
        self.GOAL = Config.get("GOAL")

        self.grid = [
            [self.FREE for _ in range(cols)] for _ in range(rows)
        ]

    def reset(self):
        """
        Reset the costmap so that all cells become FREE.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = self.FREE

