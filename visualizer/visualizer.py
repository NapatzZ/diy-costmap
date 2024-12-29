"""
A base Visualizer class with a Matplotlib figure for showing a costmap.
"""

import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    """
    Base class for costmap visualization. Creates a figure and axis for display.
    """

    def __init__(self, costmap, fig_size=(8, 8)):
        """
        Initialize the Visualizer.

        Args:
            costmap: The costmap to display.
            fig_size (tuple, optional): Size of the figure.
        """
        self.costmap = costmap
        self.fig, self.ax = plt.subplots(figsize=fig_size)
        self.im = self.ax.imshow(
            self.costmap.grid,
            cmap=plt.cm.gray,
            origin='lower',
            vmin=0,
            vmax=255
        )
        self.ax.set_aspect('equal', 'box')

        # Minor ticks for visual grid
        self.ax.set_xticks(np.arange(-0.5, costmap.width, 1), minor=True)
        self.ax.set_yticks(np.arange(-0.5, costmap.height, 1), minor=True)
        self.ax.grid(which='minor', color='lightgray', linestyle='-', linewidth=0.5)

    def update_display(self):
        """
        Update the displayed costmap.
        """
        self.im.set_data(self.costmap.grid)
        self.fig.canvas.draw_idle()