from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import numpy as np

from core.drone import Drone

class BehaviorAlgorithm(ABC):
    """
    Abstract class defining a behavior for drones.
    """

    @abstractmethod
    def apply(self, drone: Drone, neighbors: List[Drone]) -> np.ndarray:
        """
        Apply the behavior and return the new target position.

        Args:
            drone (Drone): Current drone.
            neighbors (List[Drone]): List of neighboring drones.

        Returns:
            np.ndarray: Target position of the drone.
        """
        pass
