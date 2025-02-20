import numpy as np
from typing import List

from ai.behavior_algorithm import BehaviorAlgorithm
from core.drone import Drone

class FormationControl(BehaviorAlgorithm):
    """
    Applies a specific formation to drones based on a target point.
    """

    def __init__(self, formation_type: str, target_point: np.ndarray = np.array([0, 0, 0])) -> None:
        """
        Initialize the formation control.

        Args:
            formation_type (str): Type of formation ("line", "circle", "square", "random").
            target_point (np.ndarray): Target point towards which the drones should move.
        """
        self.formation_type: str = formation_type
        self.target_point: np.ndarray = target_point  # New target point

    def apply(self, drone: Drone, neighbors: List[Drone]) -> np.ndarray:
        """
        Calculate the target position of the drone based on the formation and the target point.

        Args:
            drone (Drone): Current drone.
            neighbors (List[Drone]): List of neighboring drones.

        Returns:
            np.ndarray: Target position of the drone.
        """
        all_drones = [drone] + neighbors
        num_drones = len(all_drones)

        if self.formation_type == "line":
            line_length = num_drones / 3
            target_positions = np.linspace(0, line_length, len(all_drones))
            local_position = np.array([target_positions[drone.index], 0.0, 0.0])

        elif self.formation_type == "circle":
            radius = 10.0
            index = sorted(all_drones, key=lambda d: d.index).index(drone)
            angle = 2 * np.pi * index / num_drones
            local_position = np.array([radius * np.cos(angle), radius * np.sin(angle), 0])

        elif self.formation_type == "square":
            spacing = 2.0
            grid_size = int(np.ceil(np.sqrt(num_drones)))
            index = sorted(all_drones, key=lambda d: d.index).index(drone)

            row = index // grid_size
            col = index % grid_size

            center_offset = (grid_size - 1) * spacing / 2
            local_position = np.array([
                col * spacing - center_offset,
                row * spacing - center_offset,
                5.0
            ])

        elif self.formation_type == "random":
            local_position = np.random.rand(3) * 20 - 10

        else:
            return drone.get_position()  # Unknown formation, do not move

        # Apply the movement towards the target point
        target_position = self.target_point + local_position

        return target_position
