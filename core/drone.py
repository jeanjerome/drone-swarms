from __future__ import annotations
from typing import List
import numpy as np

from core.motor import Motor
from core.battery import Battery
from core.communication import Communication

class Drone:
    """
    Represents an autonomous drone in a swarm.
    Each drone can move, communicate, and manage its energy.
    """

    def __init__(self, index: int, position: np.ndarray) -> None:
        """
        Initialize a drone with a position and internal components.

        Args:
            index (int): Unique identifier of the drone.
            position (np.ndarray): Initial position of the drone in (x, y, z).
        """
        self.index: int = index
        self.position: np.ndarray = np.array(position, dtype=np.float64)
        self.velocity: np.ndarray = np.zeros(3, dtype=np.float64)
        self.target_position: np.ndarray = self.position.copy()

        self.motor: Motor = Motor(max_power=10)
        self.battery: Battery = Battery(capacity=100)
        self.communication: Communication = Communication(range=5.0)

    def move(self, new_position: np.ndarray) -> None:
        """
        Move the drone to a new position, updating its velocity and battery.

        Args:
            new_position (np.ndarray): New target position.
        """
        self.velocity = new_position - self.position
        self.position = new_position
        self.motor.update(self.velocity)
        self.battery.update(self.motor.power_consumption)

    def can_communicate_with(self, other: Drone) -> bool:
        """
        Check if this drone can communicate with another drone.

        Args:
            other (Drone): Another drone.

        Returns:
            bool: True if communication is possible, False otherwise.
        """
        distance = np.linalg.norm(self.position - other.position)
        return distance <= self.communication.range

    def update_velocity(self, new_velocity: np.ndarray) -> None:
        """Update the drone's velocity."""
        self.velocity = new_velocity

    def get_position(self) -> np.ndarray:
        """Get the current position of the drone."""
        return self.position

    def get_velocity(self) -> np.ndarray:
        """Get the current velocity of the drone."""
        return self.velocity

    def get_battery_level(self) -> float:
        """Get the current battery level of the drone."""
        return self.battery.level
