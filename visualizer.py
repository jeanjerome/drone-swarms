import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib.cm as cm

class DroneSwarmVisualizer:
    """
    This class visualizes a swarm of drones in a 3D space using Matplotlib.
    It updates their positions dynamically during the simulation.
    """
    
    def __init__(self, drones):
        """
        Initializes the visualizer with a list of drones.
        
        Parameters:
        - drones (list): List of Drone objects to be visualized.
        """
        self.drones = drones
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Generate colors for the drones using a colormap
        colormap = cm.hsv
        self.colors = colormap(np.linspace(0, 1, len(drones)))

        # Create a scatter plot to represent drone positions
        self.scat = self.ax.scatter(*zip(*[drone.get_position() for drone in self.drones]), c=self.colors)

        # Set initial zoom level
        self.zoom_level = 10.0
        self.update_zoom(self.zoom_level)

    def init(self):
        """
        Initializes the animation by setting the zoom level.
        Returns the scatter plot object.
        """
        self.update_zoom(self.zoom_level)
        return self.scat,

    def animate(self, frame):
        """
        Updates the positions of the drones during animation.

        Parameters:
        - frame (int): The current frame index (not used in this case).
        
        Returns:
        - self.scat (scatter plot object): Updated scatter plot with new positions.
        """
        positions = np.array([drone.get_position() for drone in self.drones])
        self.scat._offsets3d = (positions[:, 0], positions[:, 1], positions[:, 2])
        return self.scat,

    def update(self):
        """
        Manually updates the visualization (without animation).
        """
        self.animate(None)
        self.fig.canvas.draw()

    def update_zoom(self, zoom_level):
        """
        Updates the zoom level of the 3D plot.

        Parameters:
        - zoom_level (float): New zoom level to apply to the axes.
        """
        self.zoom_level = zoom_level
        self.ax.set_xlim(0, self.zoom_level)
        self.ax.set_ylim(0, self.zoom_level)
        self.ax.set_zlim(0, self.zoom_level)

    def show(self, iterations, interval):
        """
        Starts the animation and displays the simulation.

        Parameters:
        - iterations (int): Number of frames to animate.
        - interval (int): Time interval (milliseconds) between frames.
        """
        ani = animation.FuncAnimation(self.fig, self.animate, frames=iterations, init_func=self.init, blit=False, interval=interval)
        plt.show()
