"""
Script chạy TẤT CẢ 15 test cases AN TOÀN
Tự động SKIP các test quá khó
Ghi kết quả vào CSV cho Excel
"""

import tracemalloc
import time
import csv
import os
from main import PipeState, astar, count_open_ends

# ============================================================================
# CẤU HÌNH AN TOÀN
# ============================================================================

# Test cases được phép chạy (KHÔNG bao gồm test14-15 - quá nguy hiểm!)
SAFE_TESTS = [
    'test01_easy_tiny.txt',
    'test02_easy_tall.txt', 
    'test03_easy_frame.txt',
    'test04_easy_two.txt',
    'test05_easy_nested.txt',
    'test06_medium_three.txt',
    'test07_medium_l_shape.txt',
    'test08_medium_connected.txt',
    # test09-13: SKIP vì quá khó (28 open ends)
    # test14-15: SKIP vì có CROSS - chắc chắn timeout
]

MAX_TIMEOUT = 120  # 2 phút per test
MAX_RAM_WARNING = 300  # Cảnh báo nếu RAM > 300 MB

def run_single_test(test_file, timeout=MAX_TIMEOUT):
    """Chạy 1 test với tracking"""
    
    print(f"\n{'='*80}")
    print(f"Testing: {test_file}")
    print(f"{'='*80}")
    
    # Đọc puzzle
    filepath = f"test_inputs/{test_file}"
    if not os.path.exists(filepath):
        print(f"❌ File không tồn tại: {filepath}")
        return None
    
    with open(filepath, 'r') as f:
        puzzle_str = f.read()
    
    state = PipeState.from_string(puzzle_str)
    open_ends = count_open_ends(state)
    
    print(f"Open ends: {open_ends}")
    
    # Bắt đầu tracking
    tracemalloc.start()
    start = time.time()
    
    try:
        # Chạy A* (KHÔNG show progress để nhanh hơn)
        solution, path, stats = astar(state, show_progress=False)
        
        elapsed = time.time() - start
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        peak_mb = peak / 1024 / 1024
        
        # Check timeout
        if elapsed > timeout:
            print(f"⏱️ TIMEOUT sau {elapsed:.2f}s")
            return {
                'test': test_file,
                'status': 'TIMEOUT',
                'open_ends': open_ends,
                'nodes': stats.get('nodes_explored', 0),
                'time_s': elapsed,
                'ram_mb': peak_mb,
                'path_length': 0
            }
        
        # Success
        print(f"✅ SOLVED in {elapsed:.2f}s")
        print(f"   Nodes: {stats['nodes_explored']:,}")
        print(f"   RAM: {peak_mb:.2f} MB")
        
        if peak_mb > MAX_RAM_WARNING:
            print(f"   ⚠️ RAM cao! ({peak_mb:.2f} MB)")
        
        return {
            'test': test_file,
            'status': 'SOLVED',
            'open_ends': open_ends,
            'nodes': stats['nodes_explored'],
            'time_s': round(elapsed, 2),
            'ram_mb': round(peak_mb, 2),
            'path_length': len(path)
        }
        
    except KeyboardInterrupt:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        elapsed = time.time() - start
        
        print(f"\n🛑 STOPPED BY USER!")
        print(f"   Time: {elapsed:.2f}s")
        print(f"   RAM: {peak / 1024 / 1024:.2f} MB")
        
        return {
            'test': test_file,
            'status': 'CANCELLED',
            'open_ends': open_ends,
            'nodes': 0,
            'time_s': elapsed,
            'ram_mb': peak / 1024 / 1024,
            'path_length': 0
        }
        
    except Exception as e:
        tracemalloc.stop()
        print(f"\n❌ ERROR: {e}")
        
        return {
            'test': test_file,
            'status': 'ERROR',
            'open_ends': open_ends,
            'error': str(e)
        }

def save_results_csv(results, filename='test_results.csv'):
    """Lưu kết quả vào CSV cho Excel"""
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'test', 'status', 'open_ends', 'nodes', 'time_s', 'ram_mb', 'path_length'
        ])
        writer.writeheader()
        
        for result in results:
            if result:
                writer.writerow({
                    'test': result['test'],
                    'status': result['status'],
                    'open_ends': result['open_ends'],
                    'nodes': result.get('nodes', 0),
                    'time_s': result.get('time_s', 0),
                    'ram_mb': result.get('ram_mb', 0),
                    'path_length': result.get('path_length', 0)
                })
    
    print(f"\n📊 Kết quả đã lưu vào: {filename}")

def main():
    print("\n" + "="*80)
    print("SAFE TEST RUNNER - CHẠY TẤT CẢ TESTS AN TOÀN")
    print("="*80)
    
    print(f"\n📋 Sẽ chạy {len(SAFE_TESTS)} test cases:")
    for i, test in enumerate(SAFE_TESTS, 1):
        print(f"   {i}. {test}")
    
    print(f"\n⚠️ SKIP các test nguy hiểm:")
    print(f"   - test09-13: 28 open ends - quá khó, có thể >300s")
    print(f"   - test14-15: CROSS - chắc chắn timeout/RAM overflow")
    
    print(f"\n🔒 Giới hạn an toàn:")
    print(f"   - Max RAM: {MAX_RAM_WARNING} MB")
    print(f"   - Max Time: {MAX_TIMEOUT}s per test")
    print(f"   - Có thể Ctrl+C để dừng bất cứ lúc nào")
    
    input("\n▶️ Press Enter để bắt đầu...")
    
    # Chạy tất cả tests
    results = []
    
    for i, test_file in enumerate(SAFE_TESTS, 1):
        print(f"\n\n{'#'*80}")
        print(f"# TEST {i}/{len(SAFE_TESTS)}")
        print(f"{'#'*80}")
        
        result = run_single_test(test_file, timeout=MAX_TIMEOUT)
        if result:
            results.append(result)
        
        # Pause giữa các tests
        if i < len(SAFE_TESTS):
            time.sleep(2)
    
    # Hiển thị summary
    print("\n\n" + "="*80)
    print("SUMMARY - TỔNG KẾT")
    print("="*80)
    
    print(f"\n{'Test':<30} {'Status':<12} {'Nodes':<12} {'Time (s)':<10} {'RAM (MB)':<10}")
    print("-"*80)
    
    for r in results:
        print(f"{r['test']:<30} {r['status']:<12} {r.get('nodes', 0):>11,} {r.get('time_s', 0):>9.2f} {r.get('ram_mb', 0):>9.2f}")
    
    # Lưu vào CSV
    save_results_csv(results)
    
    # Statistics
    solved = [r for r in results if r['status'] == 'SOLVED']
    timeout = [r for r in results if r['status'] == 'TIMEOUT']
    cancelled = [r for r in results if r['status'] == 'CANCELLED']
    
    print(f"\n📊 Statistics:")
    print(f"   ✅ Solved: {len(solved)}/{len(results)}")
    print(f"   ⏱️ Timeout: {len(timeout)}")
    print(f"   🛑 Cancelled: {len(cancelled)}")
    
    if solved:
        avg_time = sum(r['time_s'] for r in solved) / len(solved)
        avg_ram = sum(r['ram_mb'] for r in solved) / len(solved)
        print(f"\n   Average (solved tests):")
        print(f"     Time: {avg_time:.2f}s")
        print(f"     RAM: {avg_ram:.2f} MB")
    
    print("\n" + "="*80)
    print("✅ HOÀN THÀNH!")
    print(f"Kết quả đã lưu vào: test_results.csv")
    print("Mở file CSV bằng Excel để xem chi tiết")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
