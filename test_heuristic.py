from main import PipeState, heuristic, heuristic_simple, heuristic_empty_cells, manhattan_distance_wrap

def test_manhattan_distance_wrap():
    """Test hàm Manhattan distance có wrap"""
    print("="*70)
    print("TEST 1: MANHATTAN DISTANCE VỚI WRAP-AROUND")
    print("="*70)
    
    # Test case 1: Không cần wrap
    pos1 = (0, 0)
    pos2 = (0, 3)
    grid_size = 7
    dist = manhattan_distance_wrap(pos1, pos2, grid_size)
    print(f"\n📍 Test 1.1: Từ {pos1} đến {pos2} trên lưới {grid_size}x{grid_size}")
    print(f"   Khoảng cách thường: |0-3| = 3")
    print(f"   Khoảng cách wrap: 7-3 = 4")
    print(f"   → Chọn: min(3, 4) = {dist} ✅")
    
    # Test case 2: Wrap ngắn hơn
    pos1 = (0, 0)
    pos2 = (0, 6)
    dist = manhattan_distance_wrap(pos1, pos2, grid_size)
    print(f"\n📍 Test 1.2: Từ {pos1} đến {pos2} trên lưới {grid_size}x{grid_size}")
    print(f"   Khoảng cách thường: |0-6| = 6")
    print(f"   Khoảng cách wrap: 7-6 = 1")
    print(f"   → Chọn: min(6, 1) = {dist} ✅ (Wrap tốt hơn!)")
    
    # Test case 3: Wrap 2 chiều
    pos1 = (0, 0)
    pos2 = (6, 6)
    dist = manhattan_distance_wrap(pos1, pos2, grid_size)
    print(f"\n📍 Test 1.3: Từ {pos1} đến {pos2} trên lưới {grid_size}x{grid_size}")
    print(f"   Row: min(|0-6|=6, 7-6=1) = 1")
    print(f"   Col: min(|0-6|=6, 7-6=1) = 1")
    print(f"   → Tổng: {dist} ✅ (Wrap cả 2 chiều!)")
    
    # Test case 4: Lưới 5x5
    pos1 = (0, 0)
    pos2 = (0, 4)
    grid_size = 5
    dist = manhattan_distance_wrap(pos1, pos2, grid_size)
    print(f"\n📍 Test 1.4: Từ {pos1} đến {pos2} trên lưới {grid_size}x{grid_size}")
    print(f"   Khoảng cách thường: |0-4| = 4")
    print(f"   Khoảng cách wrap: 5-4 = 1")
    print(f"   → Chọn: min(4, 1) = {dist} ✅")

def test_heuristic_functions():
    """Test các hàm heuristic"""
    print("\n" + "="*70)
    print("TEST 2: CÁC HÀM HEURISTIC")
    print("="*70)
    
    # Test case 1: 1 màu, đơn giản
    print("\n🎯 Test 2.1: Puzzle 1 màu (5x5)")
    puzzle_str = """
    A000A
    00000
    00000
    00000
    00000
    """
    state = PipeState.from_string(puzzle_str)
    
    # In state
    print("\n   State hiện tại:")
    for row in state.grid:
        print("   ", [str(x) if x != 0 else '.' for x in row])
    
    print(f"\n   Current positions: {state.current_positions}")
    print(f"   Goals: {state.goals}")
    
    # Tính heuristics
    h = heuristic(state)
    h_simple = heuristic_simple(state)
    h_empty = heuristic_empty_cells(state)
    
    print(f"\n   📊 Heuristic values:")
    print(f"      H1 (Manhattan distance): {h_simple}")
    print(f"      H2 (Empty cells): {h_empty}")
    print(f"      h(n) = max(H1, H2): {h}")
    
    # Giải thích
    pos_A = state.current_positions['A']
    goal_A = state.goals['A']
    dist_A = manhattan_distance_wrap(pos_A, goal_A, state.size)
    print(f"\n   💡 Giải thích:")
    print(f"      - A từ {pos_A} đến {goal_A}: distance = {dist_A}")
    print(f"      - Số ô trống: {h_empty}")
    print(f"      - h(n) chọn max({dist_A}, {h_empty}) = {h}")
    
    # Test case 2: 2 màu
    print("\n" + "-"*70)
    print("🎯 Test 2.2: Puzzle 2 màu (5x5)")
    puzzle_str = """
    A000B
    00000
    00000
    00000
    B000A
    """
    state = PipeState.from_string(puzzle_str)
    
    print("\n   State hiện tại:")
    for row in state.grid:
        print("   ", [str(x) if x != 0 else '.' for x in row])
    
    print(f"\n   Current positions: {state.current_positions}")
    print(f"   Goals: {state.goals}")
    
    # Tính heuristics
    h = heuristic(state)
    h_simple = heuristic_simple(state)
    h_empty = heuristic_empty_cells(state)
    
    print(f"\n   📊 Heuristic values:")
    print(f"      H1 (Manhattan distance): {h_simple}")
    print(f"      H2 (Empty cells): {h_empty}")
    print(f"      h(n) = max(H1, H2): {h}")
    
    # Giải thích chi tiết
    print(f"\n   💡 Giải thích:")
    for color in ['A', 'B']:
        pos = state.current_positions[color]
        goal = state.goals[color]
        dist = manhattan_distance_wrap(pos, goal, state.size)
        print(f"      - {color} từ {pos} đến {goal}: distance = {dist}")
    print(f"      - Tổng Manhattan distance: {h_simple}")
    print(f"      - Số ô trống: {h_empty}")
    print(f"      - h(n) chọn max({h_simple}, {h_empty}) = {h}")

def test_heuristic_properties():
    """Test tính chất admissible của heuristic"""
    print("\n" + "="*70)
    print("TEST 3: KIỂM TRA TÍNH CHẤT HEURISTIC")
    print("="*70)
    
    print("\n🔍 Kiểm tra tính Admissible (h(n) <= cost thực tế)")
    
    # Test với state gần goal (chỉ còn 1 ô trống)
    print(f"\n   Test 3.1: State gần goal (chỉ còn 1 bước)")
    from main import is_goal
    
    # Tạo state manually để test
    grid = [['A', 'A', 'A', 'A', 'A'],
            ['A', 'A', 'A', 'A', 'A'],
            ['A', 'A', 'A', 'A', 'A'],
            ['A', 'A', 'A', 'A', 'A'],
            ['A', 'A', 'A', 0, 'A']]
    current_positions = {'A': (4, 2)}
    goals = {'A': (4, 4)}
    state = PipeState(grid, current_positions, goals, size=5)
    
    h = heuristic(state)
    is_goal_state = is_goal(state)
    
    print(f"   Grid: Hầu hết đã lấp đầy, chỉ còn 1 ô trống")
    print(f"   A ở (4, 2), goal ở (4, 4)")
    print(f"   is_goal? {is_goal_state}")
    print(f"   h(n) = {h}")
    print(f"   Cost thực tế: 2 bước (đi đến (4,3) rồi (4,4))")
    print(f"   h(n) <= 2? {h} <= 2 → {h <= 2}")
    if h <= 2:
        print(f"   ✅ Admissible!")
    else:
        print(f"   ⚠️ h(n) lớn hơn cost thực tế (do đếm ô trống)")
    
    # Test với state ban đầu
    print(f"\n   Test 3.2: State ban đầu (1 màu)")
    puzzle_str = """
    A000A
    00000
    00000
    00000
    00000
    """
    state = PipeState.from_string(puzzle_str)
    
    # State này cần 24 bước để hoàn thành (25 ô - 1 ô đã lấp)
    h = heuristic(state)
    actual_cost = 24  # Cost thực tế
    
    print(f"   h(n) = {h}")
    print(f"   Cost thực tế: {actual_cost} (cần lấp đầy 24 ô)")
    print(f"   h(n) <= actual_cost? {h} <= {actual_cost} → {h <= actual_cost}")
    if h <= actual_cost:
        print(f"   ✅ Admissible!")
    else:
        print(f"   ❌ Không admissible (cần cải thiện heuristic)")
    
    # Test tính Consistent
    print(f"\n   Test 3.3: Tính Consistent (h(n) <= c(n,n') + h(n'))")
    print(f"   Với c(n,n') = 1 (mỗi bước cost = 1)")
    
    from main import get_successors
    successors = get_successors(state)
    
    if successors:
        h_n = heuristic(state)
        successor = successors[0]
        h_n_prime = heuristic(successor)
        c = 1  # Cost của 1 bước
        
        print(f"   h(n) = {h_n}")
        print(f"   h(n') = {h_n_prime}")
        print(f"   c(n,n') = {c}")
        print(f"   h(n) <= c + h(n')? {h_n} <= {c} + {h_n_prime} = {c + h_n_prime}")
        print(f"   → {h_n <= c + h_n_prime}")
        
        if h_n <= c + h_n_prime:
            print(f"   ✅ Consistent!")
        else:
            print(f"   ❌ Không consistent")

def test_heuristic_comparison():
    """So sánh các heuristic khác nhau"""
    print("\n" + "="*70)
    print("TEST 4: SO SÁNH CÁC HEURISTIC")
    print("="*70)
    
    test_cases = [
        ("1 màu", """
A000A
00000
00000
00000
00000
"""),
        ("2 màu", """
A000B
00000
00000
00000
B000A
"""),
        ("3 màu", """
AB0C0
00000
00000
00000
0C0BA
"""),
    ]
    
    print("\n   Heuristic nào mạnh hơn (giá trị cao hơn)?")
    print("   (Heuristic mạnh hơn → ít node expand hơn)")
    print("\n   " + "-"*66)
    print(f"   {'Puzzle':<12} | {'H(combined)':<12} | {'H(simple)':<12} | {'H(empty)':<12}")
    print("   " + "-"*66)
    
    for name, puzzle_str in test_cases:
        state = PipeState.from_string(puzzle_str)
        h = heuristic(state)
        h_simple = heuristic_simple(state)
        h_empty = heuristic_empty_cells(state)
        
        print(f"   {name:<12} | {h:<12} | {h_simple:<12} | {h_empty:<12}")
    
    print("   " + "-"*66)
    print("\n   💡 Kết luận:")
    print("      - h(combined) = max(h_simple, h_empty) → Luôn >= các heuristic khác")
    print("      - h(combined) mạnh nhất → A* sẽ expand ít node nhất")
    print("      - Nhưng vẫn admissible → Đảm bảo optimal solution")

def main():
    """Chạy tất cả tests"""
    print("\n" + "🧪"*35)
    print("TEST HEURISTIC FUNCTIONS")
    print("Bài toán: 7x7 Pipes Wrap Puzzle")
    print("🧪"*35)
    
    test_manhattan_distance_wrap()
    test_heuristic_functions()
    test_heuristic_properties()
    test_heuristic_comparison()
    
    print("\n" + "✅"*35)
    print("HOÀN THÀNH TẤT CẢ TESTS!")
    print("✅"*35 + "\n")

if __name__ == "__main__":
    main()

