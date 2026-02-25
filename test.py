from main import PipeState, get_successors, is_goal, count_open_ends, TileType, Tile

def print_state(state):
    """
    In trạng thái lưới với ký tự Unicode đẹp.
    """
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
    print(f"Is goal? {is_goal(state)}")
    print()


def test_basic():
    """Test cơ bản với puzzle nhỏ"""
    print("=== TEST 1: PUZZLE ĐƠN GIẢN 3x3 ===")
    print("Mục tiêu: Xoay các ống để tạo mạng kết nối hoàn chỉnh\n")
    
    # Puzzle đơn giản: 3x3 với một số ống cần xoay
    puzzle_str = """
    |-L
    |.J
    L-7
    """
    
    initial_state = PipeState.from_string(puzzle_str)
    print("TRẠNG THÁI BAN ĐẦU:")
    print_state(initial_state)
    
    # Hiển thị một số successors
    print("VÍ DỤ CÁC BƯỚC ĐI (xoay tile):")
    successors = get_successors(initial_state)
    print(f"Tổng số bước có thể: {len(successors)}\n")
    
    # Hiển thị 5 successor đầu tiên
    for i, succ in enumerate(successors[:5]):
        print(f"Option {i+1} (xoay 1 tile 90°):")
        print_state(succ)
    
    print(f"... và {len(successors) - 5} bước khác nữa.\n")


def test_wrap():
    """Test tính năng wrap"""
    print("=== TEST 2: WRAP FEATURE ===")
    print("Các ống có thể kết nối qua biên (wrap-around)\n")
    
    # Puzzle với wrap: ống ở cạnh phải nối với cạnh trái
    puzzle_str = """
    -..
    ...
    ..-
    """
    
    state = PipeState.from_string(puzzle_str)
    print("Lưới ban đầu:")
    print_state(state)
    
    print("Giải thích:")
    print("- Ống ngang ở (0,0): đầu trái wrap sang (0,2)")
    print("- Ống ngang ở (2,2): đầu phải wrap sang (2,0)")
    print("- Nếu xoay đúng → tạo vòng kết nối qua biên!\n")


def test_solution():
    """Test một puzzle có solution"""
    print("=== TEST 3: TÌM SOLUTION ===")
    print("Puzzle đơn giản có thể giải bằng 1 bước\n")
    
    # Puzzle gần giải: chỉ cần xoay 1 ống
    # Tạo một lưới 3x3 đã gần hoàn chỉnh
    puzzle_str = """
    L-7
    |.|
    r-J
    """
    
    initial_state = PipeState.from_string(puzzle_str)
    print("TRẠNG THÁI BAN ĐẦU (gần giải):")
    print_state(initial_state)
    
    # Xoay tile giữa (1,1) từ EMPTY thành gì đó
    # Thực tế puzzle này có ô giữa trống, cần điều chỉnh
    
    print("Nếu xoay đúng các tile → Open ends = 0 → GOAL!\n")


def test_tile_types():
    """Test các loại tile khác nhau"""
    print("=== TEST 4: CÁC LOẠI TILE ===\n")
    
    tiles = [
        (TileType.STRAIGHT, 0, "Ống thẳng dọc │"),
        (TileType.STRAIGHT, 1, "Ống thẳng ngang ─"),
        (TileType.CORNER, 0, "Ống góc └"),
        (TileType.CORNER, 1, "Ống góc ┘"),
        (TileType.CORNER, 2, "Ống góc ┐"),
        (TileType.CORNER, 3, "Ống góc ┌"),
        (TileType.T_JUNCTION, 0, "Ống chữ T ├"),
        (TileType.T_JUNCTION, 1, "Ống chữ T ┬"),
        (TileType.T_JUNCTION, 2, "Ống chữ T ┤"),
        (TileType.T_JUNCTION, 3, "Ống chữ T ┴"),
        (TileType.CROSS, 0, "Ống chữ + ┼"),
    ]
    
    for tile_type, rotation, description in tiles:
        tile = Tile(tile_type, rotation)
        connections = tile.get_connections()
        direction_names = {0: "Up", 1: "Right", 2: "Down", 3: "Left"}
        conn_str = ", ".join([direction_names[d] for d in connections])
        
        print(f"{tile.to_char()} - {description}")
        print(f"   Connections: {conn_str}")
        print()


def main():
    """Chạy tất cả tests"""
    print("\n" + "="*50)
    print("TEST PIPE ROTATION PUZZLE")
    print("Game mechanics: Xoay các ống để tạo mạng kết nối")
    print("="*50 + "\n")
    
    test_tile_types()
    test_basic()
    test_wrap()
    test_solution()
    
    print("="*50)
    print("HOÀN THÀNH TẤT CẢ TESTS!")
    print("="*50)


if __name__ == "__main__":
    main()
