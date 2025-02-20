import numpy as np
import pytest

from core.drone import Drone
from ai.consensus import Consensus

class TestConsensus:
    """Tests for the consensus algorithm."""

    def setup_method(self):
        """Initialize drones and the consensus algorithm."""
        self.drone1 = Drone(index=0, position=np.array([0, 0, 0]))
        self.drone2 = Drone(index=1, position=np.array([10, 0, 0]))
        self.drone3 = Drone(index=2, position=np.array([20, 0, 0]))
        self.consensus = Consensus(epsilon=0.1)

    def test_consensus_moves_towards_center(self):
        """Check that the drone moves towards the average position of its neighbors."""
        neighbor_positions = np.array([self.drone2.get_position(), self.drone3.get_position()])
        expected_mean = np.mean(neighbor_positions, axis=0)  # Average of neighbors
        new_position = self.consensus.apply(self.drone1, [self.drone2, self.drone3])
        assert np.allclose(new_position, self.drone1.get_position() + 0.1 * (expected_mean - self.drone1.get_position()))

    def test_no_movement_if_alone(self):
        """Check that the drone does not move if it is alone."""
        new_position = self.consensus.apply(self.drone1, [])
        assert np.array_equal(new_position, self.drone1.get_position())  # Does not move
