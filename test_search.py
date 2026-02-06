from main import PipeState, bfs, dfs, is_goal
import time

def print_state(state, title=""):
    """In trạng thái lưới một cách đẹp mắt"""
    if title:
        print(f"\n{title}")
    print("-" * (state.size * 2 + 1))
    for r in range(state.size):
        row_str = "|"
        for c in range(state.size):
            val = state.grid[r][c]
            char = str(val if val != 0 else ' ')
            row_str += char + "|"
        print(row_str)
    print("-" * (state.size * 2 + 1))

def print_stats(algorithm_name, stats, time_elapsed):
    """In thống kê thuật toán"""
    print(f"\n{'='*60}")
    print(f"THỐNG KÊ THUẬT TOÁN: {algorithm_name}")
    print(f"{'='*60}")
    print(f"Số node đã duyệt:        {stats['nodes_explored']:,}")
    print(f"Số trạng thái đã thăm:   {stats['visited_states']:,}")
    print(f"Kích thước frontier max: {stats['max_frontier_size']:,}")
    if 'path_length' in stats:
        print(f"Độ dài đường đi:         {stats['path_length']}")
    if 'max_depth_reached' in stats:
        print(f"Độ sâu tối đa đạt được:  {stats['max_depth_reached']}")
    print(f"Thời gian thực thi:      {time_elapsed:.4f} giây")
    print(f"{'='*60}\n")

def test_simple_case():
    """Test case đơn giản: 1 màu trên lưới 5x5"""
    print("\n" + "="*60)
    print("TEST CASE 1: ĐƠN GIẢN (1 màu, lưới 5x5)")
    print("="*60)
    
    puzzle_str = """
    A000A
    00000
    00000
    00000
    00000
    """
    
    initial_state = PipeState.from_string(puzzle_str)
    print_state(initial_state, "TRẠNG THÁI BAN ĐẦU:")
    print(f"Vị trí bắt đầu: {initial_state.current_positions}")
    print(f"Vị trí đích: {initial_state.goals}")
    
    # Test BFS
    print("\n" + "-"*60)
    print("CHẠY THUẬT TOÁN BFS...")
    print("-"*60)
    start_time = time.time()
    solution, path, stats = bfs(initial_state)
    bfs_time = time.time() - start_time
    
    if solution:
        print("\n✅ BFS TÌM THẤY GIẢI PHÁP!")
        print_state(solution, "TRẠNG THÁI ĐÍCH:")
        print_stats("BFS (Breadth-First Search)", stats, bfs_time)
    else:
        print("\n❌ BFS KHÔNG TÌM THẤY GIẢI PHÁP!")
        print_stats("BFS (Breadth-First Search)", stats, bfs_time)
    
    # Test DFS
    print("\n" + "-"*60)
    print("CHẠY THUẬT TOÁN DFS...")
    print("-"*60)
    start_time = time.time()
    solution, path, stats = dfs(initial_state)
    dfs_time = time.time() - start_time
    
    if solution:
        print("\n✅ DFS TÌM THẤY GIẢI PHÁP!")
        print_state(solution, "TRẠNG THÁI ĐÍCH:")
        print_stats("DFS (Depth-First Search)", stats, dfs_time)
    else:
        print("\n❌ DFS KHÔNG TÌM THẤY GIẢI PHÁP!")
        print_stats("DFS (Depth-First Search)", stats, dfs_time)

def test_two_colors():
    """Test case: 2 màu trên lưới 5x5"""
    print("\n" + "="*60)
    print("TEST CASE 2: VỪA PHẢI (2 màu, lưới 5x5)")
    print("="*60)
    
    puzzle_str = """
    A000B
    00000
    00000
    00000
    B000A
    """
    
    initial_state = PipeState.from_string(puzzle_str)
    print_state(initial_state, "TRẠNG THÁI BAN ĐẦU:")
    print(f"Vị trí bắt đầu: {initial_state.current_positions}")
    print(f"Vị trí đích: {initial_state.goals}")
    
    # Test BFS
    print("\n" + "-"*60)
    print("CHẠY THUẬT TOÁN BFS...")
    print("-"*60)
    start_time = time.time()
    solution, path, stats = bfs(initial_state)
    bfs_time = time.time() - start_time
    
    if solution:
        print("\n✅ BFS TÌM THẤY GIẢI PHÁP!")
        print_state(solution, "TRẠNG THÁI ĐÍCH:")
        print_stats("BFS (Breadth-First Search)", stats, bfs_time)
    else:
        print("\n❌ BFS KHÔNG TÌM THẤY GIẢI PHÁP!")
        print_stats("BFS (Breadth-First Search)", stats, bfs_time)
    
    # Test DFS
    print("\n" + "-"*60)
    print("CHẠY THUẬT TOÁN DFS...")
    print("-"*60)
    start_time = time.time()
    solution, path, stats = dfs(initial_state, max_depth=500)
    dfs_time = time.time() - start_time
    
    if solution:
        print("\n✅ DFS TÌM THẤY GIẢI PHÁP!")
        print_state(solution, "TRẠNG THÁI ĐÍCH:")
        print_stats("DFS (Depth-First Search)", stats, dfs_time)
    else:
        print("\n❌ DFS KHÔNG TÌM THẤY GIẢI PHÁP!")
        print_stats("DFS (Depth-First Search)", stats, dfs_time)

def test_three_colors():
    """Test case: 3 màu trên lưới 5x5"""
    print("\n" + "="*60)
    print("TEST CASE 3: KHÓ HƠN (3 màu, lưới 5x5)")
    print("="*60)
    
    puzzle_str = """
    AB0C0
    00000
    00000
    00000
    0C0BA
    """
    
    initial_state = PipeState.from_string(puzzle_str)
    print_state(initial_state, "TRẠNG THÁI BAN ĐẦU:")
    print(f"Vị trí bắt đầu: {initial_state.current_positions}")
    print(f"Vị trí đích: {initial_state.goals}")
    
    # Test BFS
    print("\n" + "-"*60)
    print("CHẠY THUẬT TOÁN BFS...")
    print("-"*60)
    start_time = time.time()
    solution, path, stats = bfs(initial_state)
    bfs_time = time.time() - start_time
    
    if solution:
        print("\n✅ BFS TÌM THẤY GIẢI PHÁP!")
        print_state(solution, "TRẠNG THÁI ĐÍCH:")
        print_stats("BFS (Breadth-First Search)", stats, bfs_time)
        
        # Hiển thị một vài bước trong đường đi
        print("\nMỘT SỐ BƯỚC TRONG ĐƯỜNG ĐI:")
        step_indices = [0, len(path)//4, len(path)//2, 3*len(path)//4, len(path)-1]
        for i in step_indices:
            print_state(path[i], f"Bước {i+1}/{len(path)}:")
    else:
        print("\n❌ BFS KHÔNG TÌM THẤY GIẢI PHÁP!")
        print_stats("BFS (Breadth-First Search)", stats, bfs_time)

def main():
    """Chạy tất cả test cases"""
    print("\n" + "🔍"*30)
    print("DEMO THUẬT TOÁN TÌM KIẾM MÙ - BFS & DFS")
    print("Bài toán: 7x7 Pipes Wrap Puzzle")
    print("🔍"*30)
    
    # Chạy các test case
    test_simple_case()
    test_two_colors()
    test_three_colors()
    
    print("\n" + "✅"*30)
    print("HOÀN THÀNH TẤT CẢ TEST CASES!")
    print("✅"*30 + "\n")

if __name__ == "__main__":
    main()

