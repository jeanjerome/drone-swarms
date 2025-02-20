import pytest
import numpy as np
from core.drone import Drone
from ai.behavior_manager import BehaviorManager
from ai.consensus import Consensus
from simulation.swarm_simulation import SwarmSimulation
from simulation.event_manager import EventManager

class TestSwarmSimulation:
    """Tests for swarm simulation management."""

    def setup_method(self):
        """Initialize the simulation with a set of drones."""
        self.drones = [
            Drone(index=i, position=np.array([i * 5, 0, 0])) for i in range(3)
        ]
        self.behavior_manager = BehaviorManager([Consensus(epsilon=0.1)])
        self.event_manager = EventManager()
        self.simulation = SwarmSimulation(self.drones, self.behavior_manager, self.event_manager)

    def test_simulation_start_stop(self):
        """Check that the simulation starts and stops correctly."""
        assert self.simulation.running is False

        self.simulation.start()
        assert self.simulation.running is True

        self.simulation.stop()
        assert self.simulation.running is False

    def test_drone_positions_are_updated(self):
        """Check that the drone positions change after an update."""
        initial_positions = np.array([drone.get_position() for drone in self.drones])

        self.simulation.update()  # Simulate one iteration

        new_positions = np.array([drone.get_position() for drone in self.drones])
        assert not np.array_equal(initial_positions, new_positions)  # Positions should have changed

    def test_event_manager_receives_updates(self):
        """Check that position update events are sent correctly."""
        event_received = []

        def callback(data):
            event_received.append(data)

        self.event_manager.subscribe("position_update", callback)
        self.simulation.update()

        assert len(event_received) == len(self.drones)  # Each drone sends an event
