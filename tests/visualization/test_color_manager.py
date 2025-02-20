import pytest
import numpy as np
from visualization.color_manager import ColorManager
from core.drone import Drone

class TestColorManager:
    """Tests for ColorManager."""

    def setup_method(self):
        """Initialize ColorManager and test drones."""
        self.color_manager = ColorManager()
        self.drones = [
            Drone(index=i, position=np.array([i * 2, 0, 0])) for i in range(5)
        ]

    def test_update_colors(self):
        """Check that ColorManager returns a list of normalized colors."""
        colors = self.color_manager.update_colors(self.drones)

        assert len(colors) == len(self.drones)  # Ensure each drone has a color
        assert all(isinstance(color, np.ndarray) for color in colors)  # Verify the type of colors
