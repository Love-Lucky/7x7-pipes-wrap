from main import PipeState, bfs, dfs, astar, hill_climbing, is_goal, count_open_ends, Tile, TileType
import time
import sys
import threading

# Output file for COMPARISON_RESULTS.md
OUTPUT_FILE = "COMPARISON_RESULTS.md"

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

def print_comparison_table(results):
    """In bảng so sánh các thuật toán"""
    print("\n" + "="*100)
    print("BẢNG SO SÁNH CÁC THUẬT TOÁN")
    print("="*100)
    print(f"{'Thuật toán':<15} | {'Tìm thấy?':<10} | {'Nodes':<12} | {'Path':<6} | {'Thời gian (s)':<14} | {'Tốc độ':<10}")
    print("-"*100)
    
    # Tìm thời gian nhanh nhất làm baseline
    min_time = min([r['time'] for r in results.values() if r['time'] > 0], default=1)
    
    for algo_name, result in results.items():
        found = "✅ Có" if result['found'] else "❌ Không"
        nodes = f"{result['nodes']:,}" if result['nodes'] else "N/A"
        path = str(result['path_length']) if result['path_length'] else "N/A"
        time_str = f"{result['time']:.4f}"
        
        if result['time'] > 0:
            speedup = result['time'] / min_time
            speed_str = f"{speedup:.1f}x"
        else:
            speed_str = "N/A"
        
        print(f"{algo_name:<15} | {found:<10} | {nodes:<12} | {path:<6} | {time_str:<14} | {speed_str:<10}")
    
    print("="*100)

def generate_random_puzzle(size: int, density: float = 0.7):
    """
    Tạo puzzle ngẫu nhiên.
    
    Args:
        size: Kích thước lưới
        density: Tỷ lệ ô có ống (0.0-1.0)
    
    Returns:
        PipeState ngẫu nhiên
    """
    import random
    
    grid = []
    for r in range(size):
        row = []
        for c in range(size):
            if random.random() < density:
                # Chọn ngẫu nhiên loại tile
                tile_type = random.choice([
                    TileType.STRAIGHT,
                    TileType.CORNER,
                    TileType.T_JUNCTION,
                ])
                rotation = random.randint(0, 3)
                row.append(Tile(tile_type, rotation))
            else:
                row.append(Tile(TileType.EMPTY, 0))
        grid.append(row)
    
    return PipeState(grid, size)

def run_with_timeout(func, timeout_sec, default_result):
    """Chạy func() trong thread, trả về (result, timed_out). Nếu timeout trả default_result."""
    result_holder = {}
    def run():
        try:
            result_holder['value'] = func()
        except Exception as e:
            result_holder['error'] = e
    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(timeout=timeout_sec)
    if t.is_alive():
        return default_result, True
    if 'error' in result_holder:
        raise result_holder['error']
    return result_holder.get('value'), False

def test_puzzle(puzzle_name, initial_state, timeout=60, bfs_dfs_timeout=12):
    """Test một puzzle với tất cả các thuật toán"""
    print("\n" + "="*50)
    print(f"TEST: {puzzle_name}")
    print("="*50)
    
    print_state(initial_state, "TRẠNG THÁI BAN ĐẦU:")
    
    results = {}
    
    # Test A*
    print("\n" + "-"*50)
    print("CHẠY A* SEARCH...")
    print("-"*50)
    start_time = time.time()
    try:
        solution, path, stats = astar(initial_state)
        astar_time = time.time() - start_time
        
        if solution:
            print(f"[OK] A* TÌM THẤY GIẢI PHÁP!")
            print(f"   Nodes explored: {stats['nodes_explored']:,}")
            print(f"   Path length: {stats['path_length']}")
            print(f"   Path cost: {stats['path_cost']}")
            print(f"   Thời gian: {astar_time:.4f}s")
            print_state(solution, "SOLUTION:")
            results['A*'] = {
                'found': True,
                'nodes': stats['nodes_explored'],
                'path_length': stats['path_length'],
                'time': astar_time
            }
        else:
            print(f"[FAIL] A* KHÔNG TÌM THẤY!")
            results['A*'] = {'found': False, 'nodes': stats['nodes_explored'], 'path_length': None, 'time': astar_time}
    except Exception as e:
        print(f"[ERROR] A* LỖI: {e}")
        results['A*'] = {'found': False, 'nodes': 0, 'path_length': None, 'time': 0}
    
    # Test Hill Climbing
    print("\n" + "-"*50)
    print("CHẠY HILL CLIMBING...")
    print("-"*50)
    start_time = time.time()
    try:
        solution, path, stats = hill_climbing(initial_state, max_iterations=10000)
        hc_time = time.time() - start_time
        
        if solution:
            print(f"[OK] HILL CLIMBING TÌM THẤY GIẢI PHÁP!")
            print(f"   Nodes explored: {stats['nodes_explored']:,}")
            print(f"   Path length: {stats['path_length']}")
            print(f"   Iterations: {stats['iterations']}")
            print(f"   Thời gian: {hc_time:.4f}s")
            print_state(solution, "SOLUTION:")
            results['Hill Climbing'] = {
                'found': True,
                'nodes': stats['nodes_explored'],
                'path_length': stats['path_length'],
                'time': hc_time
            }
        else:
            print(f"[FAIL] HILL CLIMBING BỊ STUCK!")
            if 'stuck' in stats:
                print(f"   Lý do: {stats.get('reason', 'Unknown')}")
            print(f"   Nodes explored: {stats['nodes_explored']:,}")
            print(f"   Iterations: {stats['iterations']}")
            print(f"   Thời gian: {hc_time:.4f}s")
            results['Hill Climbing'] = {
                'found': False,
                'nodes': stats['nodes_explored'],
                'path_length': len(path),
                'time': hc_time
            }
    except Exception as e:
        print(f"[ERROR] HILL CLIMBING LỖI: {e}")
        results['Hill Climbing'] = {'found': False, 'nodes': 0, 'path_length': None, 'time': 0}
    
    # Test BFS (với timeout)
    print("\n" + "-"*50)
    print("CHẠY BFS...")
    print("-"*50)
    start_time = time.time()
    try:
        bfs_result, timed_out = run_with_timeout(
            lambda: bfs(initial_state),
            timeout_sec=bfs_dfs_timeout,
            default_result=(None, None, {'nodes_explored': 0, 'path_length': None})
        )
        if timed_out:
            print(f"[TIMEOUT] BFS quá {bfs_dfs_timeout}s, bỏ qua...")
            results['BFS'] = {'found': False, 'nodes': 0, 'path_length': None, 'time': float(bfs_dfs_timeout)}
        else:
            solution, path, stats = bfs_result
            bfs_time = time.time() - start_time
            if solution:
                print(f"[OK] BFS TÌM THẤY GIẢI PHÁP!")
                print(f"   Nodes explored: {stats['nodes_explored']:,}")
                print(f"   Path length: {stats['path_length']}")
                print(f"   Thời gian: {bfs_time:.4f}s")
                results['BFS'] = {
                    'found': True,
                    'nodes': stats['nodes_explored'],
                    'path_length': stats['path_length'],
                    'time': bfs_time
                }
            else:
                print(f"[FAIL] BFS KHÔNG TÌM THẤY!")
                results['BFS'] = {'found': False, 'nodes': stats.get('nodes_explored', 0), 'path_length': None, 'time': bfs_time}
    except Exception as e:
        print(f"[ERROR] BFS LỖI: {e}")
        results['BFS'] = {'found': False, 'nodes': 0, 'path_length': None, 'time': 0}
    
    # Test DFS (với timeout)
    print("\n" + "-"*50)
    print("CHẠY DFS...")
    print("-"*50)
    start_time = time.time()
    try:
        dfs_result, timed_out = run_with_timeout(
            lambda: dfs(initial_state, max_depth=100),
            timeout_sec=bfs_dfs_timeout,
            default_result=(None, None, {'nodes_explored': 0, 'path_length': None})
        )
        if timed_out:
            print(f"[TIMEOUT] DFS quá {bfs_dfs_timeout}s, bỏ qua...")
            results['DFS'] = {'found': False, 'nodes': 0, 'path_length': None, 'time': float(bfs_dfs_timeout)}
        else:
            solution, path, stats = dfs_result
            dfs_time = time.time() - start_time
            if solution:
                print(f"[OK] DFS TÌM THẤY GIẢI PHÁP!")
                print(f"   Nodes explored: {stats['nodes_explored']:,}")
                print(f"   Path length: {stats['path_length']}")
                print(f"   Thời gian: {dfs_time:.4f}s")
                results['DFS'] = {
                    'found': True,
                    'nodes': stats['nodes_explored'],
                    'path_length': stats['path_length'],
                    'time': dfs_time
                }
            else:
                print(f"[FAIL] DFS KHÔNG TÌM THẤY!")
                results['DFS'] = {'found': False, 'nodes': stats.get('nodes_explored', 0), 'path_length': None, 'time': dfs_time}
    except Exception as e:
        print(f"[ERROR] DFS LỖI: {e}")
        results['DFS'] = {'found': False, 'nodes': 0, 'path_length': None, 'time': 0}
    
    # In bảng so sánh
    print_comparison_table(results)
    
    # Phân tích
    print("\nPHÂN TÍCH:")
    if results['A*']['found'] and results['BFS']['found']:
        if results['BFS']['time'] > 0 and results['A*']['time'] > 0:
            speedup = results['BFS']['time'] / results['A*']['time']
            node_ratio = results['BFS']['nodes'] / results['A*']['nodes']
            print(f"   • A* vs BFS: Tốc độ {speedup:.1f}x, Nodes {node_ratio:.1f}x")
            print(f"   • A* optimal? {'Có' if results['A*']['path_length'] == results['BFS']['path_length'] else 'Không'}")
    
    if results['Hill Climbing']['found']:
        print(f"   • Hill Climbing tìm thấy solution")
        if results['A*']['found']:
            hc_optimal = results['Hill Climbing']['path_length'] == results['A*']['path_length']
            print(f"   • Hill Climbing optimal? {'Có' if hc_optimal else 'Không'}")
    else:
        print(f"   • Hill Climbing bị stuck (local minimum)")
    
    return results

class TeeOutput:
    """Ghi đồng thời ra stdout và vào buffer để sau ghi file."""
    def __init__(self):
        self._stdout = sys.stdout
        self._buffer = []
    def write(self, s):
        self._stdout.write(s)
        self._buffer.append(s)
    def flush(self):
        self._stdout.flush()
    def getvalue(self):
        return "".join(self._buffer)

def main():
    """Chạy test so sánh các thuật toán"""
    tee = TeeOutput()
    sys.stdout = tee
    try:
        _main_impl()
    finally:
        sys.stdout = sys.__stdout__
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(tee.getvalue())
    print(f"\n[Đã ghi kết quả vào {OUTPUT_FILE}]")

def _main_impl():
    """Phần chính của main (in ra tee)."""
    print("\n" + "="*50)
    print("SO SÁNH THUẬT TOÁN: A* vs Hill Climbing vs BFS vs DFS")
    print("Bài toán: 7x7 Pipes Wrap Puzzle (Rotation Version)")
    print("="*50)
    
    # Test Case 1: Puzzle đơn giản đã sắp xếp
    print("\nTest với puzzle có sẵn...")
    puzzle1 = PipeState.from_string("""
        L-7
        |.|
        r-J
    """)
    test_puzzle("TEST 1: SIMPLE 3x3", puzzle1)
    
    # Test Case 2: Puzzle phức tạp hơn
    puzzle2 = PipeState.from_string("""
        L--7
        |..|
        |..|
        r--J
    """)
    test_puzzle("TEST 2: MEDIUM 4x4", puzzle2)
    
    # Test Case 3: Random puzzle (bỏ qua để chạy nhanh; BFS/DFS có thể rất lâu)
    # print("\nTạo puzzle ngẫu nhiên 5x5...")
    # random_puzzle = generate_random_puzzle(5, density=0.8)
    # test_puzzle("TEST 3: RANDOM 5x5", random_puzzle)
    
    print("\n" + "="*50)
    print("HOÀN THÀNH TẤT CẢ TEST CASES!")
    print("="*50)
    
    print("\nKẾT LUẬN:")
    print("   • A*: Optimal, hiệu quả với heuristic (count open ends)")
    print("   • Hill Climbing: Nhanh nhưng có thể stuck")
    print("   • BFS: Optimal nhưng chậm, tốn bộ nhớ")
    print("   • DFS: Nhanh nhưng không đảm bảo optimal")

if __name__ == "__main__":
    main()
