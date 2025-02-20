import numpy as np
from typing import List

from ai.behavior_algorithm import BehaviorAlgorithm
from core.drone import Drone

class CollisionAvoidance(BehaviorAlgorithm):
    """
    Implements a collision avoidance algorithm based on repulsive force.
    """

    def __init__(self, collision_threshold: float) -> None:
        """
        Initialize the collision avoidance algorithm.

        Args:
            collision_threshold (float): Distance threshold for collision avoidance.
        """
        self.collision_threshold: float = collision_threshold

    def apply(self, drone: Drone, neighbors: List[Drone]) -> np.ndarray:
        """
        Move the drone away from others if they are too close.

        Args:
            drone (Drone): Current drone.
            neighbors (List[Drone]): List of neighboring drones.

        Returns:
            np.ndarray: Target position after avoidance.
        """
        avoidance_vector = np.zeros(3)

        for neighbor in neighbors:
            distance = np.linalg.norm(drone.get_position() - neighbor.get_position())
            if 0 < distance < self.collision_threshold:
                direction = (drone.get_position() - neighbor.get_position()) / distance
                avoidance_vector += direction * (self.collision_threshold - distance)

        return drone.get_position() + avoidance_vector
