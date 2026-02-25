"""
Test đơn giản với puzzle nhỏ để demo nhanh
"""

from main import PipeState, astar, bfs, hill_climbing, Tile, TileType, count_open_ends
import time

def print_state(state, title=""):
    """In trạng thái lưới"""
    if title:
        print(f"\n{title}")
    print("-" * (state.size * 2 + 1))
    for r in range(state.size):
        row_str = "|"
        for c in range(state.size):
            tile = state.get_tile(r, c)
            char = tile.to_char()
            row_str += char + "|"
        print(row_str)
    print("-" * (state.size * 2 + 1))
    print(f"Open ends: {count_open_ends(state)}")

def test_trivial():
    """Test puzzle CỰC đơn giản: chỉ 1 tile cần xoay"""
    print("=" * 60)
    print("TEST: PUZZLE TRIVIAL (1 BƯỚC)")
    print("=" * 60)
    
    # Puzzle: 2 ống cần xoay để nối
    puzzle_str = """
    ||
    """
    
    state = PipeState.from_string(puzzle_str)
    print_state(state, "TRẠNG THÁI BAN ĐẦU:")
    
    print("\nChạy A* Search...")
    start = time.time()
    solution, path, stats = astar(state)
    elapsed = time.time() - start
    
    if solution:
        print(f"[OK] TÌM THẤY SOLUTION!")
        print(f"   Thời gian: {elapsed:.4f}s")
        print(f"   Nodes explored: {stats['nodes_explored']}")
        print(f"   Path length: {stats.get('path_length', len(path) if path else 1)}")
        print_state(solution, "SOLUTION:")
    else:
        print("[FAIL] Không tìm thấy solution")

def test_easy():
    """Test puzzle dễ: 2x2"""
    print("\n" + "=" * 60)
    print("TEST: PUZZLE DỄ (2x2)")
    print("=" * 60)
    
    # Puzzle 2x2 đơn giản
    puzzle_str = """
    L7
    rJ
    """
    
    state = PipeState.from_string(puzzle_str)
    print_state(state, "TRẠNG THÁI BAN ĐẦU:")
    
    print("\nChạy A* Search...")
    start = time.time()
    solution, path, stats = astar(state)
    elapsed = time.time() - start
    
    if solution:
        print(f"[OK] TÌM THẤY SOLUTION!")
        print(f"   Thời gian: {elapsed:.4f}s")
        print(f"   Nodes explored: {stats['nodes_explored']}")
        print(f"   Path length: {stats.get('path_length', len(path))}")
        print_state(solution, "SOLUTION:")
        
        # In từng bước
        print("\nCÁC BƯỚC:")
        for i, state in enumerate(path):
            print(f"\nBước {i}:")
            print_state(state, "")
    else:
        print("[FAIL] Không tìm thấy solution")

def test_medium():
    """Test puzzle vừa: 3x3"""
    print("\n" + "=" * 60)
    print("TEST: PUZZLE VỪA (3x3)")
    print("=" * 60)
    
    puzzle_str = """
    L-7
    |.|
    r-J
    """
    
    state = PipeState.from_string(puzzle_str)
    print_state(state, "TRẠNG THÁI BAN ĐẦU:")
    
    # Test Hill Climbing (nhanh hơn)
    print("\nChạy Hill Climbing (nhanh hơn)...")
    start = time.time()
    solution, path, stats = hill_climbing(state, max_iterations=1000)
    elapsed = time.time() - start
    
    if solution:
        print(f"[OK] TÌM THẤY SOLUTION!")
        print(f"   Thời gian: {elapsed:.4f}s")
        print(f"   Nodes explored: {stats['nodes_explored']}")
        print(f"   Iterations: {stats['iterations']}")
        print_state(solution, "SOLUTION:")
    else:
        print("[FAIL] Hill Climbing bị stuck")
        print(f"   Lý do: {stats.get('reason', 'Unknown')}")
        print(f"   Thời gian: {elapsed:.4f}s")
    
    # Test A* (chậm hơn nhưng optimal)
    print("\nChạy A* Search (có thể lâu)...")
    start = time.time()
    solution, path, stats = astar(state)
    elapsed = time.time() - start
    
    if solution:
        print(f"[OK] TÌM THẤY SOLUTION!")
        print(f"   Thời gian: {elapsed:.4f}s")
        print(f"   Nodes explored: {stats['nodes_explored']}")
        print(f"   Path length: {stats.get('path_length', len(path))}")
        print_state(solution, "SOLUTION:")
    else:
        print("[FAIL] Không tìm thấy solution")

def main():
    print("\nTEST PIPE ROTATION PUZZLE - PHIÊN BẢN ĐƠN GIẢN")
    print("Mục tiêu: Xoay các ống để không còn đầu hở\n")
    
    test_trivial()
    test_easy()
    test_medium()
    
    print("\n" + "=" * 60)
    print("HOÀN THÀNH!")
    print("=" * 60)
    print("\nLƯU Ý:")
    print("   • Puzzle càng lớn → search càng lâu")
    print("   • 3x3 đã có thể mất vài phút với A*")
    print("   • 7x7 rất khó, cần thuật toán tối ưu hơn")
    print("   • Hill Climbing nhanh nhưng có thể stuck")

if __name__ == "__main__":
    main()
