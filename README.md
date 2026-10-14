# Space Invaders

A classic Space Invaders game developed in Python using Pygame.

## Features

- Player movement and shooting mechanics.
- Enemy formations that move horizontally and descend when reaching the screen boundaries.
- Enemy projectiles and collision detection.
- Score tracking and player lives.
- Progressive difficulty with 10 levels.
- Increasing enemy speed as the level progresses.
- Level transitions and victory screen.
- Game over screen and restart functionality.
- Main menu.
- Configurable starting level for testing purposes.

## Technologies

- Python
- Pygame
- Git and GitHub

## Getting Started

### Requirements

- Python 3.10 or later recommended.
- pip

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Alex040901/space_invaders.git
   ```

2. Navigate to the project directory:

   ```bash
   cd space_invaders
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment.

   **Windows:**

   ```bash
   venv\Scripts\activate
   ```

5. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Run the Game

Start the game with:

```bash
python app.py
```

## Controls

| Key | Action |
|---|---|
| Left Arrow | Move left |
| Right Arrow | Move right |
| Spacebar | Shoot |
| Enter | Start or continue |
| Escape | Exit the game |

## Development

The project includes a configurable `NIVEL_PRUEBA` variable that allows testing specific levels without playing through the previous ones.

Set it to `1` to start testing from the first level or change it to another supported level to test later stages.

## Project Structure

```text
space_invaders/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/
```

The `venv/` directory is generated locally and should not be committed to the repository.

## Author

Developed as a personal programming project to practice Python, game logic, collision detection, and object-oriented programming.