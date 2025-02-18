import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap

class DroneSwarmVisualizer:
    """
    This class visualizes a swarm of drones in a 3D space using Matplotlib.
    It updates their positions dynamically during the simulation.
    """

    def __init__(self, drones, formation_type):
        """
        Initializes the visualizer with a list of drones.

        Parameters:
        - drones (list): List of Drone objects to be visualized.
        """
        self.drones = drones
        self.formation_type = formation_type
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.customize_axes()  # Customize the appearance of the axes
        self.color_mode = 'fixed'

        # Generate colors for the drones using a colormap
        colormap = cm.hsv
        self.colors = colormap(np.linspace(0, 1, len(drones)))

        # Create a scatter plot to represent drone positions
        self.scat = self.ax.scatter(*zip(*[drone.get_position() for drone in self.drones]), c=self.colors)

        # Set initial zoom level
        self.zoom_level = 10.0
        self.update_zoom(self.zoom_level)

        self.update_colors()

    def init(self):
        """
        Initializes the animation by setting the zoom level.
        Returns the scatter plot object.
        """
        self.update_zoom(self.zoom_level)
        return self.scat,

    def customize_axes(self):
        """
        Customizes the appearance of the 3D axes.
        """
        # Hide the axis planes
        self.ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

        # Hide the axis lines
        self.ax.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.ax.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.ax.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

        # Add labels to the axes
        self.ax.set_xlabel('X Axis', fontsize=12)
        self.ax.set_ylabel('Y Axis', fontsize=12)
        self.ax.set_zlabel('Z Axis', fontsize=12)

        # Add a grid for better visualization
        self.ax.grid(True)

        # Adjust the viewing angle
        self.ax.view_init(elev=20, azim=-35)

    def update_colors(self):
        """
        Updates the colors of the drones based on the selected color mode.
        """
        if self.color_mode == 'fixed':
            colormap = cm.hsv
            self.colors = colormap(np.linspace(0, 1, len(self.drones)))
        elif self.color_mode == 'distance':
            self.colors = self.calculate_colors_by_distance()

        self.scat.set_color(self.colors)

    def calculate_colors_by_distance(self):
        """
        Calculates colors based on the distance from the target positions.

        Returns:
        - colors (array): Array of colors corresponding to each drone.
        """
        # Calculate distances from target positions
        distances = [np.linalg.norm(drone.get_position() - drone.target_position) for drone in self.drones]

        # Normalize distances
        norm = plt.Normalize(vmin=min(distances), vmax=max(distances))

        # Create a custom colormap from green to red
        custom_cmap = LinearSegmentedColormap.from_list('green_red', ['green', 'yellow', 'red'])

        return custom_cmap(norm(distances))

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
        self.update_colors()
        return self.scat,

    def update(self):
        """
        Manually updates the visualization (without animation).
        """
        self.animate(None)
        self.fig.canvas.draw()

    def update_view(self, drones):
        """
        Updates the 3D view to center on the drones.

        Parameters:
        - drones (list of Drone): List of drone objects.
        """
        positions = np.array([drone.get_position() for drone in drones])
        min_pos = np.min(positions, axis=0)
        max_pos = np.max(positions, axis=0)
        center = (min_pos + max_pos) / 2
        range_ = np.max(max_pos - min_pos) / 2

        self.ax.set_xlim(center[0] - range_, center[0] + range_)
        self.ax.set_ylim(center[1] - range_, center[1] + range_)
        self.ax.set_zlim(center[2] - range_, center[2] + range_)

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
