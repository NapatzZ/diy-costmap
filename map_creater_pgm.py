import numpy as np
import matplotlib.pyplot as plt 
import imageio  
from const import *
from costmap import Costmap

class CostmapBuilder:
    """
    CostmapBuilder class provides an interactive interface for building and modifying a Costmap grid.
    Users can add or remove obstacles by clicking or dragging on the grid, save the Costmap to a file,
    reset the grid, or exit the application.

    Attributes:
        costmap (Costmap): An instance of the Costmap class representing the environment grid.
        fig (Figure): The Matplotlib figure object.
        ax (Axes): The Matplotlib axes object.
        cmap (Colormap): The color map used for displaying the Costmap.
        im (AxesImage): The image object representing the Costmap on the axes.
        mouse_pressed (bool): Flag indicating whether the mouse button is currently pressed.
        current_drag_cells (set): A set of cells that have been modified during the current drag action.
    """

    def __init__(self, costmap: Costmap):
        """
        Initializes the CostmapBuilder with a specific Costmap. Sets up the visualization window,
        configures the grid display, and connects event handlers for user interactions.

        Args:
            costmap (Costmap): The Costmap instance to be built and modified interactively.
        """
        self.costmap = costmap
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.cmap = plt.cm.gray
        self.im = self.ax.imshow(
            self.costmap.grid,
            cmap=self.cmap,
            origin='lower',
            vmin=0,
            vmax=255
        )
        self.ax.set_xticks(np.arange(-0.5, self.costmap.width, 1), minor=True)
        self.ax.set_yticks(np.arange(-0.5, self.costmap.height, 1), minor=True)
        self.ax.grid(which='minor', color='lightgrey', linestyle='-', linewidth=0.5)
        self.mouse_pressed = False
        self.current_drag_cells = set()
        self.cid_click = self.fig.canvas.mpl_connect('button_press_event', self.onbutton_press)
        self.cid_release = self.fig.canvas.mpl_connect('button_release_event', self.onbutton_release)
        self.cid_motion = self.fig.canvas.mpl_connect('motion_notify_event', self.onmotion)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.onkey)
        self.update_display()

    def onbutton_press(self, event):
        """
        Event handler for mouse button press. Initiates obstacle toggling if the click is within the grid.

        Args:
            event (MouseEvent): The mouse button press event.
        """
        if event.inaxes != self.ax:
            return
        self.mouse_pressed = True
        self.current_drag_cells.clear()
        x, y = int(round(event.xdata)), int(round(event.ydata))
        if not self.costmap.is_within_bounds(x, y):
            return
        self.costmap.toggle_obstacle(x, y)
        self.current_drag_cells.add((x, y))
        self.update_display()

    def onbutton_release(self, event):
        """
        Event handler for mouse button release. Ends the obstacle toggling action.

        Args:
            event (MouseEvent): The mouse button release event.
        """
        self.mouse_pressed = False

    def onmotion(self, event):
        """
        Event handler for mouse motion. Continues obstacle toggling while the mouse button is pressed.

        Args:
            event (MouseEvent): The mouse motion event.
        """
        if not self.mouse_pressed:
            return
        if event.inaxes != self.ax:
            return
        x, y = int(round(event.xdata)), int(round(event.ydata))
        if not self.costmap.is_within_bounds(x, y):
            return
        if (x, y) not in self.current_drag_cells:
            self.costmap.toggle_obstacle(x, y)
            self.current_drag_cells.add((x, y))
            self.update_display()

    def onkey(self, event):
        """
        Event handler for key press events. Executes actions based on the pressed key:
        - '1': Save the current Costmap to a file.
        - 'r': Reset the Costmap grid to its initial state.
        - '2': Exit the application.

        Args:
            event (KeyEvent): The key press event.
        """
        if event.key == '1':
            self.save_map()
        elif event.key == 'r':
            self.costmap.reset()
            self.update_display()
            print("Reset the Costmap grid.")
        elif event.key == '2':
            plt.close(self.fig)

    def save_map(self):
        """
        Saves the current Costmap grid to a PGM file named 'costmap.pgm'.
        Provides feedback to the user upon successful save or if an error occurs.
        """
        print("Saving Costmap...")
        try:
            imageio.imwrite("costmap.pgm", self.costmap.grid)
            print("Costmap saved successfully as 'costmap.pgm'.")
        except Exception as e:
            print(f"Error saving Costmap: {e}")

    def update_display(self):
        """
        Updates the visualization to reflect the current state of the Costmap grid.
        Refreshes the image data and redraws the canvas.
        """
        self.im.set_data(self.costmap.grid)
        self.fig.canvas.draw_idle()

    def show(self):
        """
        Displays the interactive CostmapBuilder window and prints user instructions.
        """
        print("=== Obstacle Drawing Mode ===")
        print("Click or drag on the grid to add or remove obstacles.")
        print("Press '1' to save the Costmap.")
        print("Press 'r' to reset the Costmap.")
        print("Press '2' to exit.")
        plt.show()

def main():
    """
    The main function to run the CostmapBuilder. Initializes the Costmap and launches the interactive builder.
    """
    costmap = Costmap()
    visualizer = CostmapBuilder(costmap)
    visualizer.show()

if __name__ == "__main__":
    main()