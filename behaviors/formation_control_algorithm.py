import numpy as np

class FormationControlAlgorithm:
    """
    Implements different formation control strategies for drone swarms.
    The algorithm adjusts each drone's position to maintain a specific formation.
    """

    def __init__(self, formation_type):
        """
        Initializes the formation control algorithm.

        Parameters:
        - formation_type (str): The type of formation ('line', 'circle', 'square', 'random').
        """
        self.formation_type = formation_type

    def apply(self, drone, neighbor_positions, current_position):
        """
        Applies the selected formation control strategy to adjust the drone's position.

        Parameters:
        - drone (Drone): The current drone object.
        - neighbor_positions (list of numpy arrays): Positions of neighboring drones.
        - current_position (numpy array): The current position of the drone.

        Returns:
        - new_position (numpy array): The updated position after applying the formation control algorithm.
        """
        if self.formation_type == "line":
            target_position = self._line_formation(drone, neighbor_positions)
        elif self.formation_type == "circle":
            target_position = self._circle_formation(drone, neighbor_positions)
        elif self.formation_type == "square":
            target_position = self._square_formation(drone, neighbor_positions)
        elif self.formation_type == "random":
            target_position = self._random_formation()
        else:
            # If the formation type is unknown, keep the current position
            return current_position

        # Move gradually towards the target position
        direction = target_position - current_position
        step_size = 0.1  # Adjust step size for smoother movement
        new_position = current_position + step_size * direction

        return new_position

    def _line_formation(self, drone, neighbor_positions):
        """
        Computes the target position for a line formation.

        Parameters:
        - drone (Drone): The current drone object.
        - neighbor_positions (list of numpy arrays): Positions of neighboring drones.

        Returns:
        - target_position (numpy array): The computed position for the line formation.
        """
        line_length = 10  # Increased line length
        # Dynamically determine the target positions along a straight line
        target_positions = np.linspace(0, line_length, len(neighbor_positions) + 1)
        
        # Set the target position based on the drone's index, centering the line at (5,5)
        target_position = np.array([target_positions[drone.index], 5.0, 5.0])

        return target_position

    def _circle_formation(self, drone, neighbor_positions):
        """
        Computes the target position for a circular formation.

        Parameters:
        - drone (Drone): The current drone object.
        - neighbor_positions (list of numpy arrays): Positions of neighboring drones.

        Returns:
        - target_position (numpy array): The computed position for the circular formation.
        """
        # Compute the angle for each drone in the circle
        angle = 2 * np.pi * drone.index / len(neighbor_positions)
        radius = 10  # Radius of the circle

        # Compute the target position for circular formation, centering at (5,5)
        target_position = np.array([
            radius * np.cos(angle) + 5.0, 
            radius * np.sin(angle) + 5.0, 
            5.0
        ])

        return target_position

    def _square_formation(self, drone, neighbor_positions):
        """
        Computes the target position for a square formation.
        
        Parameters:
        - drone (Drone): The current drone object.
        - neighbor_positions (list of numpy arrays): Positions of neighboring drones.
        
        Returns:
        - target_position (numpy array): The computed position for the square formation.
        """
        num_drones = len(neighbor_positions) + 1
        side_length = int(np.ceil(np.sqrt(num_drones)))  # Define the grid size
        
        row = drone.index // side_length
        col = drone.index % side_length
        
        spacing = 2  # Adjust spacing between drones
        center_offset = (side_length - 1) * spacing / 2
        
        target_position = np.array([
            col * spacing + 5.0 - center_offset, 
            row * spacing + 5.0 - center_offset,
            5.0
        ])
        
        return target_position
    
    def _random_formation(self):
        """
        Computes a random target 3D position for the drone.
        
        Returns:
        - target_position (numpy array): A random position within a defined space.
        """
        target_position = np.random.rand(3) * 10
        
        return target_position
