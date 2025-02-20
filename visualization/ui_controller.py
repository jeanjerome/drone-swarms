import asyncio
import logging
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from visualization.swarm_visualizer import SwarmVisualizer
from simulation.swarm_simulation import SwarmSimulation
from ai.formation_control import FormationControl

class UIController:
    """
    Manages the Tkinter user interface for the simulation.
    """

    def __init__(self, root: tk.Tk, simulation: SwarmSimulation, visualizer: SwarmVisualizer, loop: asyncio.AbstractEventLoop) -> None:
        """
        Initialize the interface.

        Args:
            root (tk.Tk): Main Tkinter window.
            simulation (SwarmSimulation): Simulation object.
            visualizer (SwarmVisualizer): Drone swarm visualizer.
            loop (asyncio.AbstractEventLoop): Main event loop.
        """
        self.root = root
        self.logger = logging.getLogger(__name__)
        self.simulation = simulation
        self.visualizer = visualizer
        self.loop = loop
        self.root.title("Drone Swarm Controller")

        # UI variables
        self.formation_type = tk.StringVar(value="line")
        self.target_point = np.array([0, 0, 0])  # New target point
        self.color_mode = tk.StringVar(value="by_index")
        self.zoom_level = tk.DoubleVar(value=10.0)
        self.simulation.running = False

        # Create UI components
        self.setup_ui()

    def setup_ui(self) -> None:
        """
        Initialize the user interface components.
        """
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Formation selection
        ttk.Label(control_frame, text="Formation:").pack(anchor=tk.W, pady=5)
        for formation in ["line", "circle", "square", "random"]:
            ttk.Radiobutton(control_frame, text=formation.capitalize(), variable=self.formation_type, value=formation,
                            command=self.update_formation).pack(anchor=tk.W)

        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Movement
        ttk.Button(control_frame, text="Move to new point", command=self.move_drones).pack(pady=10)

        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Color mode selection
        ttk.Label(control_frame, text="Colorization:").pack(anchor=tk.W, pady=5)
        for mode in ["fixed", "by_index", "by_distance"]:
            ttk.Radiobutton(control_frame, text=mode.replace("_", " ").capitalize(), variable=self.color_mode, value=mode,
                            command=self.update_color_mode).pack(anchor=tk.W)

        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Dynamic Tracking
        self.dynamic_tracking = tk.BooleanVar(value=False)
        ttk.Checkbutton(control_frame, text="Dynamic Tracking", variable=self.dynamic_tracking,
                        command=self.toggle_dynamic_tracking).pack(anchor=tk.W)

        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Start/Stop button
        self.start_button = ttk.Button(control_frame, text="Start", command=self.toggle_simulation)
        self.start_button.pack(pady=10)

        # Canvas for visualizer
        self.canvas = FigureCanvasTkAgg(self.visualizer.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def update_formation(self) -> None:
        """Update the formation and display."""
        new_formation = self.formation_type.get()
        print(f"📢 Updating formation -> {new_formation}")

        # Update FormationControl behavior
        for behavior in self.simulation.behavior_manager.behaviors:
            if isinstance(behavior, FormationControl):
                behavior.formation_type = new_formation

        if self.simulation.running:
            # Recalculate positions with the new formation
            new_positions = self.simulation.behavior_manager.compute_positions(self.simulation.drones)
            for drone, new_position in zip(self.simulation.drones, new_positions):
                drone.move(new_position)

            self.visualizer.update_plot()

    def move_drones(self) -> None:
        """Change the target position and update the formation."""
        self.target_point = np.random.rand(3) * 30 - 15  # New random position
        print(f"🎯 New target: {self.target_point}")

        for behavior in self.simulation.behavior_manager.behaviors:
            if isinstance(behavior, FormationControl):
                behavior.target_point = self.target_point

    def update_color_mode(self) -> None:
        """Update the colorization mode in the visualizer."""
        mode = self.color_mode.get()
        print(f"🎨 Changing colorization mode -> {mode}")
        self.visualizer.update_color_mode(mode)

    def toggle_dynamic_tracking(self):
        """Enable or disable dynamic tracking of the target point."""
        state = "enabled" if self.dynamic_tracking.get() else "disabled"
        print(f"📡 Dynamic Tracking {state}")
        self.visualizer.set_dynamic_tracking(self.dynamic_tracking.get())

    def toggle_simulation(self) -> None:
        """Start or stop the simulation properly."""
        if self.simulation.running:
            self.logger.debug("Stopping the simulation...")
            self.simulation.stop()  # Direct call if stop is not a coroutine
            self.root.after(0, lambda: self.start_button.config(text="Start"))  # Thread-safe button update
            self.logger.debug("Button updated: Start")
        else:
            self.logger.debug("Starting the simulation...")
            asyncio.run_coroutine_threadsafe(self.simulation.start(), self.loop)
            self.root.after(0, lambda: self.start_button.config(text="Stop"))  # Thread-safe button update
            self.logger.debug("Button updated: Stop")
