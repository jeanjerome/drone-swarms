import pytest
from core.communication import Communication

def test_communication_initialization():
    """Check the correct initialization of a communication module."""
    comm = Communication(range=10)
    assert comm.range == 10

def test_communication_range():
    """Check that communication is blocked out of range."""
    comm = Communication(range=10)

    assert comm.can_transmit(5) is True  # Within range
    assert comm.can_transmit(15) is False  # Out of range
