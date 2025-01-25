# Boids Simulation with **Pygame** | ASFOUR 🐦💣

Welcome to the **Boids Simulation with Predator**! This project is a visual and interactive simulation of boid behavior, featuring dynamic flocking and a predator. It also includes exciting interactive modes, allowing you to experiment with different behaviors and even have fun dropping bombs to eliminate boids!

## 🌟 Key Features
- Real-time simulation of boid behaviors: **separation**, **alignment**, and **cohesion**.
- A **predator** that dynamically hunts boids.
- **Interactive modes** for unique simulations:
  - **Mouse Interaction Mode**: Control boids' behavior with your mouse.
  - **Wind Mode**: Push the boids using directional wind forces.
  - **Lemniscate Mode**: Watch boids follow a mesmerizing figure-eight path.
- Have fun **dropping bombs** from the plane to eliminate boids!
- Adjustable FPS and boid count for performance testing.

## 🎮 Modes and How to Play

### 🔄 Lemniscate Mode
- **Activation**: Press **8** on your keyboard.
- **Description**: Boids will follow a smooth figure-eight path.

### 🖱️ Mouse Interaction Mode
- **Activation**: Press **I**.
- **Description**: Boids are attracted to the mouse but avoid getting too close to its center.

### 🌬️ Wind Mode
- **Activation**: Press **V** to toggle wind mode.
- **Controls**:
  - **W**: Wind blows upward.
  - **A**: Wind blows left.
  - **S**: Wind blows downward.
  - **D**: Wind blows right.
  - **V**: Stop the wind.

### 💣 Bomb Dropping
- **How to Use**: Press **B** to drop bombs from the plane.
- **Description**: Bombs explode on contact, eliminating nearby boids. It's a fun way to control their numbers or add excitement to the simulation!


## 🚀 Getting Started

### Prerequisites
- Python 3.7 or later
- Pygame library

Install Pygame using pip:
```bash
pip install pygame
```


---


## How to Run
1. Clone the repository:
```bash
git clone https://github.com/your-repo/BoidsSimul.git
```
2. Navigate to the project directory:
```bash
cd BoidsSimul
```
3. Run the simulation:
```bash
python Asfour_finalVersion.py
```

---

## 🎮 Controls Overview
Arrow Up: Add a boid to the simulation.
Arrow Down: Remove a boid from the simulation.
Space: Pause/unpause the simulation.
Esc: Exit the program.
B: Drop bombs from the plane.

## 📊 Performance Testing
The simulation dynamically adjusts for performance based on the number of boids. To test the FPS:

1. Open the code and modify the BOID_COUNT variable to set the number of boids (e.g., 50, 500, 2000).
2. Run the simulation and observe the FPS displayed in the terminal.

## 💡 Tips for Fun
- Experiment with the different modes to see how boids react.
- Combine Wind Mode with Mouse Interaction for chaotic and exciting boid movements.
- Drop bombs strategically to clear the boids or create dramatic effects in the simulation!

  ![Screenshot 2024-12-15 163946](https://github.com/user-attachments/assets/ba5999fd-afd5-4b28-b092-556960181e2e)

## 🚀 External Extension: Optimized FPS for Large Boid Simulations
To handle hundreds or thousands of boids efficiently, launch the OptimisationFPS(extension_externe).py file. This extension ensures smooth performance even with a large number of boids. It dynamically adjusts simulation parameters to optimize the frame rate.

Simply run the script, and for testing its effectiveness, try changing the number of boids by modifying the BOID_COUNT parameter in the code.

![image](https://github.com/user-attachments/assets/4078dadc-a7a3-4356-842c-0596c7251b26)

## 📄 Detailed Report
This section includes a downloadable PDF that provides an in-depth explanation IN FRENCH of the project's purpose, design, and implementation. It dives into the technical aspects, including boid behavior, interaction modes, and the logic behind specific features. Consult the file to understand the detailed thought process and methodology used throughout the project.

[Rapport_detaille_ASFOUR.pdf](https://github.com/user-attachments/files/18548231/Rapport_detaille_ASFOUR.pdf)

## 🛠️ User Manual
This section features a PDF user manual that guides you - IN FRENCH - through setting up and interacting with the simulation. It explains how to activate different modes, adjust parameters, and use the various features, including dropping bombs to interact with the boids. The document is designed to make the simulation easy and fun to explore—check it out for all the details!

[Notice_d'utilisation_ASFOUR.pdf](https://github.com/user-attachments/files/18548238/Notice_d.utilisation_ASFOUR.pdf)

## 📄 License
This project is licensed under the MIT License. See the `LICENSE` file for details.

Feel free to explore, play, and customize the simulation to your liking. Enjoy watching the boids in action!
This version emphasizes the interactive and fun aspects of the project while keeping it simple and engaging. Let me know if you need further tweaks!


## 👨‍💻 **Authors**

- > AHMED SALAH ALI Adham
- > ELAYOUBI Hadi
- > AIBOUD Lyes
