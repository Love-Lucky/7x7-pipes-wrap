from main import PipeState, get_successors

def print_state(state):
    """
    Prints the grid in a human-readable format.
    Uses basic chars for now, but could use ANSI colors.
    """
    print("-" * (state.size * 2 + 1))
    for r in range(state.size):
        row_str = "|"
        for c in range(state.size):
            val = state.grid[r][c]
            # Print current head as bold/different if needed, 
            # simplified here to just show the char
            char = str(val if val != 0 else ' ')
            row_str += char + "|"
        print(row_str)
    print("-" * (state.size * 2 + 1))
    print(f"Active Heads: {state.current_positions}")
    print()

def manual_test():
    print("=== TEST 1: Simple Wrap Case ===")
    
    # A simple 3x3 grid for testing ease
    # A . .
    # . . .
    # . . A
    # A needs to wrap from (0,0) to (2,2)? No, wait. 
    # Let's say A is at (0,0) and Goal is (0,2).
    # Path could be (0,0)->(0,1)->(0,2) OR (0,0)->wrap-left->(0,2) if adjacent
    
    # Let's use the from_string method I just added.
    # 5x5 grid
    # A is at (0,0), Goal A is at (0,4)
    # This tests direct wrap: (0,0) -> (0, -1) -> (0,4)
    puzzle_str = """
    A000A
    00000
    00000
    00000
    00000
    """
    
    initial_state = PipeState.from_string(puzzle_str)
    print("INITIAL STATE:")
    print_state(initial_state)
    
    print("SUCCESSORS (Level 1):")
    succs = get_successors(initial_state)
    
    found_wrap_move = False
    
    for i, s in enumerate(succs):
        print(f"Option {i+1}:")
        print_state(s)
        
        # Check if we wrapped to column 4
        head_pos = s.current_positions['A']
        if head_pos == (0, 4):
            print(">>> Found WRAP move to goal! <<<")
            found_wrap_move = True
        elif head_pos == (0, 1):
             print(">>> Found standard move right <<<")
        elif head_pos == (1, 0):
             print(">>> Found standard move down <<<")
        elif head_pos[0] == 4: # Row 4
             print(">>> Found WRAP move vertical! <<<")

    if not found_wrap_move:
        # Note: If A is adjacent to goal via wrap, it MIGHT be 
        # that it just moved directly onto the goal.
        # Ideally we see it fill the goal.
        pass

if __name__ == "__main__":
    manual_test()
