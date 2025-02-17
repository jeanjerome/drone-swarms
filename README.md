# Drone Swarm Simulation

A Python-based **drone swarm simulator** that models the behavior of multiple autonomous drones using different algorithms for **consensus**, **collision avoidance**, and **formation control**. The simulation is visualized in **3D** using Matplotlib and controlled through a Tkinter-based GUI.

![Drone Swarms](drone-swarms.png)

## 🚀 Features

- **Swarm Behavior Algorithms:**
  - **Consensus Algorithm:** Ensures cohesion by moving drones toward the average position of their neighbors.
  - **Collision Avoidance Algorithm:** Prevents drones from colliding by adjusting their trajectories dynamically.
  - **Formation Control Algorithm:** Organizes drones into structured formations (line, circle, or V-shape).
- **Interactive Visualization:**
  - Real-time 3D visualization of drone movements using **Matplotlib**.
  - Adjustable **zoom level** for better observation.
  - Supports **different formations** dynamically via the GUI.
- **Multi-threaded Simulation:** The swarm behavior runs in a separate thread to keep the UI responsive.

## 🛠️ Installation

### Prerequisites

- **Python 3.12+** is required.
- **Poetry** for dependency management.

### Install Poetry (if not installed)

```bash
pip install poetry
```

### Install Dependencies

Clone the repository and install dependencies using **Poetry**:

```bash
git clone https://github.com/jeanjerome/drone-swarms.git
cd drone-swarms
poetry install
```

## ▶️ Usage

Run the main script using Poetry:

```bash
poetry run python main.py
```

### UI Controls
- **Formation Selection:** Choose between line, circle, and V-shape formations.
- **Zoom Level:** Adjust zoom for better visualization.
- **Start/Stop Simulation:** Toggle the simulation on and off.

## 📂 Project Structure

```
📦 drone-swarms
│── 📜 main.py                  # Entry point for the simulation (Tkinter-based UI)
│── 📜 drone.py                 # Drone class defining behavior and communication
│── 📜 visualizer.py            # Matplotlib-based 3D visualization
│── 📂 behaviors                # Folder containing behavior algorithms
│   │── 📜 consensus_algorithm.py       # Consensus-based movement logic
│   │── 📜 collision_avoidance_algorithm.py  # Avoidance of drone collisions
│   │── 📜 formation_control_algorithm.py   # Formation control logic
│── 📜 README.md                # Project documentation
│── 📜 pyproject.toml           # Poetry configuration file
│── 📜 poetry.lock              # Poetry lockfile
```

## 🛠️ Customization

- **Change Number of Drones:** Modify `self.num_drones` in `main.py`.
- **Adjust Algorithm Parameters:** Modify `epsilon`, `collision_threshold`, or `formation_type` in `main.py`.

## 📖 Future Improvements

- [ ] Implement **Square formation** logic.
- 🔄 Add more **swarm behavior algorithms**:
  - [ ] **Obstacle Avoidance (Évitement d'Obstacles)**
   - **Description** : The drones detect and avoid static or dynamic obstacles in the environment.
   - **Implementation** : Introduce obstacles in the 3D space and apply a similar logic to collision avoidance to navigate around them.

  - [ ] **Path Planning (Planification de Trajectoire)**
     - **Description** : The drones plan and follow an optimal trajectory to reach a destination while avoiding obstacles.
     - **Implementation** : Use pathfinding algorithms like **A*** or **Dijkstra** to compute efficient routes in an environment with obstacles.

  - [ ] **Search and Rescue (Recherche et Sauvetage)**
     - **Description** : The drones explore an area to locate targets (e.g., distressed people) and coordinate their movements for efficient coverage.
     - **Implementation** : Implement **area coverage algorithms** and **collaborative search strategies**.

  - [ ] **Energy Management (Gestion de l'Énergie)**
     - **Description** : The drones manage their energy consumption to maximize flight time and prevent failures.
     - **Implementation** : Model energy consumption and adjust behaviors to save power (e.g., reducing speed or minimizing unnecessary movements).

  - [ ] **Communication Relay (Relais de Communication)**
     - **Description** : The drones act as relays to maintain communication between each other or with a base station, especially in environments where direct communication is limited.
     - **Implementation** : Model communication range and adjust drone positions dynamically to ensure network connectivity.

  - [ ] **Dynamic Task Allocation (Allocation Dynamique des Tâches)**
     - **Description** : The drones dynamically distribute tasks (e.g., surveillance, delivery) based on their capabilities and mission requirements.
     - **Implementation** : Use **optimization algorithms** for efficient task allocation in real-time scenarios.

  - [ ] **Flocking Behavior (Comportement de Vol en Essaim)**
     - **Description** : The drones follow swarm-inspired flight behaviors similar to birds or fish, incorporating alignment, cohesion, and separation.
     - **Implementation** : Implement **Reynolds' flocking rules** for realistic swarm movement.

- [ ] 🎮 Improve user interactivity in the **Tkinter GUI**.
- [ ]  📡 Introduce **real-world drone communication models**.

## 🤝 Contributing

Feel free to **fork**, **modify**, and **submit a pull request**! Suggestions and improvements are always welcome.  

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
