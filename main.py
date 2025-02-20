import asyncio
import logging
import sys
import threading
import numpy as np
import tkinter as tk

from config.logging_config import configure_logging
from core.drone import Drone
from ai.behavior_manager import BehaviorManager
from ai.collision_avoidance import CollisionAvoidance
from ai.consensus import Consensus
from ai.formation_control import FormationControl
from simulation.event_manager import EventManager
from simulation.swarm_simulation import SwarmSimulation
from visualization.swarm_visualizer import SwarmVisualizer
from visualization.ui_controller import UIController

# Configure logging
configure_logging(logging.DEBUG)

class DroneSwarmApp(tk.Frame):
    """
    Main class for the drone simulation application.
    """

    def __init__(self, loop: asyncio.AbstractEventLoop, parent: tk.Tk, num_drones: int = 100, formation: str = "line") -> None:
        """
        Initialize all components necessary for the simulation.

        Args:
            loop (asyncio.AbstractEventLoop): Main event loop.
            num_drones (int): Number of drones in the simulation.
            formation (str): Initial formation of the drones ("circle", "line", "square", "random").
        """
        super().__init__(parent)

        self.loop = loop
        self.root = parent
        self.logger = logging.getLogger(__name__)
        self.num_drones = num_drones
        self.formation = formation
        self.running = True

        self.logger.info(f"Initializing DroneSwarmApp with {num_drones} drones in '{formation}' formation.")

        # Initialize EventManager
        self.event_manager = EventManager(self.root)

        # Create drones and emit initialization events
        self.drones = [Drone(index=i, position=np.random.rand(3) * 10) for i in range(num_drones)]
        self.logger.info(f"All {num_drones} drones have been initialized.")

        # Instantiate behavior managers
        self.behaviors = [
            CollisionAvoidance(collision_threshold=2.0),
            Consensus(epsilon=0.1),
            FormationControl(formation_type=formation)
        ]
        self.behavior_manager = BehaviorManager(behaviors=self.behaviors)

        # Initialize simulation with EventManager
        self.simulation = SwarmSimulation(drones=self.drones, behavior_manager=self.behavior_manager, event_manager=self.event_manager)

        # Initialize visualizer
        self.visualizer = SwarmVisualizer(drones=self.drones, event_manager=self.event_manager, formation_control=self.behaviors[-1])

        # Initialize user interface
        self.ui_controller = UIController(root=self.root, simulation=self.simulation, visualizer=self.visualizer, loop=self.loop)

        self.logger.info("DroneSwarmApp initialization complete.")

    def run(self):
        """
        Start the application by displaying the user interface with the asyncio loop.
        """
        self.logger.info("🚀 Launching the application...")
        self.event_manager.notify("SIMULATION_STARTED", {"num_drones": self.num_drones, "formation": self.formation})
        self._tkinter_loop()

    def _tkinter_loop(self):
        """Event loop to update Tkinter without blocking asyncio."""
        if self.running:
            self.update()
            self.root.after(100, self._tkinter_loop)  # 10 ms = 0.01 s

def loop_worker(loop_: asyncio.AbstractEventLoop):
    """
    Thread for running the asyncio event loop
    """
    asyncio.set_event_loop(loop_)
    loop_.run_forever()

def main():
    loop = asyncio.new_event_loop()
    loop_thread = threading.Thread(target=loop_worker, args=(loop,), daemon=True)
    loop_thread.start()
    root = tk.Tk()
    app = DroneSwarmApp(loop, root)
    app.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    sys.exit(main())
