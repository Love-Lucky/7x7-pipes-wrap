from main import PipeState, bfs, dfs, astar, hill_climbing, is_goal
import time

def print_state(state, title=""):
    """In trạng thái lưới"""
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

def test_puzzle(puzzle_name, puzzle_str, timeout=60):
    """Test một puzzle với tất cả các thuật toán"""
    print("\n" + "🎯"*50)
    print(f"TEST: {puzzle_name}")
    print("🎯"*50)
    
    initial_state = PipeState.from_string(puzzle_str)
    print_state(initial_state, "TRẠNG THÁI BAN ĐẦU:")
    print(f"Vị trí bắt đầu: {initial_state.current_positions}")
    print(f"Vị trí đích: {initial_state.goals}")
    
    results = {}
    
    # Test A*
    print("\n" + "-"*50)
    print("🌟 CHẠY A* SEARCH...")
    print("-"*50)
    start_time = time.time()
    try:
        solution, path, stats = astar(initial_state)
        astar_time = time.time() - start_time
        
        if solution:
            print(f"✅ A* TÌM THẤY GIẢI PHÁP!")
            print(f"   Nodes explored: {stats['nodes_explored']:,}")
            print(f"   Path length: {stats['path_length']}")
            print(f"   Path cost: {stats['path_cost']}")
            print(f"   Thời gian: {astar_time:.4f}s")
            results['A*'] = {
                'found': True,
                'nodes': stats['nodes_explored'],
                'path_length': stats['path_length'],
                'time': astar_time
            }
        else:
            print(f"❌ A* KHÔNG TÌM THẤY!")
            results['A*'] = {'found': False, 'nodes': stats['nodes_explored'], 'path_length': None, 'time': astar_time}
    except Exception as e:
        print(f"❌ A* LỖI: {e}")
        results['A*'] = {'found': False, 'nodes': 0, 'path_length': None, 'time': 0}
    
    # Test Hill Climbing
    print("\n" + "-"*50)
    print("⛰️  CHẠY HILL CLIMBING...")
    print("-"*50)
    start_time = time.time()
    try:
        solution, path, stats = hill_climbing(initial_state, max_iterations=10000)
        hc_time = time.time() - start_time
        
        if solution:
            print(f"✅ HILL CLIMBING TÌM THẤY GIẢI PHÁP!")
            print(f"   Nodes explored: {stats['nodes_explored']:,}")
            print(f"   Path length: {stats['path_length']}")
            print(f"   Iterations: {stats['iterations']}")
            print(f"   Thời gian: {hc_time:.4f}s")
            results['Hill Climbing'] = {
                'found': True,
                'nodes': stats['nodes_explored'],
                'path_length': stats['path_length'],
                'time': hc_time
            }
        else:
            print(f"❌ HILL CLIMBING BỊ STUCK!")
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
        print(f"❌ HILL CLIMBING LỖI: {e}")
        results['Hill Climbing'] = {'found': False, 'nodes': 0, 'path_length': None, 'time': 0}
    
    # Test BFS (với timeout đơn giản)
    print("\n" + "-"*50)
    print("🌊 CHẠY BFS (để so sánh)...")
    print("-"*50)
    start_time = time.time()
    try:
        solution, path, stats = bfs(initial_state)
        bfs_time = time.time() - start_time
        
        if bfs_time > timeout:
            print(f"⏱️  BFS QUÁ LÂU (>{timeout}s), bỏ qua...")
            results['BFS'] = {'found': False, 'nodes': stats['nodes_explored'], 'path_length': None, 'time': bfs_time}
        elif solution:
            print(f"✅ BFS TÌM THẤY GIẢI PHÁP!")
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
            print(f"❌ BFS KHÔNG TÌM THẤY!")
            results['BFS'] = {'found': False, 'nodes': stats['nodes_explored'], 'path_length': None, 'time': bfs_time}
    except Exception as e:
        print(f"❌ BFS LỖI: {e}")
        results['BFS'] = {'found': False, 'nodes': 0, 'path_length': None, 'time': 0}
    
    # Test DFS (nhanh, để tham khảo)
    print("\n" + "-"*50)
    print("🎯 CHẠY DFS (để tham khảo)...")
    print("-"*50)
    start_time = time.time()
    try:
        solution, path, stats = dfs(initial_state, max_depth=500)
        dfs_time = time.time() - start_time
        
        if solution:
            print(f"✅ DFS TÌM THẤY GIẢI PHÁP!")
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
            print(f"❌ DFS KHÔNG TÌM THẤY!")
            results['DFS'] = {'found': False, 'nodes': stats.get('nodes_explored', 0), 'path_length': None, 'time': dfs_time}
    except Exception as e:
        print(f"❌ DFS LỖI: {e}")
        results['DFS'] = {'found': False, 'nodes': 0, 'path_length': None, 'time': 0}
    
    # In bảng so sánh
    print_comparison_table(results)
    
    # Phân tích kết quả
    print("\n📊 PHÂN TÍCH:")
    if results['A*']['found'] and results['BFS']['found']:
        speedup = results['BFS']['time'] / results['A*']['time']
        node_ratio = results['BFS']['nodes'] / results['A*']['nodes']
        print(f"   • A* nhanh hơn BFS: {speedup:.1f}x")
        print(f"   • A* duyệt ít node hơn BFS: {node_ratio:.1f}x")
        print(f"   • A* optimal? {'✅ Có' if results['A*']['path_length'] == results['BFS']['path_length'] else '❌ Không'}")
    
    if results['Hill Climbing']['found']:
        print(f"   • Hill Climbing tìm thấy solution (nhưng có thể không optimal)")
        if results['A*']['found']:
            hc_optimal = results['Hill Climbing']['path_length'] == results['A*']['path_length']
            print(f"   • Hill Climbing optimal? {'✅ Có' if hc_optimal else '❌ Không'}")
    else:
        print(f"   • Hill Climbing bị stuck (local minimum/plateau)")
    
    return results

def main():
    """Chạy test so sánh các thuật toán"""
    print("\n" + "🔬"*50)
    print("SO SÁNH THUẬT TOÁN: A* vs Hill Climbing vs BFS vs DFS")
    print("Bài toán: 7x7 Pipes Wrap Puzzle")
    print("🔬"*50)
    
    # Test Case 1: Đơn giản
    test_puzzle(
        "TEST 1: ĐỠN GIẢN (1 màu, 5x5)",
        """
        A000A
        00000
        00000
        00000
        00000
        """
    )
    
    # Test Case 2: Vừa phải
    test_puzzle(
        "TEST 2: VỪA PHẢI (2 màu, 5x5)",
        """
        A000B
        00000
        00000
        00000
        B000A
        """
    )
    
    # Test Case 3: Khó hơn
    test_puzzle(
        "TEST 3: KHÓ HƠN (3 màu, 5x5)",
        """
        AB0C0
        00000
        00000
        00000
        0C0BA
        """
    )
    
    print("\n" + "✅"*50)
    print("HOÀN THÀNH TẤT CẢ TEST CASES!")
    print("✅"*50)
    
    print("\n💡 KẾT LUẬN:")
    print("   • A*: Optimal, nhanh hơn BFS nhờ heuristic")
    print("   • Hill Climbing: Rất nhanh nhưng có thể stuck, không optimal")
    print("   • BFS: Optimal nhưng chậm, duyệt nhiều node")
    print("   • DFS: Nhanh nhưng không optimal")

if __name__ == "__main__":
    main()

