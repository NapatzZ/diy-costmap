"""
Main entry point. Allows user to choose either Costmap Builder or Path Visualizer.
"""

import sys
from costmap.costmap import Costmap
from costmap.costmap_builder import CostmapBuilder
from visualizer.path_visualizer import PathVisualizer


def main() -> None:
    """
    The main function. Allows selection:
    1) Costmap Builder
    2) Path Visualizer
    """
    print("=== Costmap Path Planning and Visualization Tool ===")
    print("Select Mode:")
    print("1. Costmap Builder")
    print("2. Path Visualizer")

    mode = input("Enter '1' or '2': ").strip()

    # Create a default 100x100 costmap
    costmap = Costmap(width=100, height=100)

    if mode == '1':
        # Builder mode
        builder = CostmapBuilder(costmap)
        builder.show()

    elif mode == '2':
        # Path Visualizer mode
        map_file = input("Enter the name of the map file to load (e.g. 'costmap.pgm'): ").strip()
        costmap.load_map(map_file)
        visualizer = PathVisualizer(costmap, map_file)
        visualizer.show()

    else:
        print("Invalid selection. Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()