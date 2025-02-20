import numpy as np

class Motor:
    """
    Manages the power and consumption of the drone's motor.
    """

    def __init__(self, max_power: float) -> None:
        """
        Initialize the drone's motor.

        Args:
            max_power (float): Maximum power of the motor.
        """
        self.max_power: float = max_power
        self.power_consumption: float = 0.0

    def update(self, velocity: np.ndarray) -> None:
        """
        Update the power consumption based on the velocity.

        Args:
            velocity (np.ndarray): Velocity vector of the drone.
        """
        speed = np.linalg.norm(velocity)
        self.power_consumption = (speed / 10.0) * self.max_power  # Arbitrary scale
