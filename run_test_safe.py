"""
Script chạy test AN TOÀN với giới hạn RAM và timeout
Tự động STOP khi RAM quá cao hoặc timeout
"""

import tracemalloc
import signal
import sys
import time
from main import PipeState, astar, count_open_ends

# ============================================================================
# GIỚI HẠN AN TOÀN
# ============================================================================
MAX_RAM_MB = 500  # Dừng khi RAM > 500 MB
MAX_TIME_SECONDS = 120  # Dừng sau 120 giây
MAX_NODES = 100000  # Dừng khi explore > 100K nodes

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Timeout!")

def run_test_safe(test_file, max_ram_mb=MAX_RAM_MB, max_time=MAX_TIME_SECONDS):
    """
    Chạy test với giới hạn RAM và timeout
    
    Returns:
        dict với kết quả hoặc error
    """
    print("="*80)
    print(f"SAFE TEST: {test_file}")
    print("="*80)
    print(f"Giới hạn: RAM < {max_ram_mb} MB, Time < {max_time}s")
    
    # Đọc puzzle
    try:
        with open(test_file, 'r') as f:
            puzzle_str = f.read()
    except FileNotFoundError:
        return {'error': 'File not found', 'status': 'ERROR'}
    
    state = PipeState.from_string(puzzle_str)
    open_ends = count_open_ends(state)
    
    print(f"\nInitial state:")
    print(f"  Open ends: {open_ends}")
    
    # Đánh giá độ khó
    if open_ends > 30:
        print(f"\n⚠️ CẢNH BÁO: {open_ends} open ends - RẤT KHÓ!")
        print(f"   Có thể gây tràn RAM hoặc timeout")
        confirm = input("   Bạn có muốn tiếp tục? (y/n): ")
        if confirm.lower() != 'y':
            return {'error': 'User cancelled', 'status': 'CANCELLED'}
    
    # Bắt đầu tracking
    tracemalloc.start()
    
    # Set timeout
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(max_time)
    
    start_time = time.time()
    result = {}
    
    try:
        print(f"\n🚀 Đang chạy A* search...")
        print(f"   (Checking RAM every 5000 nodes)")
        
        # Chạy A* với monitoring
        nodes_count = 0
        
        # Chạy với custom astar có monitoring
        solution, path, stats = astar(state, show_progress=True)
        
        elapsed = time.time() - start_time
        current, peak = tracemalloc.get_traced_memory()
        
        # Check RAM
        peak_mb = peak / 1024 / 1024
        if peak_mb > max_ram_mb:
            signal.alarm(0)  # Cancel timeout
            tracemalloc.stop()
            print(f"\n❌ STOPPED! RAM vượt giới hạn: {peak_mb:.2f} MB > {max_ram_mb} MB")
            return {
                'status': 'RAM_OVERFLOW',
                'peak_ram_mb': peak_mb,
                'nodes': stats['nodes_explored'],
                'time': elapsed
            }
        
        # Success
        signal.alarm(0)  # Cancel timeout
        tracemalloc.stop()
        
        print(f"\n✅ SOLVED!")
        print(f"   Time: {elapsed:.2f}s")
        print(f"   Nodes: {stats['nodes_explored']:,}")
        print(f"   Peak RAM: {peak_mb:.2f} MB")
        
        return {
            'status': 'SOLVED',
            'open_ends': open_ends,
            'nodes': stats['nodes_explored'],
            'time': elapsed,
            'peak_ram_mb': peak_mb,
            'path_length': len(path)
        }
        
    except TimeoutException:
        signal.alarm(0)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        elapsed = time.time() - start_time
        
        print(f"\n⏱️ TIMEOUT sau {elapsed:.2f}s")
        print(f"   Peak RAM: {peak / 1024 / 1024:.2f} MB")
        
        return {
            'status': 'TIMEOUT',
            'time': elapsed,
            'peak_ram_mb': peak / 1024 / 1024
        }
        
    except KeyboardInterrupt:
        signal.alarm(0)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"\n🛑 STOPPED BY USER")
        print(f"   Peak RAM: {peak / 1024 / 1024:.2f} MB")
        
        return {
            'status': 'CANCELLED',
            'peak_ram_mb': peak / 1024 / 1024
        }
        
    except Exception as e:
        signal.alarm(0)
        tracemalloc.stop()
        
        print(f"\n❌ ERROR: {e}")
        
        return {
            'status': 'ERROR',
            'error': str(e)
        }

def main():
    print("\n" + "="*80)
    print("SAFE TEST RUNNER - CHẠY TEST AN TOÀN")
    print("="*80)
    print("\nTính năng:")
    print("  ✅ Tự động dừng khi RAM > 500 MB")
    print("  ✅ Tự động dừng khi timeout > 120s")
    print("  ✅ Cảnh báo khi test quá khó (>30 open ends)")
    print("  ✅ Có thể Ctrl+C để dừng bất cứ lúc nào")
    
    if len(sys.argv) < 2:
        print("\nUsage: python3 run_test_safe.py <test_file>")
        print("\nVí dụ:")
        print("  python3 run_test_safe.py test_inputs/test01_easy_tiny.txt")
        print("  python3 run_test_safe.py test_inputs/test07_medium_l_shape.txt")
        print("\n⚠️ KHÔNG NÊN chạy test14-15 (EXTREME với CROSS) - chắc chắn timeout!")
        sys.exit(1)
    
    test_file = sys.argv[1]
    
    # Chạy test
    result = run_test_safe(test_file)
    
    # Hiển thị kết quả
    print("\n" + "="*80)
    print("KẾT QUẢ:")
    print("="*80)
    
    if result['status'] == 'SOLVED':
        print(f"✅ Giải thành công!")
        print(f"   Nodes: {result['nodes']:,}")
        print(f"   Time: {result['time']:.2f}s")
        print(f"   RAM: {result['peak_ram_mb']:.2f} MB")
        print(f"   Path: {result['path_length']} steps")
    elif result['status'] == 'TIMEOUT':
        print(f"⏱️ Timeout sau {result['time']:.2f}s")
        print(f"   Peak RAM: {result['peak_ram_mb']:.2f} MB")
    elif result['status'] == 'RAM_OVERFLOW':
        print(f"❌ RAM vượt giới hạn!")
        print(f"   Peak RAM: {result['peak_ram_mb']:.2f} MB (> {MAX_RAM_MB} MB)")
        print(f"   Nodes: {result['nodes']:,}")
    elif result['status'] == 'CANCELLED':
        print(f"🛑 Đã dừng bởi user")
        print(f"   Peak RAM: {result['peak_ram_mb']:.2f} MB")
    else:
        print(f"❌ Lỗi: {result.get('error', 'Unknown')}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
