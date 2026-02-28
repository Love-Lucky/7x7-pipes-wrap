# Presentation Script: Class State and get_successors

## 1. Class State (PipeState)

### 1.1. Introduction

The **State** class in the 7x7 Pipes Wrap Puzzle is called **PipeState**. It represents the puzzle state at a given moment as a **grid of pipe tiles**.

Each cell is a **Tile** with:
- **Tile type** (TileType): EMPTY, STRAIGHT, CORNER, T_JUNCTION, CROSS
- **Rotation**: 0, 1, 2, 3 (0°, 90°, 180°, 270°)

### 1.2. PipeState Structure

```
PipeState
├── grid: List[List[Tile]]  — 2D grid of pipe tiles
└── size: int               — Grid size (7 for 7x7 board)
```

- **grid**: 2D array; each element is a `Tile` (type + rotation).
- **size**: Board size, typically 7 (7x7).

### 1.3. Key Properties

- **Immutable for comparison**: Each state is hashed and compared by the full grid, used for `visited` set and priority queue.
- **Deep copy**: When creating a new state, the grid is deep-copied to avoid modifying the previous state.
- **Wrap-around**: The grid is **toroidal** – top edge connects to bottom, left to right.

### 1.4. Main Methods

| Method | Description |
|--------|-------------|
| `get_tile(r, c)` | Get tile at position (r, c) |
| `set_tile(r, c, tile)` | Create new state with tile at (r, c) changed |
| `from_string(s)` | Parse string into PipeState (read from input file) |

---

## 2. get_successors – Generating Valid Next Moves

### 2.1. Definition

**get_successors(state)** returns a list of **next states** reachable from the current state by **one valid move**.

In this puzzle, a **move** is: **rotate one pipe tile 90°** (clockwise or counter-clockwise).

### 2.2. Rotatable Tiles

- **EMPTY**: Cannot rotate.
- **CROSS (+)**: Rotation does not change shape → skip.
- **Others** (STRAIGHT, CORNER, T_JUNCTION): Each has 2–4 distinct orientations → each 90° rotation yields one successor.

### 2.3. Two Successor Modes

#### Optimized mode (optimized = True) – default

Only rotate tiles **related to open ends**:

1. Find all tiles with **at least one unconnected pipe end**.
2. Add their **neighbors** (rotating neighbors can connect/disconnect).
3. For each tile in the list: rotate 90°, create new state, add to successors.

**Benefit**: Fewer successors, faster search (A*, BFS, DFS).

#### Full mode (optimized = False)

Rotate **all** non-EMPTY and non-CROSS tiles:

- Iterate over the entire grid.
- For each pipe tile: rotate 90°, create new state, add to successors.

**Drawback**: Many successors, slower search.

### 2.4. Successor Generation (Optimized Mode)

```
Step 1: Call get_tiles_with_open_ends(state)
        → Returns set of positions (r, c) to consider rotating

Step 2: For each (r, c) in the set:
        - tile = state.get_tile(r, c)
        - Skip if tile is CROSS
        - rotated_tile = tile.rotate(1)   // rotate 90°
        - new_state = state.set_tile(r, c, rotated_tile)
        - Add new_state to successors list

Step 3: Return successors list
```

---

## 3. BFS – Breadth-First Search

### 3.1. Idea

BFS explores the state space **level by level**: states closer to the start are expanded first. Guarantees finding the **shortest path** (minimum steps) if a solution exists.

### 3.2. Data Structures in Code

```python
frontier = deque([(initial_state, [initial_state])])  # FIFO queue
visited = {initial_state}                             # Set of visited states
```

- **frontier**: `deque` queue; each element is `(state, path)`.
- **visited**: Set of visited states to avoid duplicates.

### 3.3. Procedure (from code)

1. **Init**: Add `(initial_state, [initial_state])` to frontier, add initial_state to visited.
2. **Loop**:
   - Pop `(current_state, path)` from **front** of frontier (`popleft`).
   - For each `successor` from `get_successors(current_state)`:
     - If `successor not in visited`: add to visited, `new_path = path + [successor]`.
     - If `is_goal(successor)` → return solution.
     - Else → push `(successor, new_path)` to **back** of frontier.
3. **End**: If frontier empty and no goal found → no solution.

### 3.4. Characteristics

- **Blind search**: No heuristic.
- **Optimal**: Finds shortest path (minimum steps).
- **Drawback**: High memory (entire frontier can be huge on 7x7).

---

## 4. DFS – Depth-First Search

### 4.1. Idea

DFS goes **deep** into one branch first, backtracks when no moves remain. Uses **stack** (LIFO) instead of queue.

### 4.2. Data Structures in Code

```python
frontier = [(initial_state, [initial_state], 0)]  # Stack: (state, path, depth)
visited = {initial_state}
max_depth = 1000  # Depth limit to avoid infinite search
```

- **frontier**: List used as stack; each element is `(state, path, depth)`.
- **max_depth**: States with `depth >= max_depth` are not expanded.

### 4.3. Procedure (from code)

1. **Init**: Add `(initial_state, [initial_state], 0)` to frontier.
2. **Loop**:
   - Pop `(current_state, path, depth)` from **end** of frontier (`pop`).
   - If `depth >= max_depth` → skip (do not expand).
   - For each `successor` from `get_successors(current_state)`:
     - If `successor not in visited`: add to visited, `new_path = path + [successor]`.
     - If `is_goal(successor)` → return solution.
     - Else → push `(successor, new_path, depth + 1)` to **end** of frontier.
3. **End**: If frontier empty → no solution.

### 4.4. Characteristics

- **Blind search**: No heuristic.
- **Not optimal**: May find a longer path.
- **Advantage**: Lower memory than BFS (only stores path from root to current node on stack).

---

## 5. Heuristic Function h(n)

### 5.1. Definition

**Heuristic h(n)** estimates the **cost** from state `n` to the goal. In code:

```python
def heuristic(state: PipeState) -> int:
    open_ends = count_open_ends(state)
    return open_ends // 2
```

### 5.2. count_open_ends

- Counts **unconnected pipe ends** on the board.
- For each tile connection: if not connected to a neighbor (or neighbor lacks opposite connection) → counts as 1 open end.
- **Goal**: All pipes closed → `count_open_ends == 0`.

### 5.3. Formula h(n)

```
h(n) = count_open_ends(state) // 2
```

- **Divide by 2**: Each correct connection joins 2 open ends, reducing count by 2.
- h(n) estimates **minimum steps** needed to close all open ends.
- h(n) = 0 iff `is_goal(state)`.

### 5.4. Admissibility

- Each step (rotate 1 tile) can reduce at most 2 open ends.
- So actual steps ≥ number of pairs to connect ≥ `open_ends // 2`.
- → h(n) **never overestimates** cost to goal → **admissible** (suitable for A*).

---

## 6. A* Algorithm

### 6.1. Evaluation Formula f(n)

```
f(n) = g(n) + h(n)
```

- **g(n)**: Actual cost from start to n (in code: number of steps = `len(path) - 1`).
- **h(n)**: Estimated cost from n to goal (`heuristic(state)`).
- **f(n)**: Estimated total cost of path through n.

### 6.2. Structure in Code

```python
# Init
g_score = 0
h_score = heuristic(initial_state)
f_score = g_score + h_score
frontier = [(f_score, counter, g_score, initial_state, [initial_state])]  # Min-heap
visited = {initial_state}
```

- **frontier**: Min-heap (priority queue) ordered by **f_score** (lowest f first).
- **counter**: Tie-breaker when f values are equal (FIFO).
- Each element: `(f, counter, g, state, path)`.

### 6.3. Procedure (from code)

1. Pop state with **lowest f** from heap (`heappop`).
2. For each successor:
   - `new_g = current_g + 1` (each step costs 1).
   - `new_h = heuristic(successor)`.
   - `new_f = new_g + new_h`.
   - If `is_goal(successor)` → return solution.
   - If `successor not in visited`: add to visited, push `(new_f, counter, new_g, successor, new_path)` to heap.

### 6.4. Characteristics

- **Informed search**: Uses heuristic to guide search.
- **Optimal** (when h is admissible): Finds shortest path.
- **Efficient**: Usually explores fewer nodes than BFS thanks to h(n) guiding toward goal.

---

## 7. Hill Climbing Algorithm

### 7.1. Idea

Hill Climbing is **local search**: at each step, consider successors and choose the one with **lowest h(n)** (closest to goal by heuristic). No backtracking.

### 7.2. Procedure in Code

1. **Init**: `current_state = initial_state`, `path = [initial_state]`, `visited = {initial_state}`.
2. **Loop** (up to `max_iterations`):
   - `successors = get_successors(current_state)`.
   - Filter `unvisited_successors`.
   - If no unvisited successors → **stuck** (local minimum or plateau).
   - Compute `h(successor)` for each unvisited successor.
   - Sort by h ascending, take `best_successor` (lowest h).
   - Compare `best_h` with `current_h = heuristic(current_state)`:
     - If `best_h >= current_h` → **stuck** (no better successor).
     - Else → `current_state = best_successor`, add to path, continue.
3. **End**: Goal found, stuck, or max iterations reached.

### 7.3. Characteristics

- **Greedy**: Each step picks the “best” move by h.
- **Fast**: No large frontier, follows a single path.
- **Drawback**: Can get **stuck** at local minimum (all successors have h ≥ current h) or plateau (many states with same h).

## 8. Examples by Difficulty: Easy – Medium – Hard – Extreme

### 8.1. EASY Test (test01_easy_tiny)

**Description**: One small 3×3 pipe box in top-left corner, rest empty.

**Initial state**:
```
---------
|└─┐    |
|│ │    |
|┌─┘    |
|       |
|       |
|       |
|       |
---------
```

- **Open ends**: 8
- **Structure**: 1 simple pipe loop (one small box)
- **A* result**: SOLVED in ~0.7s, 268 nodes, 9 steps
- **Goal state**:
```
|┌─└    |
|│ │    |
|┐─┘    |
```

**Presentation notes**:
- Few open ends (8) → small search space.
- Few rotations needed to close the loop → A* is fast with few nodes.
- Good for demo: simple state, easy to visualize.

---

### 8.2. MEDIUM Test (test07_medium_l_shape)

**Description**: Large L-shape, more pipe tiles, more complex structure.

**Initial state**:
```
---------
|└─┐    |
|│ │    |
|│ ┌─┐  |
|│   │  |
|│   │  |
|│   │  |
|┌───┘  |
---------
```

- **Open ends**: 14
- **Structure**: 1 L-shape loop with nested branch
- **A* result**: SOLVED in ~171s, 27,982 nodes, 14 steps
- **Goal state**:
```
|┌─└    |
|│ │    |
|│ ┐─└  |
|│   │  |
|│   │  |
|│   │  |
|┐───┘  |
```

**Presentation notes**:
- More open ends (14) → more wrong rotations, larger search space.
- L-shape with many connected tiles → many rotation orders to try.
- ~3 minutes, ~285 MB RAM → medium difficulty, still runs stably.

---

### 8.3. HARD Test (test04_hard_two)

**Description**: Two separate pipe boxes – one top-left, one bottom-right.

**Initial state**:
```
---------
|└─┐    |
|│ │    |
|┌─┘    |
|       |
|    └─┐|
|    │ │|
|    ┌─┘|
---------
```

- **Open ends**: 16
- **Structure**: 2 independent pipe loops, far apart
- **A* result**: SOLVED in ~18 min (1098s), 218,974 nodes, 17 steps
- **Goal state**:
```
|┌─└    |
|│ │    |
|┐─┘    |
|       |
|    ┌─└|
|    │ │|
|    ┐─┘|
```

**Presentation notes**:
- Two independent loops → A* must close each; rotation order and choices matter.
- 16 open ends, many rotatable tiles → high branching factor.
- ~1.75 GB RAM, ~18 min → hard, requires significant resources.
- Illustrates: “multiple separate loops” makes the problem noticeably harder.

---

### 8.4. EXTREME Test (test14_extreme_cross)

**Description**: Nearly full board, many CROSS (┼) tiles, very many open ends.

**Initial state**:
```
---------
|└─┐ └─┐|
|││┼ ││┼|
|┌─┘┌─┘│|
|└─┼ └┼┐|
|││┼ ││┼|
|┌─┘┌─┘│|
|       |
---------
```

- **Open ends**: 40
- **Non-empty tiles**: 38/49
- **Feature**: Many CROSS (┼) tiles – 4-way connections; rotation does not change shape but still increases complexity when combined with other tiles.

**Result**: NOT RUN (simulated) – OOM (Out of Memory) risk

**Presentation notes**:
- 40 open ends → very large initial h(n), huge state space.
- Many CROSS + wrap-around → very high branching factor; frontier and visited set can reach millions of states.
- RAM may exceed machine limits → this test illustrates the **limits** of the algorithm on 7×7 boards.
- Implication: for very hard configurations, stronger heuristics or time/memory limits are needed.
