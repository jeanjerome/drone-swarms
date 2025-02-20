import asyncio
import logging
from typing import Dict, Callable, List, Union, Coroutine

class EventManager:
    """
    Manages event communication between components, supporting both synchronous and asynchronous calls.
    """

    def __init__(self, root) -> None:
        """Initialize the event manager."""
        self.listeners: Dict[str, List[Union[Callable, Coroutine]]] = {}
        self.root = root
        self.loop = asyncio.get_event_loop()
        self.logger = logging.getLogger(__name__)

    def subscribe(self, event_type: str, callback: Union[Callable, Coroutine]) -> None:
        """
        Subscribe a function (synchronous or asynchronous) to an event type.

        Args:
            event_type (str): Event name.
            callback (Union[Callable, Coroutine]): Function to call.
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
        self.logger.info(f"🔗 Subscribed `{callback.__name__}` to event '{event_type}'")

    def notify(self, event_type: str, data: Dict) -> None:
        """
        Notify all subscribers of an event (executed synchronously in the main Tkinter thread).

        Args:
            event_type (str): Event name.
            data (Dict): Data associated with the event.
        """
        self.logger.info(f"📢 Notifying {len(self.listeners.get(event_type, []))} listeners of event '{event_type}'")
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        self.logger.debug(f"🌀 Running async callback `{callback.__name__}`")
                        self.loop.create_task(callback(data))  # Asynchronous execution
                    else:
                        self.logger.debug(f"🔧 Running sync callback `{callback.__name__}`")
                        self.root.after(0, callback, data)  # Synchronous execution in Tkinter
                except Exception as e:
                    self.logger.error(f"Error executing callback `{callback.__name__}`: {e}")
