class Communication:
    """
    Manages communication between drones.
    """

    def __init__(self, range: float) -> None:
        """
        Initialize the communication range.

        Args:
            range (float): Maximum communication distance between drones.
        """
        self.range: float = range

    def can_transmit(self, distance: float) -> bool:
        """
        Check if a message can be transmitted at a given distance.

        Args:
            distance (float): Distance between two drones.

        Returns:
            bool: True if transmission is possible, False otherwise.
        """
        return distance <= self.range
