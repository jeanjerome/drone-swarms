import numpy as np
import pytest
from core.motor import Motor

def test_motor_initialization():
    """Check the correct initialization of a motor."""
    motor = Motor(max_power=10)
    assert motor.max_power == 10
    assert motor.power_consumption == 0

def test_motor_update():
    """Check that power consumption varies with speed."""
    motor = Motor(max_power=10)

    motor.update(np.array([0, 0, 0]))  # Stationary
    assert motor.power_consumption == 0

    motor.update(np.array([5, 0, 0]))  # Moving
    assert motor.power_consumption > 0

    motor.update(np.array([10, 0, 0]))  # Higher speed
    assert motor.power_consumption > 0
