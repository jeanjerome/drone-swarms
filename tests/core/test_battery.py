import pytest
from core.battery import Battery

def test_battery_initialization():
    """Check the correct initialization of a battery."""
    battery = Battery(capacity=100)
    assert battery.level == 100

def test_battery_update():
    """Check the correct discharge of the battery."""
    battery = Battery(capacity=100)

    battery.update(20)
    assert battery.level == 80

    battery.update(90)  # Should not go below 0
    assert battery.level == 0

def test_battery_is_depleted():
    """Check if the battery can be considered empty."""
    battery = Battery(capacity=50)

    assert battery.is_depleted() is False
    battery.update(50)
    assert battery.is_depleted() is True
