import numpy as np
import matplotlib.pyplot as plt
from typing import List

from ai.formation_control import FormationControl
from core.drone import Drone
from simulation.event_manager import EventManager
from visualization.color_manager import ColorManager

class SwarmVisualizer:
    """
    Manages the 3D display of the drone swarm.
    """

    def __init__(self, drones: List[Drone], event_manager: EventManager, formation_control: FormationControl) -> None:
        """
        Initialize the visualizer.

        Args:
            drones (List[Drone]): List of drones to display.
            event_manager (EventManager): Simulation event manager.
            formation_control (FormationControl): Formation control behavior.
        """
        self.drones = drones
        self.event_manager = event_manager
        self.formation_control = formation_control

        self.color_manager = ColorManager(mode="by_index")  # Initialize color manager
        self.dynamic_tracking = False  # Disabled by default
        self.target_point = np.array([0, 0, 0])  # Default value
        self.current_range = 10.0

        # Smoothing factor (closer to 1 = more reactive, closer to 0 = slower)
        self.smoothing_factor = 0.01

        self.fig = plt.figure()

        # Axes
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.set_xlim([-10, 10])
        self.ax.set_ylim([-10, 10])
        self.ax.set_zlim([-10, 10])
        self.ax.set_xlabel('X Axis', fontsize=12)
        self.ax.set_ylabel('Y Axis', fontsize=12)
        self.ax.set_zlabel('Z Axis', fontsize=12)

        # Adjust the viewing angle
        self.ax.view_init(elev=20, azim=-35)

        # Initialize with current drone positions
        positions = np.array([drone.get_position() for drone in self.drones])
        colors = self.color_manager.get_colors(self.drones)  # Get colors

        self.scat = self.ax.scatter(
            positions[:, 0], positions[:, 1], positions[:, 2], c=colors, s=50
        )

        self.update_plot()
        self.event_manager.subscribe("position_update", self.on_position_update)
        self.event_manager.subscribe("target_update", self.on_target_update)

    def update_plot(self) -> None:
        """Update the position of drones in the 3D display."""
        positions = np.array([drone.get_position() for drone in self.drones])

        if len(positions) > 0:
            self.scat._offsets3d = (positions[:, 0], positions[:, 1], positions[:, 2])

        # Update colors based on target positions
        self.scat.set_color(self.color_manager.get_colors(self.drones, self.formation_control))

        # If dynamic tracking is enabled, gradually adjust the scale
        if self.dynamic_tracking:
            min_pos = np.min(positions, axis=0)
            max_pos = np.max(positions, axis=0)
            new_range = np.max(max_pos - min_pos) / 2

            self.current_range = self.smoothing_factor * new_range + (1 - self.smoothing_factor) * self.current_range

            center = (min_pos + max_pos) / 2
            self.ax.set_xlim(center[0] - self.current_range, center[0] + self.current_range)
            self.ax.set_ylim(center[1] - self.current_range, center[1] + self.current_range)
            self.ax.set_zlim(center[2] - self.current_range, center[2] + self.current_range)

        plt.draw()

    def on_position_update(self, data: dict) -> None:
        """Handle position updates sent by the simulation."""
        index = data["index"]
        new_position = data["position"]

        self.drones[index].move(new_position)

        # Update target point for dynamic axis adjustment with smoothing
        if self.dynamic_tracking and hasattr(self, "target_point"):
            alpha = 0.1  # Smoothing coefficient (0.1 = 90% old value, 10% new value)
            self.target_point = alpha * new_position + (1 - alpha) * self.target_point

        self.update_plot()

    def on_target_update(self, data: dict) -> None:
        """Update the target point from events."""
        self.target_point = np.array(data["target_point"])

    def update_color_mode(self, mode: str) -> None:
        """Update the colorization mode and refresh the display."""
        self.color_manager.set_mode(mode)
        self.update_plot()

    def set_dynamic_tracking(self, enabled: bool) -> None:
        """Enable or disable dynamic tracking of the target point."""
        self.dynamic_tracking = enabled

    def show(self) -> None:
        """Display the simulation."""
        print("📡 Displaying Matplotlib...")  # Debug
        plt.ion()  # Enable interactive mode
        plt.show()

        while True:
            plt.pause(0.1)  # Force continuous refresh
