# AI Assignment 2 - Dynamic Pathfinding Agent

## Student Information
- **Name:** Tahreem Noor
- **Roll Number:** 24F-0559

## How to Run
1. Install pygame:
pip install pygame

text
2. Run the program:
python pathfinder.py

text
3. Follow prompts to enter:
- Grid rows and columns
- Obstacle density (0.0 to 1.0)
- Algorithm (1=A*, 2=Greedy)
- Heuristic (1=Manhattan, 2=Euclidean)

## Controls
| Key/Mouse | Action |
|-----------|--------|
| Left Click | Add wall |
| Right Click | Remove wall |
| R | Generate new random walls |
| C | Clear all walls |
| SPACE | Run search |
| D | Toggle dynamic mode |

## Colors
- 🟦 Blue: Start
- 🟪 Purple: Goal
- 🟨 Yellow: Frontier
- 🟥 Red: Visited/expanded
- 🟩 Green: Final path
- ⬛ Black: Walls

## Features
- A* and Greedy Best-First Search
- Manhattan and Euclidean heuristics
- Dynamic obstacles with auto-replanning
- Real-time metrics display
