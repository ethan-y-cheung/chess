# Chess AI Project

## Overview
This Chess AI project is a fully functional chess engine designed to evaluate board states and determine optimal moves. It integrates advanced algorithms and heuristic evaluation techniques to mimic human-like strategic thinking while leveraging computational power to explore possible moves efficiently.

## Features
- **Static Evaluation Function**: Assigns scores to board states based on material balance, piece activity, and positional factors (e.g., central control, pawn structure).
- **Positional Heuristics**: Includes advanced heuristics such as rewarding protected pawns and penalizing weaknesses like isolated pawns or trapped pieces.
- **Search Algorithms**:
  - **Principal Variation Search (PVS)**: Focuses on the most promising move sequences to optimize computational resources.
  - **Alpha-Beta Pruning**: Efficiently cuts off unproductive move branches, reducing search space.
- **Endgame Adjustments**: Dynamically shifts evaluation priorities to favor king activity and pawn promotion in the endgame phase.
- **Killer Move Heuristic**: Prioritizes previously successful moves to accelerate decision-making.
- **Memoization**: Caches previously evaluated board states to avoid redundant computations.

## Installation
### Prerequisites
- Python 3.8+
- Required libraries (install via `pip`):
  ```bash
  pip install Pillow
  pip install webcolors
  pip install pygame
  ```

### Clone Repository
```bash
git clone https://github.com/ethan-y-cheung/chess.git
cd chess-ai
```

## Usage
1. Run the GUI script to play against the AI:
   ```bash
   python chess_gui.py
   ```
   
## Project Structure
- `chess_gui.py`: Entry point for the program.
- `engine/`
  - `model.py`: Contains the methods for possible move calculation.
  - `hard_ai.py`: Implements PVS, alpha-beta pruning, and killer move logic.
  - `random_ai.py`: Standard structure for AI, plays at random.

## Example
Here’s a quick example of the AI making a move in the command line, outputting score and depth:
```bash
  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 
  ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
  . . . . . . . .
  . . . . . . . .
  . . . . ♙ . . .
  . . . . . . . .
  ♙ ♙ ♙ ♙ . ♙ ♙ ♙
  ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖

Turn killed after time limit.
('n', 12, 33) 23.74417740395657 3
('n', 12, 33)
('n', 12, 33) -37.155034045855444 4
('n', 12, 33)
('n', 17, 36) 19.384492824023624 5
('n', 17, 36)
```

## Future Improvements
- **Opening Book**: Add a database of pre-analyzed openings to enhance early-game play.
- **Neural Network Integration**: Experiment with machine learning for advanced evaluation.
- **ProbCut Algorithm**: Test the efficacy of adding the ProbCut algorithm.

## Acknowledgments
- Special thanks to the chess programming community for inspiration and resources.
