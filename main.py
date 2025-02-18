import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import numpy as np

from behaviors.consensus_algorithm import ConsensusAlgorithm
from behaviors.collision_avoidance_algorithm import CollisionAvoidanceAlgorithm
from behaviors.formation_control_algorithm import FormationControlAlgorithm
from visualizer import DroneSwarmVisualizer
from drone import Drone

class DroneSwarmApp:
    def __init__(self, root):
        """
        Initialize the Drone Swarm Simulation application.
        """
        self.root = root
        self.root.title("Drone Swarm Simulation")

        self.target_point = np.array([0, 0, 0])  # Initial target point
        self.is_x_at_origin = True  # State to track if the target is at the origin

        # Simulation parameters
        self.num_drones = 100  # Number of drones in the swarm
        self.iterations = 100  # Number of iterations (not currently used)
        self.epsilon = 0.1  # Parameter for the consensus algorithm
        self.collision_threshold = 1.0  # Minimum distance to avoid collisions
        self.interval = 200  # Time interval between simulation updates (ms)

        # UI control variables
        self.formation_type = tk.StringVar(value="line")  # Formation type selection
        self.zoom_level = tk.DoubleVar(value=10.0)  # Zoom level for visualization

        # Define behavior algorithms
        self.behavior_algorithms = [
            ConsensusAlgorithm(self.epsilon),
            CollisionAvoidanceAlgorithm(self.collision_threshold),
            FormationControlAlgorithm(self.formation_type.get())
        ]

        # Initialize the swarm with 3D random positions
        self.drones = [Drone(np.random.rand(3) * 10, i) for i in range(self.num_drones)]

        # Initialize the visualizer
        self.visualizer = DroneSwarmVisualizer(self.drones, self.formation_type.get())

        # Set up the UI
        self.setup_ui()

        # Simulation state
        self.running = True

    def setup_ui(self):
        """
        Set up the graphical user interface.
        """
        # Create a frame for controls
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Formation selection radio buttons
        ttk.Label(control_frame, text="Formation:").pack(anchor=tk.W)
        ttk.Radiobutton(control_frame, text="Line", variable=self.formation_type, value="line", command=self.update_formation).pack(anchor=tk.W)
        ttk.Radiobutton(control_frame, text="Circle", variable=self.formation_type, value="circle", command=self.update_formation).pack(anchor=tk.W)
        ttk.Radiobutton(control_frame, text="Square", variable=self.formation_type, value="square", command=self.update_formation).pack(anchor=tk.W)
        ttk.Radiobutton(control_frame, text="Random", variable=self.formation_type, value="random", command=self.update_formation).pack(anchor=tk.W)

        # Separator
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Zoom level control
        ttk.Label(control_frame, text="Zoom Level:").pack(anchor=tk.W)
        zoom_scale = ttk.Scale(control_frame, from_=5.0, to=20.0, orient=tk.HORIZONTAL, variable=self.zoom_level, command=self.update_zoom)
        zoom_scale.pack(anchor=tk.W)

        # Separator
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Color mode control
        ttk.Label(control_frame, text="Color Mode:").pack(anchor=tk.W)
        self.color_mode = tk.StringVar(value="fixed")
        ttk.Radiobutton(control_frame, text="Fixed Colors", variable=self.color_mode, value="fixed", command=self.update_color_mode).pack(anchor=tk.W)
        ttk.Radiobutton(control_frame, text="Distance Colors", variable=self.color_mode, value="distance", command=self.update_color_mode).pack(anchor=tk.W)

        # Separator
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Button to change the target position
        ttk.Button(control_frame, text="Change X Position", command=self.change_x_position).pack(pady=10)

        # Separator
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Start/Stop button
        self.start_button = ttk.Button(control_frame, text="Start", command=self.toggle_simulation)
        self.start_button.pack(pady=10)

        # Canvas to display the swarm visualization
        self.canvas = FigureCanvasTkAgg(self.visualizer.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    def update_formation(self):
        """
        Update the formation control algorithm when the user selects a different formation.
        """
        self.behavior_algorithms[-1] = FormationControlAlgorithm(self.formation_type.get())
        self.visualizer.formation_type = self.formation_type.get()
        self.canvas.draw()

    def update_zoom(self, event):
        """
        Update the visualization zoom level when the user adjusts the zoom slider.
        """
        self.visualizer.update_zoom(self.zoom_level.get())
        self.canvas.draw()

    def update_color_mode(self):
        """
        Update the color mode of the drones in the visualization.
        """
        self.visualizer.color_mode = self.color_mode.get()
        self.visualizer.update_colors()
        self.canvas.draw()

    def toggle_simulation(self):
        """
        Start or stop the simulation when the button is clicked.
        """
        if self.running:
            self.running = False
            self.start_button.config(text="Start")
        else:
            self.running = True
            self.start_button.config(text="Stop")
            threading.Thread(target=self.run_simulation).start()

    def change_x_position(self):
        """
        Toggle the target position between [20, 0, 0] and [0, 0, 0].
        """
        if self.is_x_at_origin:
            self.target_point = np.array([20, 0, 0])
        else:
            self.target_point = np.array([0, 0, 0])

        self.is_x_at_origin = not self.is_x_at_origin
        self.update_target_positions()

    def update_target_positions(self):
        """
        Update the target positions of the drones based on the current formation.
        """
        formation = self.behavior_algorithms[-1].get_formation(self.drones)
        for drone, target in zip(self.drones, formation):
            drone.target_position = self.target_point + target

        # Update the target point in the formation control algorithm
        self.behavior_algorithms[-1].set_target_point(self.target_point)

    def run_simulation(self):
        """
        Run the simulation loop, updating drone positions and refreshing the visualization.
        """
        while self.running:
            # Update each drone's position based on behavior algorithms
            for drone in self.drones:
                neighbor_positions = [other_drone.communicate() for other_drone in self.drones if other_drone != drone]
                drone.update_position(neighbor_positions, self.behavior_algorithms)

            # Update the view to follow the drones
            self.visualizer.update_view(self.drones)

            # Refresh visualization
            self.visualizer.update()
            self.canvas.draw()

# Main entry point for the application
def main():
    root = tk.Tk()
    app = DroneSwarmApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
