import asyncio
import numpy as np
from typing import List

from core.drone import Drone
from ai.behavior_manager import BehaviorManager
from simulation.event_manager import EventManager

class SwarmSimulation:
    """
    Manages the simulation of the drone swarm.
    """

    def __init__(self, drones: List[Drone], behavior_manager: BehaviorManager, event_manager: EventManager) -> None:
        """
        Initialize the simulation.

        Args:
            drones (List[Drone]): List of drones.
            behavior_manager (BehaviorManager): Behavior manager.
            event_manager (EventManager): Event manager.
        """
        self.drones: List[Drone] = drones
        self.behavior_manager: BehaviorManager = behavior_manager
        self.event_manager: EventManager = event_manager
        self.running: bool = False
        self.lock = asyncio.Lock()  # To avoid conflicts in updates

    async def start(self) -> None:
        """Start the simulation in an asynchronous coroutine."""
        if not self.running:
            self.running = True
            asyncio.create_task(self.run())

    def stop(self) -> None:
        """Stop the simulation properly."""
        self.running = False

    async def run(self):
        """Main loop to update drones."""
        while self.running:
            await self.update()
            # await asyncio.sleep(0.2)  # Control simulation speed

    async def update(self) -> None:
        """Update drone positions and notify events."""
        new_positions = self.behavior_manager.compute_positions(self.drones)
        for drone, new_position in zip(self.drones, new_positions):
            drone.move(self.interpolate(drone.get_position(), new_position, alpha=0.1))
            self.event_manager.notify("position_update", {"index": drone.index, "position": new_position})

    @staticmethod
    def interpolate(start: np.ndarray, end: np.ndarray, alpha: float) -> np.ndarray:
        """
        Gradually interpolate between the current position and the target position.

        Args:
            start (np.ndarray): Current position.
            end (np.ndarray): Target position.
            alpha (float): Interpolation factor (0 = stationary, 1 = instant).

        Returns:
            np.ndarray: New interpolated position.
        """
        return (1 - alpha) * start + alpha * end
