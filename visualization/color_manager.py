import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
from typing import List

from ai.formation_control import FormationControl
from core.drone import Drone

class ColorManager:
    """
    Manages drone colors based on different criteria.
    """

    def __init__(self, mode: str = "fixed"):
        """
        Initialize the color manager.

        Args:
            mode (str): Color mode (fixed, by_index, by_distance).
        """
        self.mode = mode
        self.colormap = cm.hsv  # Used for color variation

    def set_mode(self, mode: str) -> None:
        """
        Set the coloration mode.

        Args:
            mode (str): "fixed", "by_index", "by_distance"
        """
        self.mode = mode

    def get_colors(self, drones: List[Drone], formation_control: FormationControl = None) -> np.ndarray:
        """
        Calculate drone colors based on the active mode.

        Args:
            drones (List[Drone]): List of drones.
            formation_control (FormationControl): Formation control behavior.

        Returns:
            np.ndarray: Drone colors as an RGBA array.
        """
        if self.mode == "by_index":
            return self.colormap(np.linspace(0, 1, len(drones)))

        elif self.mode == "by_distance":
            return self._calculate_colors_by_distance(drones, formation_control)

        return np.array(["blue"] * len(drones))  # Default "fixed" mode

    def _calculate_colors_by_distance(self, drones: List[Drone], formation_control: FormationControl) -> List[str]:
        """
        Calculate drone colors based on their distance to their target position defined by the formation.

        Args:
            drones (List[Drone]): List of drones.
            formation_control (FormationControl): Formation control behavior.

        Returns:
            List[str]: List of colors based on distances.
        """
        target_positions = [formation_control.apply(drone, drones) for drone in drones]

        distances = [np.linalg.norm(drone.get_position() - target) for drone, target in zip(drones, target_positions)]

        # Normalize and convert to colors
        norm = plt.Normalize(vmin=min(distances), vmax=max(distances))
        custom_cmap = LinearSegmentedColormap.from_list('green_red', ['green', 'yellow', 'red'])

        return custom_cmap(norm(distances))
