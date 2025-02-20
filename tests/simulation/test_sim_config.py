import pytest
from config.sim_config import SimConfig

class TestSimConfig:
    """Tests for simulation configuration."""

    def test_default_parameters(self):
        """Check that the default parameters are correctly defined."""
        assert SimConfig.NUM_DRONES == 10
        assert SimConfig.COLLISION_THRESHOLD == 1.0
        assert SimConfig.CONSENSUS_EPSILON == 0.1
        assert SimConfig.FORMATION_TYPE == "line"
        assert SimConfig.SIMULATION_SPEED == 0.05
