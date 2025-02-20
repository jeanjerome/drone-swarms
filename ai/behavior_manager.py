from typing import List
import numpy as np

from core.drone import Drone
from ai.behavior_algorithm import BehaviorAlgorithm

class BehaviorManager:
    """
    Manages the application of various behaviors on a swarm of drones.
    """

    def __init__(self, behaviors: List[BehaviorAlgorithm]) -> None:
        """
        Initialize the behavior manager with a list of behavior algorithms.

        Args:
            behaviors (List[BehaviorAlgorithm]): List of behavior algorithms.
        """
        self.behaviors: List[BehaviorAlgorithm] = behaviors

    def compute_positions(self, drones: List[Drone]) -> List[np.ndarray]:
        """
        Calculate the new positions of the drones by combining the behaviors.

        Args:
            drones (List[Drone]): List of drones.

        Returns:
            List[np.ndarray]: List of new positions.
        """
        new_positions = []

        for drone in drones:
            neighbors = [other for other in drones if other != drone]
            behavior_positions = [algo.apply(drone, neighbors) for algo in self.behaviors]
            new_positions.append(np.mean(behavior_positions, axis=0))  # Average of behaviors

        return new_positions
