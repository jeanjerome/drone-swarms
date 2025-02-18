import numpy as np

class FlockingBehavior:
    """
    Implements flocking behavior for drone swarms based on Reynolds' rules.
    """

    def apply(self, drone, neighbors):
        """
        Applies flocking behavior to adjust the drone's velocity.

        Parameters:
        - drone (Drone): The current drone object.
        - neighbors (list of Drone): List of neighboring drones.

        Returns:
        - new_velocity (numpy array): The updated velocity after applying flocking behavior.
        """
        alignment = self._align(drone, neighbors)
        cohesion = self._cohere(drone, neighbors)
        separation = self._separate(drone, neighbors)

        # Update the drone's velocity based on the flocking rules
        new_velocity = drone.velocity + alignment + cohesion + separation

        # Limit the velocity to a maximum speed
        max_speed = 2.0
        speed = np.linalg.norm(new_velocity)
        if speed > max_speed:
            new_velocity = (new_velocity / speed) * max_speed

        return new_velocity

    def _align(self, drone, neighbors):
        """
        Computes the alignment vector for the drone.
        """
        perception_radius = 50
        avg_velocity = np.zeros(3)
        total = 0

        for neighbor in neighbors:
            if np.linalg.norm(neighbor.position - drone.position) < perception_radius:
                avg_velocity += neighbor.velocity
                total += 1

        if total > 0:
            avg_velocity /= total
            return (avg_velocity - drone.velocity) * 0.1

        return np.zeros(3)

    def _cohere(self, drone, neighbors):
        """
        Computes the cohesion vector for the drone.
        """
        perception_radius = 50
        center_of_mass = np.zeros(3)
        total = 0

        for neighbor in neighbors:
            if np.linalg.norm(neighbor.position - drone.position) < perception_radius:
                center_of_mass += neighbor.position
                total += 1

        if total > 0:
            center_of_mass /= total
            return (center_of_mass - drone.position) * 0.01

        return np.zeros(3)

    def _separate(self, drone, neighbors):
        """
        Computes the separation vector for the drone.
        """
        perception_radius = 25
        move_away = np.zeros(3)

        for neighbor in neighbors:
            distance = np.linalg.norm(neighbor.position - drone.position)
            if distance < perception_radius:
                move_away += (drone.position - neighbor.position) / distance

        return move_away * 0.1
