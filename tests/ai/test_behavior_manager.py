import numpy as np
import pytest

from core.drone import Drone
from ai.consensus import Consensus
from ai.collision_avoidance import CollisionAvoidance
from ai.formation_control import FormationControl
from ai.behavior_manager import BehaviorManager

class TestBehaviorManager:
    """Tests for behavior management."""

    def setup_method(self):
        """Initialize drones and BehaviorManager."""
        self.drones = [
            Drone(index=i, position=np.array([i * 5, 0, 0]))
            for i in range(3)
        ]
        self.behaviors = [
            Consensus(epsilon=0.1),
            CollisionAvoidance(collision_threshold=2.0),
            FormationControl(formation_type="line")
        ]
        self.manager = BehaviorManager(self.behaviors)

    def test_combined_behaviors(self):
        """Check that multiple behaviors are correctly applied together."""
        new_positions = self.manager.compute_positions(self.drones)

        for i, new_pos in enumerate(new_positions):
            assert np.linalg.norm(new_pos - self.drones[i].get_position()) > 0  # Must move
            assert np.linalg.norm(new_pos - self.drones[i].get_position()) < 5  # Must not move too far
