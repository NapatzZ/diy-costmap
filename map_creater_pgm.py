import numpy as np
import matplotlib.pyplot as plt # type: ignore
import imageio # type: ignore
from const import *

class Costmap:
    def __init__(self,width : int = MAX_WIDHT_PIXEL,height :int  = MAX_HEIGHT_PIXEL):
        self.width = width
        self.height = height
        self.grid = np.full((self.width,self.height), NOT_YET_VISITED, dtype=np.uint8)

