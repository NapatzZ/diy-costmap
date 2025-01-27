class Config:
    """
    Constants for cell states in a 2D occupancy grid, simplified for visualization.
    """
    __ALL_CONFIGS = {
        
        "MAX_WIDTH_PIXEL": 100,
        "MAX_HEIGHT_PIXEL": 100,

        "FREE": (255, 255, 255),   # white
        "OBSTACLE": (0, 0, 0),     # black
        "VISITED": (0, 0, 255),    # blue
        "START": (255, 0, 0),      # red
        "GOAL": (0, 255, 0),       # green
    }

    @classmethod
    def get(cls, key):
        return cls.__ALL_CONFIGS[key]