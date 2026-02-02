# 7x7 Pipe Wrapping Puzzle (AI Search)

This project implements the state representation and successor generation for a **7x7 Pipe Wrapping Logic Puzzle**. The goal is to connect pairs of colored endpoints on a grid where paths can "wrap around" the edges (toroidal topology).

## Project Structure

- **`main.py`**: Contains the core logic.
    - `PipeState`: Represents the grid, current pipe positions, and goals.
    - `get_successors(state)`: Generates valid next moves from a given state, handling collision detection and wrap-around logic.
    - `is_goal(state)`: Checks if the puzzle is solved.
- **`test.py`**: A test bench to visualize the puzzle and verify the successor logic.
- **`implementation_plan.md`**: Development plan and notes.

## Usage

### Prerequisites
- Python 3.x

### Running the Test Bench
To verify the state logic and see the wrapping mechanics in action:

```bash
python test.py
```

> **Note**: If `test.py` fails with an `AttributeError`, check `main.py` and ensure the `from_string` and `__lt__` methods are uncommented, as the test script relies on them for easy setup.

## Class Documentation: `PipeState`

The `PipeState` class is designed to be used with standard AI search algorithms (BFS, DFS, A*).

### Attributes
- `grid`: 7x7 matrix. `0` represents empty space. Strings (e.g., `'A'`) represent colors.
- `current_positions`: Dictionary `{color: (row, col)}` tracking the *current head* of each pipe.
- `goals`: Dictionary `{color: (row, col)}` tracking the *target endpoint* for each pipe.
- `size`: Grid size (default 7).

### Key Methods
- `get_successors(state)`: Returns a list of valid `PipeState` objects reachable in one step.
    - Enforces "one active color moves at a time" strategy to reduce branching.
    - Handles toroidal wrapping: `(-1, 0)` wraps to `(6, 0)`.

## AI Assignment Details
This code is intended to serve as the backend for the "Search Algorithms" assignment.
- **Blind Search**: Can be solved with DFS/BFS.
- **Heuristic Search**: Compatible with A* (ensure `__lt__` is enabled).
