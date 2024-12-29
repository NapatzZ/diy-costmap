"""
Constants for cell states in a 2D occupancy grid.
"""

MAX_WIDHT_PIXEL = 100
MAX_HEIGHT_PIXEL = 100 
FREE = 255      # White
OBSTACLE = 0    # Black
UNKNOWN = 128   # Gray
VISITED = 160   # Slightly off-white (for marking visited cells)
START = 200     # Distinct grayscale for start
GOAL = 50       # Distinct grayscale for goal