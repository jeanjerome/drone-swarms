import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
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

        # Simulation parameters
        self.num_drones = 100  # Number of drones in the swarm
        self.dimensions = 3  # 3D space
        self.iterations = 100  # Number of iterations (not currently used)
        self.epsilon = 0.1  # Parameter for the consensus algorithm
        self.collision_threshold = 1.0  # Minimum distance to avoid collisions
        self.interval = 200  # Time interval between simulation updates (ms)

        # UI control variables
        self.formation_type = tk.StringVar(value="line")  # Formation type selection
        self.zoom_level = tk.DoubleVar(value=10.0)  # Zoom level for visualization

        # Initialize the swarm with random positions
        self.drones = [Drone(np.random.rand(self.dimensions) * 10, i) for i in range(self.num_drones)]
        
        # Define behavior algorithms
        self.behavior_algorithms = [
            ConsensusAlgorithm(self.epsilon),
            CollisionAvoidanceAlgorithm(self.collision_threshold),
            FormationControlAlgorithm(self.formation_type.get())
        ]

        # Initialize the visualizer
        self.visualizer = DroneSwarmVisualizer(self.drones)

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

        # Zoom level control
        ttk.Label(control_frame, text="Zoom Level:").pack(anchor=tk.W)
        zoom_scale = ttk.Scale(control_frame, from_=5.0, to=20.0, orient=tk.HORIZONTAL, variable=self.zoom_level, command=self.update_zoom)
        zoom_scale.pack(anchor=tk.W)

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

    def update_zoom(self, event):
        """
        Update the visualization zoom level when the user adjusts the zoom slider.
        """
        self.visualizer.update_zoom(self.zoom_level.get())
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

    def run_simulation(self):
        """
        Run the simulation loop, updating drone positions and refreshing the visualization.
        """
        while self.running:
            # Update each drone's position based on behavior algorithms
            for drone in self.drones:
                neighbor_positions = [other_drone.communicate() for other_drone in self.drones if other_drone != drone]
                drone.update_position(neighbor_positions, self.behavior_algorithms)

            # Refresh visualization
            self.visualizer.update()
            self.canvas.draw()
            
            # Wait for the next update interval
            time.sleep(self.interval / 1000)

# Main entry point for the application
def main():
    root = tk.Tk()
    app = DroneSwarmApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
