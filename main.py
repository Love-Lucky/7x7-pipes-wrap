class PipeState:
    def __init__(self, grid, current_positions, goals, size=7):
        """
        grid: 2D list where 0 is empty, colors are strings/ints.
        current_positions: Dict {color: (r, c)} of the moving end of the pipe.
        goals: Dict {color: (r, c)} of the fixed destination.
        """
        self.grid = [row[:] for row in grid]
        self.current_positions = current_positions
        self.goals = goals
        self.size = size

    def __eq__(self, other):
        return self.grid == other.grid and self.current_positions == other.current_positions

    def __hash__(self):
        # Stable hash: Sort dictionary items to ensure same hash regardless of insertion order
        return hash((tuple(tuple(row) for row in self.grid), tuple(sorted(self.current_positions.items()))))

    def __lt__(self, other):
        # Required for priority queues (heapq). 
        # Tie-breaking can be arbitrary, we'll use the grid state.
        return self.grid < other.grid

    @staticmethod
    def from_string(grid_str):
        """
        Parses a string representation of the grid.
        Letters (A-Z) are endpoints. '.' or '0' are empty.
        Returns a PipeState.
        """
        lines = [line.strip() for line in grid_str.strip().splitlines() if line.strip()]
        grid = []
        positions = {}
        goals = {}
        
        # Temporary storage to pair up endpoints
        endpoints = {}
        
        for r, line in enumerate(lines):
            row = []
            for c, char in enumerate(line):
                if char in '.0':
                    row.append(0)
                else:
                    # It's a color endpoint
                    row.append(char)
                    if char not in endpoints:
                        endpoints[char] = []
                    endpoints[char].append((r, c))
            grid.append(row)
            
        # Assign start/end. 
        # Arbitrarily pick first occurrence as "current_position" (head) and second as "goal".
        # In a real search, this might swap dynamically, but for init it's fine.
        for color, points in endpoints.items():
            if len(points) != 2:
                raise ValueError(f"Color {color} must have exactly 2 endpoints, found {len(points)}")
            positions[color] = points[0]
            goals[color] = points[1]
            
        return PipeState(grid, positions, goals, size=len(grid))

def is_goal(state):
    # 1. Check if all path heads have reached their goals
    for color, pos in state.current_positions.items():
        if pos != state.goals[color]:
            return False
    
    # 2. Check if the grid is completely filled (no zeros)
    for row in state.grid:
        if 0 in row:
            return False
            
    return True

def get_successors(state):
    successors = []
    
    # Identify the first color that still needs to move
    active_color = None
    for color, pos in state.current_positions.items():
        if pos != state.goals[color]:
            active_color = color
            break
            
    if active_color is None:
        return []

    r, c = state.current_positions[active_color]
    target = state.goals[active_color]

    # Standard moves + Wrap-around moves
    # (dr, dc): Up, Down, Left, Right
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        # Apply wrapping logic using modulo
        nr = (r + dr) % state.size
        nc = (c + dc) % state.size
        
        # Check if the move is valid: 
        # Must be empty OR the target endpoint for this color
        # IMPORTANT: If it's the target, it must be the target for THIS color.
        # Other colors' endpoints are obstacles.
        cell_value = state.grid[nr][nc]
        is_empty = (cell_value == 0)
        is_own_target = ((nr, nc) == target)
        
        if is_empty or is_own_target:
            # Create a deep copy of the grid for the new state
            new_grid = [row[:] for row in state.grid]
            new_grid[nr][nc] = active_color
            
            new_positions = state.current_positions.copy()
            new_positions[active_color] = (nr, nc)
            
            successors.append(PipeState(new_grid, new_positions, state.goals, state.size))
            
    return successors


from collections import deque
import heapq


# HÀM HEURISTIC (HEURISTIC FUNCTIONS)


def manhattan_distance_wrap(pos1, pos2, grid_size):
    """
    Tính Manhattan distance giữa 2 vị trí với wrap-around (toroidal topology).
    
    Trong lưới wrap-around, khoảng cách có thể ngắn hơn nếu đi qua cạnh.
    Ví dụ: trên lưới 7x7, từ (0,0) đến (0,6) có thể:
      - Đi thẳng: 6 bước
      - Wrap qua trái: 1 bước (0,0) -> (0,-1) = (0,6)
    
    Args:
        pos1: tuple (row, col) vị trí 1
        pos2: tuple (row, col) vị trí 2
        grid_size: kích thước lưới (7 cho 7x7)
    
    Returns:
        int: Manhattan distance ngắn nhất (có xét wrap)
    
    Công thức:
        - Với mỗi chiều (row/col), khoảng cách = min(normal_dist, wrap_dist)
        - normal_dist = |pos1 - pos2|
        - wrap_dist = grid_size - normal_dist
    
    Ví dụ:
        Grid 7x7, từ (0,0) đến (0,6):
        - Col: min(|0-6|=6, 7-6=1) = 1 ← chọn wrap!
        - Row: min(|0-0|=0, 7-0=7) = 0
        - Tổng: 1
    """
    r1, c1 = pos1
    r2, c2 = pos2
    
    # Khoảng cách theo hàng (row)
    row_dist = abs(r1 - r2)
    row_wrap_dist = grid_size - row_dist
    min_row_dist = min(row_dist, row_wrap_dist)
    
    # Khoảng cách theo cột (column)
    col_dist = abs(c1 - c2)
    col_wrap_dist = grid_size - col_dist
    min_col_dist = min(col_dist, col_wrap_dist)
    
    return min_row_dist + min_col_dist

def heuristic(state):
    """
    Hàm heuristic h(n) cho A* search.
    
    Ước lượng số bước còn lại từ state hiện tại đến goal state.
    
    THÀNH PHẦN CÁC HEURISTIC:
    
    1. **H1: Tổng Manhattan distance của các màu chưa hoàn thành**
       - Với mỗi màu chưa đến đích, tính khoảng cách từ vị trí hiện tại đến goal
       - Sử dụng Manhattan distance có wrap-around
       - Lý do: Mỗi màu cần ít nhất Manhattan distance bước để đến đích
    
    2. **H2: Số ô trống còn lại**
       - Đếm số ô có giá trị 0 trong grid
       - Mỗi ô trống cần ít nhất 1 bước để lấp đầy
       - Lý do: Goal state yêu cầu lấp đầy toàn bộ lưới
    
    3. **Kết hợp H1 và H2**
       - h(n) = max(H1, H2)
       - Lý do: Cả hai điều kiện đều phải thỏa mãn
       - Chọn max để có heuristic mạnh hơn nhưng vẫn admissible
    
    TÍNH CHẤT:
    - **Admissible**: h(n) <= cost thực tế
      + H1 admissible vì Manhattan distance <= đường đi thực tế
      + H2 admissible vì phải đi qua tất cả ô trống
      + max(H1, H2) vẫn admissible
    
    - **Consistent**: h(n) <= c(n, n') + h(n')
      + Mỗi bước đi giảm Manhattan distance tối đa 1
      + Mỗi bước đi lấp đầy tối đa 1 ô
      + Do đó heuristic consistent
    
    Args:
        state: PipeState object
    
    Returns:
        int: Giá trị heuristic (ước lượng số bước còn lại)
    
    Ví dụ:
        State: A ở (0,0), goal ở (0,4), lưới 5x5, 20 ô trống
        - H1 = manhattan_distance_wrap((0,0), (0,4), 5) = 1 (wrap!)
        - H2 = 20 ô trống
        - h(n) = max(1, 20) = 20
    """
    h1 = 0  # Tổng Manhattan distance
    h2 = 0  # Số ô trống
    
    # H1: Tính tổng Manhattan distance của các màu chưa hoàn thành
    for color, current_pos in state.current_positions.items():
        goal_pos = state.goals[color]
        
        # Nếu màu này chưa đến đích
        if current_pos != goal_pos:
            distance = manhattan_distance_wrap(current_pos, goal_pos, state.size)
            h1 += distance
    
    # H2: Đếm số ô trống (giá trị 0)
    for row in state.grid:
        h2 += row.count(0)
    
    # Trả về max của hai heuristic
    # Lý do dùng max:
    # - Cả hai điều kiện đều cần thỏa mãn để đạt goal
    # - max() cho heuristic mạnh hơn (ít node expand hơn)
    # - max() vẫn admissible nếu cả hai thành phần đều admissible
    return max(h1, h2)

def heuristic_simple(state):
    """
    Heuristic đơn giản hơn - chỉ dùng Manhattan distance.
    Dùng để so sánh performance với heuristic phức tạp hơn.
    Args:
        state: PipeState object
    Returns:
        int: Tổng Manhattan distance của các màu chưa hoàn thành
    """
    total_distance = 0
    
    for color, current_pos in state.current_positions.items():
        goal_pos = state.goals[color]
        if current_pos != goal_pos:
            distance = manhattan_distance_wrap(current_pos, goal_pos, state.size)
            total_distance += distance
    
    return total_distance

def heuristic_empty_cells(state):
    """
    Heuristic chỉ đếm số ô trống.
    
    Đơn giản nhưng đôi khi hiệu quả.
    
    Args:
        state: PipeState object
    
    Returns:
        int: Số ô trống trong grid
    """
    empty_count = 0
    for row in state.grid:
        empty_count += row.count(0)
    return empty_count

# THUẬT TOÁN TÌM KIẾM MÙ (BLIND SEARCH ALGORITHMS)


def bfs(initial_state):
    if is_goal(initial_state):
        return initial_state, [initial_state], {'nodes_explored': 0, 'max_frontier_size': 1}
    
    # Queue cho BFS (FIFO)
    frontier = deque([(initial_state, [initial_state])])
    visited = {initial_state}
    
    # Thống kê
    nodes_explored = 0
    max_frontier_size = 1
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        current_state, path = frontier.popleft()
        nodes_explored += 1
        
        # Sinh các trạng thái kế tiếp
        for successor in get_successors(current_state):
            if successor not in visited:
                visited.add(successor)
                new_path = path + [successor]
                
                # Kiểm tra đích
                if is_goal(successor):
                    stats = {
                        'nodes_explored': nodes_explored,
                        'max_frontier_size': max_frontier_size,
                        'path_length': len(new_path),
                        'visited_states': len(visited)
                    }
                    return successor, new_path, stats
                
                frontier.append((successor, new_path))
    
    # Không tìm thấy solution
    stats = {
        'nodes_explored': nodes_explored,
        'max_frontier_size': max_frontier_size,
        'visited_states': len(visited)
    }
    return None, None, stats

def dfs(initial_state, max_depth=1000):
   
    if is_goal(initial_state):
        return initial_state, [initial_state], {'nodes_explored': 0, 'max_depth': 0}
    
    # Stack cho DFS (LIFO)
    frontier = [(initial_state, [initial_state], 0)]  # (state, path, depth)
    visited = {initial_state}
    
    # Thống kê
    nodes_explored = 0
    max_frontier_size = 1
    max_depth_reached = 0
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        current_state, path, depth = frontier.pop()
        nodes_explored += 1
        max_depth_reached = max(max_depth_reached, depth)
        
        # Kiểm tra độ sâu
        if depth >= max_depth:
            continue
        
        # Sinh các trạng thái kế tiếp
        for successor in get_successors(current_state):
            if successor not in visited:
                visited.add(successor)
                new_path = path + [successor]
                
                # Kiểm tra đích
                if is_goal(successor):
                    stats = {
                        'nodes_explored': nodes_explored,
                        'max_frontier_size': max_frontier_size,
                        'path_length': len(new_path),
                        'visited_states': len(visited),
                        'max_depth_reached': max_depth_reached + 1
                    }
                    return successor, new_path, stats
                
                frontier.append((successor, new_path, depth + 1))
    
    # Không tìm thấy solution
    stats = {
        'nodes_explored': nodes_explored,
        'max_frontier_size': max_frontier_size,
        'visited_states': len(visited),
        'max_depth_reached': max_depth_reached
    }
    return None, None, stats

# ============================================================================
# INFORMED SEARCH ALGORITHMS
# ============================================================================

def astar(initial_state):
    """
    A* Search - Thuật toán tìm kiếm tối ưu với heuristic.
    
    A* kết hợp cost thực tế g(n) và heuristic h(n):
        f(n) = g(n) + h(n)
    
    Trong đó:
        - g(n): Chi phí thực tế từ start đến node n
        - h(n): Ước lượng chi phí từ n đến goal (heuristic)
        - f(n): Ước lượng tổng chi phí từ start qua n đến goal
    
    NGUYÊN LÝ:
        - Mở rộng node có f(n) nhỏ nhất
        - Sử dụng Priority Queue (min-heap) để lưu frontier
        - Đảm bảo tìm được đường đi tối ưu nếu h(n) admissible
    """
    if is_goal(initial_state):
        return initial_state, [initial_state], {'nodes_explored': 0, 'max_frontier_size': 1}
    
    # Priority queue: (f_score, counter, g_score, state, path)
    # counter để break ties khi f_score bằng nhau
    counter = 0
    g_score = 0  # Cost từ start đến initial_state
    h_score = heuristic(initial_state)
    f_score = g_score + h_score
    
    frontier = [(f_score, counter, g_score, initial_state, [initial_state])]
    visited = {initial_state}
    
    # Thống kê
    nodes_explored = 0
    max_frontier_size = 1
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        
        # Lấy node có f_score nhỏ nhất
        current_f, _, current_g, current_state, path = heapq.heappop(frontier)
        nodes_explored += 1
        
        # Sinh các trạng thái kế tiếp
        for successor in get_successors(current_state):
            if successor not in visited:
                visited.add(successor)
                counter += 1
                
                # Tính các score cho successor
                new_g = current_g + 1  # Cost mỗi bước = 1
                new_h = heuristic(successor)
                new_f = new_g + new_h
                new_path = path + [successor]
                
                # Kiểm tra đích
                if is_goal(successor):
                    stats = {
                        'nodes_explored': nodes_explored,
                        'max_frontier_size': max_frontier_size,
                        'path_length': len(new_path),
                        'visited_states': len(visited),
                        'path_cost': new_g
                    }
                    return successor, new_path, stats
                
                # Thêm vào frontier
                heapq.heappush(frontier, (new_f, counter, new_g, successor, new_path))
    
    # Không tìm thấy solution
    stats = {
        'nodes_explored': nodes_explored,
        'max_frontier_size': max_frontier_size,
        'visited_states': len(visited)
    }
    return None, None, stats

def hill_climbing(initial_state, max_iterations=10000):
    """
    Hill Climbing - Thuật toán tìm kiếm local search.
    
    NGUYÊN LÝ:
        - Bắt đầu từ state hiện tại
        - Chọn successor có h(n) NHỎ NHẤT (gần goal nhất)
        - Di chuyển đến successor đó
        - Lặp lại cho đến khi đạt goal hoặc stuck
    
    LƯU Ý:
        - h(n) NHỎ → GẦN GOAL hơn
        - Chọn successor có h(n) nhỏ nhất = greedy best-first
    """
    if is_goal(initial_state):
        return initial_state, [initial_state], {'nodes_explored': 0, 'iterations': 0}
    
    current_state = initial_state
    path = [initial_state]
    visited = {initial_state}
    
    # Thống kê
    nodes_explored = 0
    iterations = 0
    max_successors_size = 0
    
    for iterations in range(max_iterations):
        # Sinh các successors
        successors = get_successors(current_state)
        
        # Lọc bỏ các state đã thăm (để tránh vòng lặp)
        unvisited_successors = [s for s in successors if s not in visited]
        
        if not unvisited_successors:
            # Stuck - không còn successor chưa thăm
            stats = {
                'nodes_explored': nodes_explored,
                'iterations': iterations,
                'visited_states': len(visited),
                'stuck': True,
                'reason': 'No unvisited successors'
            }
            return None, path, stats
        
        max_successors_size = max(max_successors_size, len(unvisited_successors))
        
        # Tính h(n) cho tất cả successors
        successors_with_h = []
        for successor in unvisited_successors:
            h_value = heuristic(successor)
            successors_with_h.append((h_value, successor))
            nodes_explored += 1
            
            # Kiểm tra nếu successor là goal
            if is_goal(successor):
                new_path = path + [successor]
                stats = {
                    'nodes_explored': nodes_explored,
                    'iterations': iterations + 1,
                    'path_length': len(new_path),
                    'visited_states': len(visited) + 1,
                    'max_successors_size': max_successors_size
                }
                return successor, new_path, stats
        
        # Sắp xếp theo h(n) tăng dần (nhỏ nhất = tốt nhất)
        successors_with_h.sort(key=lambda x: x[0])
        
        # Chọn successor tốt nhất (h(n) nhỏ nhất)
        best_h, best_successor = successors_with_h[0]
        current_h = heuristic(current_state)
        
        # Kiểm tra có cải thiện không
        if best_h >= current_h:
            # Stuck at local minimum - successor tốt nhất vẫn tệ hơn hoặc bằng hiện tại
            stats = {
                'nodes_explored': nodes_explored,
                'iterations': iterations + 1,
                'visited_states': len(visited),
                'stuck': True,
                'reason': f'Local minimum (current h={current_h}, best successor h={best_h})'
            }
            return None, path, stats
        
        # Di chuyển đến successor tốt nhất
        current_state = best_successor
        path.append(best_successor)
        visited.add(best_successor)
    
    # Đã đạt max_iterations
    stats = {
        'nodes_explored': nodes_explored,
        'iterations': max_iterations,
        'visited_states': len(visited),
        'stuck': True,
        'reason': 'Max iterations reached'
    }
    return None, path, stats