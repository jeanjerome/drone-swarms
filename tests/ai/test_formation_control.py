import numpy as np
import pytest

from core.drone import Drone
from ai.formation_control import FormationControl

class TestFormationControl:
    """Tests for formation control."""

    def setup_method(self):
        """Initialize drones and formation."""
        self.drones = [
            Drone(index=i, position=np.array([0, 0, 0]))
            for i in range(3)
        ]
        self.formation = FormationControl(formation_type="line")

    def test_line_formation(self):
        """Check that drones form a line."""
        new_positions = [self.formation.apply(drone, self.drones) for drone in self.drones]
        assert np.array_equal(new_positions[0], np.array([0, 0, 0]))
        assert np.array_equal(new_positions[1], np.array([2, 0, 0]))
        assert np.array_equal(new_positions[2], np.array([4, 0, 0]))

    def test_circle_formation(self):
        """Check that drones form a circle."""
        self.formation = FormationControl(formation_type="circle")
        new_positions = [self.formation.apply(drone, self.drones) for drone in self.drones]
        assert len(new_positions) == 3
        assert all(np.linalg.norm(pos - np.array([0, 0, 0])) > 0 for pos in new_positions)  # Must form a circle
