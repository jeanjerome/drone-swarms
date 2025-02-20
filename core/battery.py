class Battery:
    """
    Manages the available energy of the drone.
    """

    def __init__(self, capacity: float) -> None:
        """
        Initialize the drone's battery.

        Args:
            capacity (float): Maximum capacity of the battery.
        """
        self.capacity: float = capacity
        self.level: float = capacity

    def update(self, power_consumption: float) -> None:
        """
        Update the battery level based on power consumption.

        Args:
            power_consumption (float): Amount of energy consumed.
        """
        self.level = max(0.0, self.level - power_consumption)

    def is_depleted(self) -> bool:
        """
        Check if the battery is empty.

        Returns:
            bool: True if the battery is empty, False otherwise.
        """
        return self.level <= 0
