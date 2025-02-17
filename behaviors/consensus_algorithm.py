import numpy as np

class ConsensusAlgorithm:
    """
    Implements a consensus algorithm for drone swarms.
    The algorithm ensures that drones move towards the average position of their neighbors,
    promoting cohesion within the swarm.
    """

    def __init__(self, epsilon):
        """
        Initializes the consensus algorithm.

        Parameters:
        - epsilon (float): Convergence rate factor that determines how strongly 
                           the drone moves towards the average neighbor position.
        """
        self.epsilon = epsilon

    def apply(self, drone, neighbor_positions, current_position):
        """
        Applies the consensus algorithm to adjust the drone's position based on 
        the average position of its neighbors.

        Parameters:
        - drone (Drone): The current drone object.
        - neighbor_positions (list of numpy arrays): Positions of neighboring drones.
        - current_position (numpy array): The current position of the drone.

        Returns:
        - new_position (numpy array): The updated position after applying the consensus algorithm.
        """
        # Compute the mean position of all neighboring drones
        mean_neighbor_position = np.mean(neighbor_positions, axis=0)

        # Update the position by moving towards the mean neighbor position
        new_position = current_position + self.epsilon * (mean_neighbor_position - current_position)

        return new_position
