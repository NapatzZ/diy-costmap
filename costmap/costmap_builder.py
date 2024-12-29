"""
Interactive CostmapBuilder for toggling obstacles.
"""

import matplotlib.pyplot as plt
from visualizer.visualizer import Visualizer


class CostmapBuilder(Visualizer):
    """
    Allows the user to click or drag on the grid to toggle obstacles
    between UNKNOWN and OBSTACLE.
    """

    def __init__(self, costmap):
        """
        Initialize the builder with a given costmap.

        Args:
            costmap (Costmap): The costmap to modify.
        """
        super().__init__(costmap, fig_size=(10, 10))
        self.mouse_pressed = False
        self.current_drag_cells = set()

        self.cid_click = self.fig.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.cid_release = self.fig.canvas.mpl_connect('button_release_event', self.on_button_release)
        self.cid_motion = self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def on_button_press(self, event):
        """
        Handle mouse press. Toggle the clicked cell if within axes.
        """
        if event.inaxes != self.ax:
            return
        self.mouse_pressed = True
        self.current_drag_cells.clear()
        x, y = int(round(event.xdata)), int(round(event.ydata))
        if self.costmap.is_within_bounds(x, y):
            self.costmap.toggle_obstacle(x, y)
            self.current_drag_cells.add((x, y))
            self.update_display()

    def on_button_release(self, event):
        """
        Handle mouse release.
        """
        self.mouse_pressed = False

    def on_motion(self, event):
        """
        Handle mouse drag. Toggle obstacles along the path of the drag.
        """
        if not self.mouse_pressed:
            return
        if event.inaxes != self.ax:
            return
        x, y = int(round(event.xdata)), int(round(event.ydata))
        if (x, y) not in self.current_drag_cells and self.costmap.is_within_bounds(x, y):
            self.costmap.toggle_obstacle(x, y)
            self.current_drag_cells.add((x, y))
            self.update_display()

    def on_key(self, event):
        """
        Handle keypress:
          '1' -> save map
          'r' -> reset costmap to UNKNOWN
          '2' -> exit
        """
        if event.key == '1':
            self.save_map()
        elif event.key == 'r':
            self.costmap.reset()
            self.update_display()
            print("Costmap has been reset to UNKNOWN.")
        elif event.key == '2':
            plt.close(self.fig)

    def save_map(self):
        """
        Save the costmap as costmap.pgm using imageio.
        """
        import imageio
        print("Saving costmap as 'costmap.pgm'...")
        try:
            imageio.imwrite("costmap.pgm", self.costmap.grid)
            print("Saved successfully.")
        except Exception as e:
            print(f"Error saving map: {e}")

    def show(self):
        """
        Display the builder instructions and show the interactive plot.
        """
        print("=== Costmap Builder ===")
        print("Click or drag on the grid to toggle obstacles (UNKNOWN <-> OBSTACLE).")
        print("Press '1' to save as costmap.pgm")
        print("Press 'r' to reset to UNKNOWN")
        print("Press '2' to close")
        plt.show()