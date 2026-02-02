class PipeState:
    def __init__(self, grid, current_positions, goals, size=7):
        """
        grid: 2D list where 0 is empty, colors are strings/ints.
        current_positions: Dict {color: (r, c)} of the moving end of the pipe.
        goals: Dict {color: (r, c)} of the fixed destination.
        """
        self.grid = [row[:] for row in grid]
        self.current_positions = current_positions
        self.goals = goals
        self.size = size

    def __eq__(self, other):
        return self.grid == other.grid and self.current_positions == other.current_positions

    def __hash__(self):
        # Stable hash: Sort dictionary items to ensure same hash regardless of insertion order
        return hash((tuple(tuple(row) for row in self.grid), tuple(sorted(self.current_positions.items()))))

    # def __lt__(self, other):
    #     # Required for priority queues (heapq). 
    #     # Tie-breaking can be arbitrary, we'll use the grid state.
    #     return self.grid < other.grid

    # @staticmethod
    # def from_string(grid_str):
    #     """
    #     Parses a string representation of the grid.
    #     Letters (A-Z) are endpoints. '.' or '0' are empty.
    #     Returns a PipeState.
    #     """
    #     lines = [line.strip() for line in grid_str.strip().splitlines() if line.strip()]
    #     grid = []
    #     positions = {}
    #     goals = {}
        
    #     # Temporary storage to pair up endpoints
    #     endpoints = {}
        
    #     for r, line in enumerate(lines):
    #         row = []
    #         for c, char in enumerate(line):
    #             if char in '.0':
    #                 row.append(0)
    #             else:
    #                 # It's a color endpoint
    #                 row.append(char)
    #                 if char not in endpoints:
    #                     endpoints[char] = []
    #                 endpoints[char].append((r, c))
    #         grid.append(row)
            
    #     # Assign start/end. 
    #     # Arbitrarily pick first occurrence as "current_position" (head) and second as "goal".
    #     # In a real search, this might swap dynamically, but for init it's fine.
    #     for color, points in endpoints.items():
    #         if len(points) != 2:
    #             raise ValueError(f"Color {color} must have exactly 2 endpoints, found {len(points)}")
    #         positions[color] = points[0]
    #         goals[color] = points[1]
            
    #     return PipeState(grid, positions, goals, size=len(grid))

def is_goal(state):
    # 1. Check if all path heads have reached their goals
    for color, pos in state.current_positions.items():
        if pos != state.goals[color]:
            return False
    
    # 2. Check if the grid is completely filled (no zeros)
    for row in state.grid:
        if 0 in row:
            return False
            
    return True

def get_successors(state):
    successors = []
    
    # Identify the first color that still needs to move
    active_color = None
    for color, pos in state.current_positions.items():
        if pos != state.goals[color]:
            active_color = color
            break
            
    if active_color is None:
        return []

    r, c = state.current_positions[active_color]
    target = state.goals[active_color]

    # Standard moves + Wrap-around moves
    # (dr, dc): Up, Down, Left, Right
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        # Apply wrapping logic using modulo
        nr = (r + dr) % state.size
        nc = (c + dc) % state.size
        
        # Check if the move is valid: 
        # Must be empty OR the target endpoint for this color
        # IMPORTANT: If it's the target, it must be the target for THIS color.
        # Other colors' endpoints are obstacles.
        cell_value = state.grid[nr][nc]
        is_empty = (cell_value == 0)
        is_own_target = ((nr, nc) == target)
        
        if is_empty or is_own_target:
            # Create a deep copy of the grid for the new state
            new_grid = [row[:] for row in state.grid]
            new_grid[nr][nc] = active_color
            
            new_positions = state.current_positions.copy()
            new_positions[active_color] = (nr, nc)
            
            successors.append(PipeState(new_grid, new_positions, state.goals, state.size))
            
    return successors