import numpy as np
import pytest

from core.drone import Drone
from ai.collision_avoidance import CollisionAvoidance

class TestCollisionAvoidance:
    """Tests for the collision avoidance algorithm."""

    def setup_method(self):
        """Initialize objects for testing."""
        self.drone1 = Drone(index=0, position=np.array([0, 0, 0]))
        self.drone2 = Drone(index=1, position=np.array([0.5, 0, 0]))  # Very close
        self.avoidance = CollisionAvoidance(collision_threshold=1.0)

    def test_avoidance_moves_drone(self):
        """Check that the drone moves in case of imminent collision."""
        new_position = self.avoidance.apply(self.drone1, [self.drone2])
        assert np.linalg.norm(new_position - self.drone1.get_position()) > 0  # Must move

    def test_no_movement_if_far(self):
        """Check that the drone does not move if it is out of the collision zone."""
        self.drone2.move(np.array([5, 0, 0]))  # Out of range
        new_position = self.avoidance.apply(self.drone1, [self.drone2])
        assert np.array_equal(new_position, self.drone1.get_position())  # Does not move
