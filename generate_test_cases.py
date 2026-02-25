"""
Tool tạo 15 test cases cho demo thầy
- 5 case DỄ (4-8 open ends) - giải được <10s
- 5 case VỪA (10-14 open ends) - giải được 10-60s
- 3 case KHÓ (16-20 open ends) - giải được 60-180s
- 2 case EXTREME (26+ open ends với CROSS) - không giải được
"""

from main import PipeState, count_open_ends
import time
import os

# Định nghĩa 15 test cases - Puzzles đơn giản hơn
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
    
    "test02_easy_tall": """
L-7....
|.|....
|.|....
|.|....
|.|....
|.|....
r-J....
""",
    # 1 box cao, 4 open ends
    
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
    
    "test04_easy_two": """
L-7....
|.|....
r-J....
.......
....L-7
....|.|
....r-J
""",
    # 2 boxes riêng biệt, 8 open ends
    
    "test05_easy_nested": """
L-----7
||...||
||...||
||...||
||...||
||...||
r-----J
""",
    # Double frame, 6 open ends (có thể 10 nếu xoay sai)
    
    # ======================================================================
    # VỪA (10-14 open ends) - Giải được trong 10-60s
    # ======================================================================
    
    "test06_medium_three": """
L-7....
|.|....
r-J.L-7
....|.|
....r-J
.......
.......
""",
    # 3 boxes xa nhau, ~12 open ends
    
    "test07_medium_l_shape": """
L-7....
|.|....
|.r-7..
|...|..
|...|..
|...|..
r---J..
""",
    # L-shape lớn, ~10-12 open ends
    
    "test08_medium_connected": """
L-7....
|.|....
|.r-7..
|...|..
r---J..
.......
.......
""",
    # Connected boxes, ~10 open ends
    
    "test09_medium_four_small": """
L-7.L-7
|.|.|.|
r-J.r-J
.......
L-7.L-7
|.|.|.|
r-J.r-J
""",
    # 4 boxes nhỏ, ~16 open ends (biên giới VỪA/KHÓ)
    
    "test10_medium_nested": """
L-----7
||L-7||
|||.|||
||r-J||
||...||
||...||
r-----J
""",
    # Triple nested, ~14 open ends
    
    # ======================================================================
    # KHÓ (16-20 open ends) - Giải được trong 60-180s
    # ======================================================================
    
    "test11_hard_five": """
L-7L-7.
|.||.|.
r-Jr-J.
.......
...L-7.
...|.|.
...r-J.
""",
    # 5 boxes, ~16-18 open ends
    
    "test12_hard_six": """
L-7L-7.
|.||.|.
r-Jr-J.
L-7L-7.
|.||.|.
r-Jr-J.
.......
""",
    # 6 boxes, ~18-20 open ends
    
    "test13_hard_dense": """
L-7L-7L
|.||.||
r-Jr-J|
.......
L-7L-7.
|.||.|.
r-Jr-J.
""",
    # 8 boxes, ~20-22 open ends
    
    # ======================================================================
    # EXTREME (26+ open ends với CROSS) - KHÔNG GIẢI ĐƯỢC
    # ======================================================================
    
    "test14_extreme_cross": """
L-7.L-7
||+.||+
r-Jr-J|
L-+.L+7
||+.||+
r-Jr-J|
.......
""",
    # Multiple CROSS, ~30+ open ends
    # CROSS tạo branching factor khổng lồ → KHÔNG giải được
    
    "test15_extreme_max": """
L-7L-7L
||+||+|
r-Jr-J|
L-+L-+7
||+||+|
r-Jr-J|
L-7L-7r
""",
    # EXTREME với CROSS khắp nơi, ~40-50 open ends
    # CHẮC CHẮN timeout / RAM overflow
}

def analyze_puzzle(name, puzzle_str):
    """Phân tích puzzle trước khi test"""
    state = PipeState.from_string(puzzle_str)
    open_ends = count_open_ends(state)
    
    # Đếm tiles
    non_empty = 0
    has_cross = False
    has_tjunc = False
    
    for r in range(state.size):
        for c in range(state.size):
            tile = state.get_tile(r, c)
            if tile.type.value > 0:  # Not EMPTY
                non_empty += 1
            if tile.type.name == 'CROSS':
                has_cross = True
            if tile.type.name == 'T_JUNCTION':
                has_tjunc = True
    
    return {
        'name': name,
        'open_ends': open_ends,
        'non_empty_tiles': non_empty,
        'has_cross': has_cross,
        'has_tjunc': has_tjunc,
        'difficulty': (
            'DỄ' if open_ends <= 8 else
            'VỪA' if open_ends <= 14 else
            'KHÓ' if open_ends <= 22 else
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
        
        special = ""
        if analysis['has_cross']:
            special = " [CROSS ⚠️]"
        if analysis['has_tjunc']:
            special += " [T-JUN ⚠️]"
        
        print(f"[{idx:2d}/15] {name:<35} | {analysis['difficulty']:<12} | {analysis['open_ends']:2d} open ends{special}")
    
    # In summary table
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    print(f"{'#':<4} {'Test Name':<35} {'Difficulty':<12} {'Open Ends':<12} {'Est. Time':<20}")
    print("-"*80)
    
    for idx, result in enumerate(results, 1):
        # Estimate time
        difficulty = result['difficulty']
        has_complex = result['has_cross'] or result['has_tjunc']
        
        if difficulty == 'DỄ':
            est_time = "<10s"
        elif difficulty == 'VỪA':
            est_time = "10-60s"
        elif difficulty == 'KHÓ':
            if has_complex:
                est_time = "60-180s hoặc timeout"
            else:
                est_time = "60-180s"
        else:  # EXTREME
            if has_complex:
                est_time = "TIMEOUT / UNSOLVABLE"
            else:
                est_time = ">180s"
        
        print(f"{idx:<4} {result['name']:<35} {result['difficulty']:<12} {result['open_ends']:<12} {est_time:<20}")
    
    # Print category summary
    print("\n" + "="*80)
    print("CATEGORY BREAKDOWN")
    print("="*80)
    
    easy = [r for r in results if r['difficulty'] == 'DỄ']
    medium = [r for r in results if r['difficulty'] == 'VỪA']
    hard = [r for r in results if r['difficulty'] == 'KHÓ']
    extreme = [r for r in results if r['difficulty'] == 'EXTREME']
    
    cross_count = len([r for r in results if r['has_cross'] or r['has_tjunc']])
    
    print(f"DỄ (4-8 open ends):          {len(easy)} cases")
    print(f"VỪA (10-14 open ends):       {len(medium)} cases")
    print(f"KHÓ (16-22 open ends):       {len(hard)} cases")
    print(f"EXTREME (26+ open ends):     {len(extreme)} cases")
    print(f"\nCó CROSS/T-JUNCTION:         {cross_count} cases (test14-15)")
    print(f"Chỉ STRAIGHT + CORNER:       {15 - cross_count} cases (test01-13)")
    
    print("\n" + "="*80)
    print("FILES CREATED")
    print("="*80)
    print(f"Location: ./test_inputs/")
    print(f"Total files: {len(TEST_CASES)}")
    print("\nĐỀ XUẤT SỬ DỤNG:")
    print("  - Demo an toàn: test01-test09 (DỄ + VỪA)")
    print("  - Show giải khó: test10-test13 (KHÓ)")
    print("  - Chứng minh giới hạn: test14-test15 (EXTREME với CROSS - timeout)")
    print("\nLƯU Ý:")
    print("  - Test 01-13: CHỈ STRAIGHT + CORNER → Giải được")
    print("  - Test 14-15: Có CROSS + T-JUNCTION → Timeout / không giải được")
    print("="*80 + "\n")
    
    return results

def main():
    print("\n" + "="*80)
    print("7x7 PIPES WRAP PUZZLE - TEST CASE GENERATOR")
    print("="*80)
    print("\nTạo 15 test cases đơn giản hơn:")
    print("  - Test 01-13: Chỉ STRAIGHT (|, -) và CORNER (L, J, 7, r)")
    print("  - Test 14-15: Có CROSS (+) và T-JUNCTION → Không giải được")
    print("")
    
    results = generate_all_tests()

if __name__ == "__main__":
    main()
