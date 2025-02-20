class SimConfig:
    """
    Contains global parameters for the simulation.
    """

    NUM_DRONES: int = 10  # Number of drones in the simulation
    COLLISION_THRESHOLD: float = 1.0  # Minimum distance to consider a collision
    CONSENSUS_EPSILON: float = 0.1  # Tolerance for consensus algorithm
    FORMATION_TYPE: str = "line"  # Initial formation type of the drones
    SIMULATION_SPEED: float = 0.05  # Pause between each update in seconds
