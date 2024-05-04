# Tetris AI

<div align="center">

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/CogitoNTNU/TetrisAI/ci.yml)
![GitHub top language](https://img.shields.io/github/languages/top/CogitoNTNU/TetrisAI)
![GitHub language count](https://img.shields.io/github/languages/count/CogitoNTNU/TetrisAI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Project Version](https://img.shields.io/badge/version-1.0.0-blue)](https://img.shields.io/badge/version-1.0.0-blue)

![logo](docs/img/Logo.webp)

</div>

## Description

This project is our attempt at making an AI that can play Tetris. First of all we made the environment (the game itself) and then we started working on multiple AI's that can play the game. The AI's are based on different algorithms and strategies. We have implmented:

- Random agent
- Heuristic agent with set weights
- Genetic algorithm to find the best weights for the heuristic agent

The game is playable/viable both in the terminal and in a GUI. The GUI is made with Pygame.

## How to run and install

- Have python installed (tested with 3.10+ but should work on older versions as well)
- Have pip installed
- Clone the repository
- Set up a virtual environment (optional but recommended) see [here](docs/guide/venv.md) for a guide
- Install the required packages with pip

```bash
pip install -r requirements.txt
```

- Done! You are now ready to run the game

## Usage

To play the game yourself, run the following command:
  
```bash
python main.py play
```

To let the agent play the game, run the following command:

```bash
python main.py agent <agent>
```

where `<agent>` is the agent you want to use. The available agents are: `random`, `heuristic`, `genetic`

To train the genetic agent, run the following command:

```bash
python main.py train
```

## Testing

To run the test suite, run the following command from the root directory of the project:

```bash
python -m pytest
```

## Team

The team behind this project is a group of students at NTNU in Trondheim, Norway, developed during the spring semester of 2024. The team consists of:

<table align="center">
    <tr>
        <td align="center">
                <a href="https://github.com/Eduard-Prokhorikhin">
                        <img src="https://github.com/Eduard-Prokhorikhin.png?size=100" width="100px;" alt="Eduard-Prokhorikhin"/><br />
                        <sub><b>Eduard Prokhorikhin</b></sub>
                </a>
        </td>
        <td align="center">
                <a href="https://github.com/henrinha">
                        <img src="https://github.com/henrinha.png?size=100" width="100px;" alt="henrinha"/><br />
                        <sub><b>Henrik Haaland</b></sub>
                </a>
        </td>
        <td align="center">
                <a href="https://github.com/HFossdal">
                        <img src="https://github.com/HFossdal.png?size=100" width="100px;" alt="HFossdal"/><br />
                        <sub><b>Håvard Fossdal</b></sub>
                </a>
        </td>
        <td align="center">
                <a href="https://github.com/JonBergland">
                        <img src="https://github.com/JonBergland.png?size=100" width="100px;" alt="JonBergland"/><br />
                        <sub><b>Jon Bergland</b></sub>
                </a>
        </td>
        <td align="center">
                <a href="https://github.com/maiahi">
                        <img src="https://github.com/maiahi.png?size=100" width="100px;" alt="maiahi"/><br />
                        <sub><b>Maia Austigard</b></sub>
                </a>
        </td>
        <td align="center">
                <a href="https://github.com/oystkva">
                        <img src="https://github.com/oystkva.png?size=100" width="100px;" alt="oystkva"/><br />
                        <sub><b>Øystein Kvandal</b></sub>
                </a>
        </td>
        <td align="center">
                <a href="https://github.com/SindreFossdal">
                        <img src="https://github.com/SindreFossdal.png?size=100" width="100px;" alt="SindreFossdal"/><br />
                        <sub><b>Sindre Fossdal</b></sub>
                </a>
        </td>
    </tr>
</table>

![Group picture](docs/img/Team.png)
