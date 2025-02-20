import numpy as np
from typing import List

from ai.behavior_algorithm import BehaviorAlgorithm
from core.drone import Drone

class Consensus(BehaviorAlgorithm):
    """
    Implements a consensus algorithm for aligning drones.
    """

    def __init__(self, epsilon: float) -> None:
        """
        Initialize the consensus algorithm.

        Args:
            epsilon (float): Attraction factor towards the center.
        """
        self.epsilon: float = epsilon

    def apply(self, drone: Drone, neighbors: List[Drone]) -> np.ndarray:
        """
        Converge the drone towards the average position of its neighbors.

        Args:
            drone (Drone): Current drone.
            neighbors (List[Drone]): List of neighboring drones.

        Returns:
            np.ndarray: Target position after applying consensus.
        """
        if not neighbors:
            return drone.get_position()  # No neighbors, stay in place

        neighbor_positions = np.array([n.get_position() for n in neighbors])
        mean_position = np.mean(neighbor_positions, axis=0)

        return drone.get_position() + self.epsilon * (mean_position - drone.get_position())
