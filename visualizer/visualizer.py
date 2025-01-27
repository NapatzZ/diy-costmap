import random
import pygame

from abc import ABC, abstractmethod
from const import Config


class Visualizer(ABC):
    """
    Abstract base class for all visualizers.
    """

    @abstractmethod
    def draw(self, screen):
        """
        Draw method to be implemented by subclasses.
        """
        pass
