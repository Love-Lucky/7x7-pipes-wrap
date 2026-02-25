"""
Tool tạo 10-15 test cases cho demo thầy
"""

from main import PipeState, count_open_ends
from main_optimized import astar_optimized
import time
import os

# Định nghĩa test cases với độ khó tăng dần
TEST_CASES = {
    # ==== DỄ (6-8 open ends) ====
    "test01_easy_frame": """
L-----7
|.....|
|.....|
|.....|
|.....|
|.....|
r-----J
""",
    
    "test02_easy_cross": """
...L7..
...||..
L--++-7
|||.|||
r--++-J
...||..
...rJ..
""",
    
    "test03_easy_double": """
L-7.L-7
|.|.|.|
r-J.r-J
.......
.......
.......
.......
""",
    
    # ==== VỪA (10-14 open ends) ====
    "test04_medium_grid": """
L-7...L
|.|...|
r-J...|
......|
L-7...|
|.|...|
r-J...r
""",
    
    "test05_medium_nested": """
L-----7
|.L-7.|
|.|||.|
|.+-+.|
|.|||.|
|.r-J.|
r-----J
""",
    
    "test06_medium_symmetric": """
L--7.L-7
|..|.|.|
r--J.r-J
.......
L--7.L-7
|..|.|.|
r--J.r-J
""",
    
    "test07_medium_diagonal": """
L-7....
|.|....
r-J.L-7
....|.|
....r-J
.......
.......
""",
    
    # ==== KHÓ (16-20 open ends) ====
    "test08_hard_multi": """
L-7.L-7
|.|.|.|
r-J.r-J
L-7.L-7
|.|.|.|
r-J.r-J
.......
""",
    
    "test09_hard_complex": """
L--7.L7
|..|.||
r--J.||
L-7..||
|.|..||
r-J.r-J
.......
""",
    
    # ==== RẤT KHÓ (>20 open ends - có thể fail) ====
    "test10_veryhard_dense": """
L--7.L7
|..|.||
r-7r-J|
..||..|
L-Jr-7|
|....|.|
r----Jr
""",
    
    # ==== EDGE CASES ====
    "test11_already_solved": """
L-----7
|.....|
|.....|
|.....|
|.....|
|.....|
r-----J
""",  # Giống test01 nhưng đã xoay đúng
    
    "test12_unsolvable": """
L7.....
||.....
rJ.....
.......
.......
.......
.......
""",  # Ống không thể nối (nhỏ, isolated)
}

def analyze_puzzle(name, puzzle_str):
    """Phân tích puzzle trước khi test"""
    state = PipeState.from_string(puzzle_str)
    open_ends = count_open_ends(state)
    
    # Đếm tiles
    non_empty = 0
    for r in range(state.size):
        for c in range(state.size):
            if state.get_tile(r, c).type.value > 0:  # Not EMPTY
                non_empty += 1
    
    return {
        'name': name,
        'open_ends': open_ends,
        'non_empty_tiles': non_empty,
        'difficulty': (
            'EASY' if open_ends <= 8 else
            'MEDIUM' if open_ends <= 14 else
            'HARD' if open_ends <= 20 else
            'VERY_HARD'
        )
    }

def test_puzzle(name, puzzle_str, timeout=120):
    """Test puzzle với timeout"""
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print("="*70)
    
    state = PipeState.from_string(puzzle_str)
    
    # Phân tích
    analysis = analyze_puzzle(name, puzzle_str)
    print(f"Difficulty: {analysis['difficulty']}")
    print(f"Open ends: {analysis['open_ends']}")
    print(f"Non-empty tiles: {analysis['non_empty_tiles']}")
    
    # Test với timeout
    print(f"\nRunning A*... (timeout: {timeout}s)")
    start = time.time()
    
    try:
        solution, path, stats = astar_optimized(state)
        elapsed = time.time() - start
        
        if solution:
            print(f"\n[OK] SOLVED in {elapsed:.2f}s")
            print(f"   Nodes explored: {stats['nodes_explored']:,}")
            print(f"   Path length: {stats['path_length']}")
            
            result = {
                **analysis,
                'solved': True,
                'time': elapsed,
                'nodes': stats['nodes_explored'],
                'path_length': stats['path_length']
            }
        else:
            print(f"\n[FAIL] NOT SOLVED in {elapsed:.2f}s")
            print(f"   Nodes explored: {stats['nodes_explored']:,}")
            
            result = {
                **analysis,
                'solved': False,
                'time': elapsed,
                'nodes': stats['nodes_explored'],
                'path_length': 0
            }
    
    except KeyboardInterrupt:
        print(f"\n[TIMEOUT] Stopped manually")
        result = {
            **analysis,
            'solved': False,
            'time': timeout,
            'nodes': 0,
            'path_length': 0
        }
    
    return result

def save_test_case(name, puzzle_str):
    """Lưu test case vào file .txt"""
    os.makedirs('test_inputs', exist_ok=True)
    filename = f'test_inputs/{name}.txt'
    with open(filename, 'w') as f:
        f.write(puzzle_str.strip())
    print(f"Saved: {filename}")

def generate_all_tests(run_tests=False):
    """Tạo tất cả test cases"""
    print("\n" + "="*70)
    print("GENERATING TEST CASES")
    print("="*70)
    
    results = []
    
    for name, puzzle_str in TEST_CASES.items():
        # Lưu file
        save_test_case(name, puzzle_str)
        
        # Phân tích
        analysis = analyze_puzzle(name, puzzle_str)
        
        # Test nếu được yêu cầu
        if run_tests:
            # Chỉ test case dễ và vừa (để tiết kiệm thời gian)
            if analysis['difficulty'] in ['EASY', 'MEDIUM']:
                result = test_puzzle(name, puzzle_str, timeout=120)
                results.append(result)
            else:
                print(f"\n[SKIP] {name} - {analysis['difficulty']} (quá khó)")
                results.append({
                    **analysis,
                    'solved': None,
                    'time': 0,
                    'nodes': 0,
                    'path_length': 0
                })
        else:
            results.append(analysis)
    
    # In summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"{'Test Name':<30} {'Difficulty':<12} {'Open Ends':<12} {'Time (s)':<10}")
    print("-"*70)
    
    for result in results:
        time_str = f"{result['time']:.2f}" if 'time' in result and result['time'] > 0 else "N/A"
        solved_mark = "[OK]" if result.get('solved') else ("[FAIL]" if result.get('solved') == False else "[---]")
        print(f"{result['name']:<30} {result['difficulty']:<12} {result['open_ends']:<12} {time_str:<10} {solved_mark}")
    
    print("\n" + "="*70)
    print("Đã tạo xong test cases!")
    print(f"Tổng số: {len(TEST_CASES)} files")
    print("Location: ./test_inputs/")
    print("="*70)
    
    return results

def main():
    import sys
    
    print("\nTOOL TẠO TEST CASES CHO 7x7 PIPES WRAP PUZZLE")
    print("="*70)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        print("\nChế độ: TẠO + TEST (chậm, ~5-10 phút)")
        print("Sẽ test các case DỄ và VỪA")
        input("Press Enter to continue...")
        results = generate_all_tests(run_tests=True)
    else:
        print("\nChế độ: CHỈ TẠO FILE (nhanh)")
        print("Để test, chạy: python3 generate_test_cases.py --test")
        results = generate_all_tests(run_tests=False)
    
    print("\nĐỀ XUẤT:")
    print("- Dùng test01-test03 (EASY) cho demo an toàn")
    print("- Dùng test04-test07 (MEDIUM) để show khó hơn")
    print("- Dùng test08-test10 (HARD/VERY_HARD) nếu thầy hỏi")
    print("- Dùng test11-test12 (EDGE CASES) cho đầy đủ")

if __name__ == "__main__":
    main()
