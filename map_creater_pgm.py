import numpy as np
import matplotlib.pyplot as plt 
import imageio  
from const import *

class Costmap:
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.grid = np.full((height, width), NOT_YET_VISITED, dtype=np.uint8)
    
    def add_obstacle(self, x, y):
        if self.is_within_bounds(x, y):
            self.grid[y][x] = OBSTACLE
    
    def remove_obstacle(self, x, y):
        if self.is_within_bounds(x, y) and self.grid[y][x] == OBSTACLE:
            self.grid[y][x] = NOT_YET_VISITED
    
    def toggle_obstacle(self, x, y):
        if self.is_within_bounds(x, y):
            if self.grid[y][x] == OBSTACLE:
                self.grid[y][x] = NOT_YET_VISITED
            else:
                self.grid[y][x] = OBSTACLE
    
    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def reset(self):
        self.grid = np.full((self.height, self.width), NOT_YET_VISITED, dtype=np.uint8)

class CostmapBuilder: 
    def __init__(self, costmap):
        self.costmap = costmap
        self.fig, self.ax = plt.subplots(figsize=(10,10))
        self.cmap = plt.cm.gray
        self.im = self.ax.imshow(self.costmap.grid, cmap=self.cmap, origin='lower', vmin=0, vmax=255)
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
        self.mouse_pressed = False
    
    def onmotion(self, event):
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
        if event.key == '1':
            self.save_map()
        elif event.key == 'r':
            self.costmap.reset()
            self.update_display()
            print("reset")
        elif event.key == '2':
            plt.close(self.fig)
    
    def save_map(self):
        print("save!!")
        imageio.imwrite("costmap.pgm", self.costmap.grid)
    
    def update_display(self):
        self.im.set_data(self.costmap.grid)
        self.fig.canvas.draw_idle()
    
    def show(self):
        print("=== Obstacle Drawing Mode ===")
        print("Click or drag on the grid to add or remove obstacles.")
        print("press '1' save")
        print("press 'r' reset")
        print("press '2' exit")
        plt.show()

def main():
    costmap = Costmap()
    visualizer = CostmapBuilder(costmap)
    visualizer.show()

if __name__ == "__main__":
    main()