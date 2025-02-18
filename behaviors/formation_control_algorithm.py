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
        self.target_point = np.array([0, 0, 0])  # Initial target point for the formation

    def set_target_point(self, target_point):
        """
        Sets the target point for the formation.

        Parameters:
        - target_point (numpy array): The new target point for the formation.
        """
        self.target_point = target_point

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

        # Adjust the target position based on the formation's target point
        target_position += self.target_point

        # Move gradually towards the target position
        direction = target_position - current_position
        step_size = 0.1  # Adjust step size for smoother movement
        new_position = current_position + step_size * direction

        return new_position

    def get_formation(self, drones):
        """
        Returns the relative positions of drones based on the current formation type.

        Parameters:
        - drones (list of Drone): List of drone objects in the swarm.

        Returns:
        - formation (numpy array): Relative positions of drones in the formation.
        """
        if self.formation_type == "line":
            return self._compute_line_formation(len(drones))
        elif self.formation_type == "circle":
            return self._compute_circle_formation(len(drones))
        elif self.formation_type == "square":
            return self._compute_square_formation(len(drones))
        elif self.formation_type == "random":
            return self._compute_random_formation(len(drones))
        return np.zeros((len(drones), 3))

    def _compute_line_formation(self, num_drones):
        """
        Computes the relative positions for a line formation.

        Parameters:
        - num_drones (int): Number of drones in the swarm.

        Returns:
        - formation (numpy array): Relative positions for the line formation.
        """
        line_length = 10  # Length of the line
        return np.array([[i, 0, 0] for i in np.linspace(0, line_length, num_drones)])

    def _compute_circle_formation(self, num_drones):
        """
        Computes the relative positions for a circular formation.

        Parameters:
        - num_drones (int): Number of drones in the swarm.

        Returns:
        - formation (numpy array): Relative positions for the circular formation.
        """
        radius = 10  # Radius of the circle
        angle_step = 2 * np.pi / num_drones
        return np.array([[radius * np.cos(i * angle_step), radius * np.sin(i * angle_step), 0] for i in range(num_drones)])

    def _compute_square_formation(self, num_drones):
        """
        Computes the relative positions for a square formation.

        Parameters:
        - num_drones (int): Number of drones in the swarm.

        Returns:
        - formation (numpy array): Relative positions for the square formation.
        """
        side_length = int(np.ceil(np.sqrt(num_drones)))  # Define the grid size
        spacing = 2  # Adjust spacing between drones
        center_offset = (side_length - 1) * spacing / 2
        return np.array([[(i % side_length) * spacing - center_offset, (i // side_length) * spacing - center_offset, 0] for i in range(num_drones)])

    def _compute_random_formation(self, num_drones):
        """
        Computes random relative positions for the drones.

        Parameters:
        - num_drones (int): Number of drones in the swarm.

        Returns:
        - formation (numpy array): Random relative positions.
        """
        return np.random.rand(num_drones, 3) * 10

    def _line_formation(self, drone, neighbor_positions):
        """
        Computes the target position for a line formation.

        Parameters:
        - drone (Drone): The current drone object.
        - neighbor_positions (list of numpy arrays): Positions of neighboring drones.

        Returns:
        - target_position (numpy array): The computed position for the line formation.
        """
        line_length = 10  # Length of the line
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
