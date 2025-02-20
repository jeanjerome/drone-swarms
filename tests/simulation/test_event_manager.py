import pytest
from simulation.event_manager import EventManager

class TestEventManager:
    """Tests for event management."""

    def setup_method(self):
        """Initialize an EventManager for each test."""
        self.event_manager = EventManager()
        self.event_triggered = False
        self.received_data = None

    def sample_callback(self, data):
        """Test callback to verify event reception."""
        self.event_triggered = True
        self.received_data = data

    def test_subscribe_and_notify(self):
        """Check that an event is received after subscription."""
        self.event_manager.subscribe("test_event", self.sample_callback)
        self.event_manager.notify("test_event", {"message": "Hello"})

        assert self.event_triggered is True
        assert self.received_data == {"message": "Hello"}

    def test_no_notification_if_not_subscribed(self):
        """Check that an unsubscribed event does not trigger anything."""
        self.event_manager.notify("test_event", {"message": "Hello"})
        assert self.event_triggered is False  # Callback should not be called
