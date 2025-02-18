import numpy as np

class Drone:
    """
    Represents a single drone in the swarm with basic movement and communication capabilities.
    """

    def __init__(self, position, index):
        """
        Initializes a drone with a given position and index.

        Parameters:
        - position (array-like): Initial position of the drone in the 3D space.
        - index (int): Unique identifier for the drone.
        """
        self.position = np.array(position)
        self.index = index
        self.target_position = np.array(position)  # Initialize with the current position

    def update_position(self, neighbor_positions, behavior_algorithms):
        """
        Updates the drone's position based on behavior algorithms and neighboring drones.

        Parameters:
        - neighbor_positions (list of arrays): Positions of nearby drones.
        - behavior_algorithms (list): List of behavior algorithms to apply.
        
        The new position is determined by averaging the results of all applied behavior algorithms.
        """
        # Compute the new position proposed by each behavior algorithm
        new_positions = [algorithm.apply(self, neighbor_positions, self.position.copy()) for algorithm in behavior_algorithms]

        # Calculate the average of all proposed new positions
        new_position = np.mean(new_positions, axis=0)
        self.position = new_position
        
        # Update target position based on the last applied algorithm
        if behavior_algorithms:
            self.target_position = behavior_algorithms[-1].apply(self, neighbor_positions, self.position.copy())


    def communicate(self):
        """
        Returns the position information that the drone shares with others.
        This simulates communication between drones in the swarm.
        
        Returns:
        - position (numpy array): The current position of the drone.
        """
        return self.position

    def get_position(self):
        """
        Retrieves the current position of the drone.

        Returns:
        - position (numpy array): The current position of the drone.
        """
        return self.position
