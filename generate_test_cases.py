"""
Tool tạo 15 test cases cho demo thầy
- 5 case DỄ (4-8 open ends) - giải được <10s
- 5 case VỪA (10-16 open ends) - giải được 10-60s
- 5 case KHÓ (18-30+ open ends) - khó, có case gây tràn RAM
"""

from main import PipeState, count_open_ends
import time
import os

# Định nghĩa 15 test cases với độ khó tăng dần
TEST_CASES = {
    # ======================================================================
    # DỄ (4-8 open ends) - Giải được trong <10s  
    # ======================================================================
    
    "test01_easy_tiny": """
L-7....
|.|....
r-J....
.......
.......
.......
.......
""",
    # 1 box siêu nhỏ, 4 open ends
    
    "test02_easy_straight": """
L-7....
|.|....
|.|....
|.|....
|.|....
|.|....
r-J....
""",
    # 1 hình chữ nhật dài, 4 open ends
    
    "test03_easy_frame": """
L-----7
|.....|
|.....|
|.....|
|.....|
|.....|
r-----J
""",
    # Frame 7x7, 6 open ends
    
    "test04_easy_corner": """
L-7....
|.|....
|.r----
|......
|......
|......
r------
""",
    # L-shape lớn, 6 open ends
    
    "test05_easy_two_small": """
L-7....
|.|....
r-J....
.......
....L-7
....|.|
....r-J
""",
    # 2 boxes nhỏ riêng biệt, 8 open ends
    
    # ======================================================================
    # VỪA (10-16 open ends) - Giải được trong 10-60s
    # ======================================================================
    
    "test06_medium_nested": """
L-----7
||...||
||...||
||...||
||...||
||...||
r-----J
""",
    # Double frame, 10 open ends
    
    "test07_medium_three": """
L-7L-7.
|.||.|.
r-Jr-J.
.......
...L-7.
...|.|.
...r-J.
""",
    # 3 boxes scattered, 12 open ends
    
    "test08_medium_cross": """
.......
...L7..
...||..
L--++-7
...||..
...rJ..
.......
""",
    # 1 cross structure, 10 open ends
    
    "test09_medium_connected": """
L-7....
|.|....
|.r-7..
|...|..
r-7.|..
..|.|..
..r-J..
""",
    # Connected structures, 14 open ends
    
    "test10_medium_grid": """
L-7.L-7
|.|.|.|
r-J.r-J
.......
L-7.L-7
|.|.|.|
r-J.r-J
""",
    # 4 boxes grid, 16 open ends (boundary)
    
    # ======================================================================
    # KHÓ (18-30+ open ends) - Giải chậm hoặc tràn RAM
    # ======================================================================
    
    "test11_hard_complex": """
L-7L-7.
|.||.|.
|.||.|.
r-Jr-J.
L-7L-7.
|.||.|.
r-Jr-J.
""",
    # 4 boxes + 2 boxes, 20 open ends
    
    "test12_hard_tjunction": """
L-7.L-7
|.|.|.|
r-J.r-J
L-+.L+7
|.|.|.|
r-J.r-J
.......
""",
    # Multiple T-junctions, 22 open ends
    
    "test13_hard_dense": """
L-7L-7.
||||||.
r-Jr-J.
L-7L-7.
||||||.
r-Jr-J.
.......
""",
    # Very dense, 24 open ends
    
    "test14_veryhard_max": """
L-7L-7L
|.||.||
r-Jr-J|
L-7L-7|
|.||.||
r-Jr-J|
L-7L-7r
""",
    # Maximum density, 28-30 open ends
    # RẤT KHÓ - có thể >180s hoặc timeout
    
    "test15_extreme_ram": """
L-7L-7L
||+||+|
r-Jr-J|
L-+L-+7
||+||+|
r-Jr-J|
L-7L-7r
""",
    # EXTREME: 35+ open ends với crosses
    # GÂY TRÀN RAM - Search space khổng lồ
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
            'DỄ' if open_ends <= 8 else
            'VỪA' if open_ends <= 16 else
            'KHÓ' if open_ends <= 24 else
            'RẤT KHÓ' if open_ends <= 30 else
            'EXTREME'
        )
    }

def save_test_case(name, puzzle_str):
    """Lưu test case vào file .txt"""
    os.makedirs('test_inputs', exist_ok=True)
    filename = f'test_inputs/{name}.txt'
    with open(filename, 'w') as f:
        f.write(puzzle_str.strip())
    return filename

def generate_all_tests():
    """Tạo tất cả test cases"""
    print("\n" + "="*80)
    print("GENERATING 15 TEST CASES FOR 7x7 PIPES WRAP PUZZLE")
    print("="*80)
    
    results = []
    
    for idx, (name, puzzle_str) in enumerate(TEST_CASES.items(), 1):
        # Lưu file
        filename = save_test_case(name, puzzle_str)
        
        # Phân tích
        analysis = analyze_puzzle(name, puzzle_str)
        results.append(analysis)
        
        print(f"[{idx:2d}/15] {name:<35} | {analysis['difficulty']:<12} | {analysis['open_ends']:2d} open ends")
    
    # In summary table
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    print(f"{'#':<4} {'Test Name':<35} {'Difficulty':<12} {'Open Ends':<12} {'Est. Time':<15}")
    print("-"*80)
    
    for idx, result in enumerate(results, 1):
        # Estimate time
        difficulty = result['difficulty']
        open_ends = result['open_ends']
        
        if difficulty == 'DỄ':
            est_time = "<10s"
        elif difficulty == 'VỪA':
            est_time = "10-60s"
        elif difficulty == 'KHÓ':
            est_time = "60-180s"
        elif difficulty == 'RẤT KHÓ':
            est_time = ">180s"
        else:  # EXTREME
            est_time = ">300s / RAM OVERFLOW"
        
        print(f"{idx:<4} {result['name']:<35} {result['difficulty']:<12} {result['open_ends']:<12} {est_time:<15}")
    
    # Print category summary
    print("\n" + "="*80)
    print("CATEGORY BREAKDOWN")
    print("="*80)
    
    easy = [r for r in results if r['difficulty'] == 'DỄ']
    medium = [r for r in results if r['difficulty'] == 'VỪA']
    hard = [r for r in results if r['difficulty'] == 'KHÓ']
    very_hard = [r for r in results if r['difficulty'] == 'RẤT KHÓ']
    extreme = [r for r in results if r['difficulty'] == 'EXTREME']
    
    print(f"DỄ (4-8 open ends):          {len(easy)} cases")
    print(f"VỪA (10-16 open ends):       {len(medium)} cases")
    print(f"KHÓ (18-24 open ends):       {len(hard)} cases")
    print(f"RẤT KHÓ (26-30 open ends):   {len(very_hard)} cases")
    print(f"EXTREME (32+ open ends):     {len(extreme)} cases [RAM OVERFLOW]")
    
    print("\n" + "="*80)
    print("FILES CREATED")
    print("="*80)
    print(f"Location: ./test_inputs/")
    print(f"Total files: {len(TEST_CASES)}")
    print("\nĐỀ XUẤT SỬ DỤNG:")
    print("  - Demo an toàn: test01-test10 (DỄ + VỪA)")
    print("  - Show khả năng giải khó: test11-test13 (KHÓ)")
    print("  - Chứng minh giới hạn: test14-test15 (RẤT KHÓ + EXTREME/RAM)")
    print("="*80 + "\n")
    
    return results

def main():
    print("\n" + "="*80)
    print("7x7 PIPES WRAP PUZZLE - TEST CASE GENERATOR")
    print("="*80)
    print("\nChế độ: CHỈ TẠO FILE (không chạy test)")
    print("Tạo 15 test cases: 5 DỄ + 5 VỪA + 5 KHÓ (có RAM overflow)")
    print("")
    
    results = generate_all_tests()
    
    print("\nLƯU Ý:")
    print("  - Test 01-05: DỄ (4-8 open ends), giải <10s")
    print("  - Test 06-10: VỪA (10-16 open ends), giải 10-60s")
    print("  - Test 11-13: KHÓ (18-24 open ends), cần 60-180s")
    print("  - Test 14: RẤT KHÓ (28-30 open ends), có thể >180s")
    print("  - Test 15: EXTREME (35+ open ends), GÂY TRÀN RAM")
    print("\nĐể chạy test:")
    print("  python3 test_comparison.py")

if __name__ == "__main__":
    main()
