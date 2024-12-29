# Costmap Path Planning and Visualization Tool

## Introduction

  This project is an interactive Costmap Path Planning and Visualization Tool designed to enable users to build and edit 2D occupancy grids, define start and goal points, and simulate path planning using A*, Dijkstra, and RRT.

---

## Features

- **Create 2D Occupancy Grids**:
  - Interactively toggle cells to mark obstacles, free space, and unknown areas.
  - Save maps in `.pgm` format for later use.

- **Simulate Path Planning**:
  - Visualize computed paths for start and goal points using A*, Dijkstra, or RRT algorithms.
  - Color-coded grid states:
    - **White**: Free space.
    - **Black**: Obstacles.
    - **Gray**: Unknown areas.
  - Start and goal points are displayed as a **blue circle** and **red "X"**, respectively.

- **Reset and Reload**:
  - Restore the grid to its initial state.
  - Maintain start and goal points after a reset.

---

## Installation

### Dependencies

Install the required Python libraries:
```bash
pip install numpy matplotlib imageio
```
### Clone the Repository
How to clone and run 
```bash
git clone https://github.com/NapatzZ/diy-costmap.git

cd diy-costmap

python main.py
```

### Demostration
Here a demostration video
https://youtu.be/zN2icwEPDjE
