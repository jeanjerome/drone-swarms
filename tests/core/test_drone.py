import numpy as np
from core.drone import Drone
from core.motor import Motor
from core.battery import Battery
from core.communication import Communication

def test_drone_initialization():
    """Check the correct initialization of a drone."""
    drone = Drone(index=0, position=np.array([0, 0, 0]))
    assert isinstance(drone.motor, Motor)
    assert isinstance(drone.battery, Battery)
    assert isinstance(drone.communication, Communication)
    assert np.array_equal(drone.get_position(), np.array([0, 0, 0]))
    assert drone.get_battery_level() == 100

def test_drone_move():
    """Check that the drone moves correctly and consumes energy."""
    drone = Drone(index=0, position=np.array([0, 0, 0]))
    initial_battery = drone.get_battery_level()

    drone.move(np.array([5, 5, 5]))

    assert np.array_equal(drone.get_position(), np.array([5, 5, 5]))
    assert drone.get_battery_level() < initial_battery  # Should have consumed energy

def test_drone_communication():
    """Test communication between two drones."""
    drone1 = Drone(index=0, position=np.array([0, 0, 0]))
    drone2 = Drone(index=1, position=np.array([3, 0, 0]))  # Within range

    assert drone1.can_communicate_with(drone2) is True

    drone2.move(np.array([10, 0, 0]))  # Out of range
    assert drone1.can_communicate_with(drone2) is False
