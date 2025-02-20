import pytest
import numpy as np
import matplotlib.pyplot as plt
from core.drone import Drone
from simulation.event_manager import EventManager
from visualization.swarm_visualizer import SwarmVisualizer

class TestSwarmVisualizer:
    """Tests for 3D visualization of the drone swarm."""

    def setup_method(self):
        """Initialize visualization with drones and an event manager."""
        self.drones = [
            Drone(index=i, position=np.array([i * 5, 0, 0])) for i in range(3)
        ]
        self.event_manager = EventManager()
        self.visualizer = SwarmVisualizer(self.drones, self.event_manager)

    def test_initialization(self):
        """Check that the display is properly initialized."""
        assert self.visualizer.scat is not None
        assert isinstance(self.visualizer.fig, plt.Figure)

    def test_update_plot(self):
        """Check that the drone positions are correctly updated in the display."""
        old_positions = np.array(self.visualizer.scat._offsets3d)

        # Simulate drone movement
        for drone in self.drones:
            drone.move(drone.get_position() + np.array([1, 1, 0]))

        self.visualizer.update_plot()
        new_positions = np.array(self.visualizer.scat._offsets3d)

        assert not np.array_equal(old_positions, new_positions)  # Positions should change

    def test_on_position_update(self):
        """Check that the `position_update` event correctly updates the display."""
        old_positions = np.array(self.visualizer.scat._offsets3d)

        self.event_manager.notify("position_update", {"index": 0, "position": np.array([10, 10, 10])})

        new_positions = np.array(self.visualizer.scat._offsets3d)
        assert not np.array_equal(old_positions, new_positions)  # Expected update
