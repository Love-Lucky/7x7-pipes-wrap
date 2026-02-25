# ============================================================================
# 7x7 PIPES WRAP PUZZLE - PIPE ROTATION VERSION
# ============================================================================

# ============================================================================

from collections import deque
import heapq
from enum import Enum
from typing import List, Tuple, Dict, Set


# ============================================================================
# TILE TYPES - CÁC LOẠI ỐNG
# ============================================================================

class TileType(Enum):
    """
    Các loại tile ống:
    - EMPTY: Ô trống (không có ống)
    - STRAIGHT: Ống thẳng (2 đầu nối: 0-2 hoặc 1-3)
    - CORNER: Ống góc (2 đầu nối: 0-1, 1-2, 2-3, 3-0)
    - T_JUNCTION: Ống chữ T (3 đầu nối)
    - CROSS: Ống chữ + (4 đầu nối)
    """
    EMPTY = 0       # ' '
    STRAIGHT = 1    # │ hoặc ─
    CORNER = 2      # └ ┘ ┐ ┌
    T_JUNCTION = 3  # ├ ┤ ┬ ┴
    CROSS = 4       # ┼


# ============================================================================
# TILE CLASS - MỖI Ô LƯỚI
# ============================================================================

class Tile:

    # Định nghĩa connections cho mỗi loại tile ở rotation 0
    BASE_CONNECTIONS = {
        TileType.EMPTY: [],
        TileType.STRAIGHT: [0, 2],      # Up-Down (│)
        TileType.CORNER: [2, 3],        # Down-Left (└)
        TileType.T_JUNCTION: [0, 1, 2], # Up-Right-Down (├)
        TileType.CROSS: [0, 1, 2, 3]    # All directions (┼)
    }
    
    def __init__(self, tile_type: TileType, rotation: int = 0):
        """
        Args:
            tile_type: Loại tile (STRAIGHT, CORNER, etc.)
            rotation: Độ xoay (0, 1, 2, 3)
        """
        self.type = tile_type
        self.rotation = rotation % 4  # Đảm bảo 0-3
    
    def get_connections(self) -> List[int]:

        base = self.BASE_CONNECTIONS[self.type]
        # Xoay mỗi connection theo rotation
        return [(conn + self.rotation) % 4 for conn in base]
    
    def rotate(self, times: int = 1) -> 'Tile':
        return Tile(self.type, self.rotation + times)
    
    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.type == other.type and self.rotation == other.rotation
    
    def __hash__(self):
        return hash((self.type, self.rotation))
    
    def __repr__(self):
        return f"Tile({self.type.name}, rot={self.rotation})"
    
    def to_char(self) -> str:
        """
        Chuyển tile thành ký tự hiển thị.
        
        Returns:
            Ký tự đại diện cho tile
        """
        if self.type == TileType.EMPTY:
            return ' '
        
        # Ký tự Unicode cho các loại ống
        chars = {
            TileType.STRAIGHT: ['│', '─', '│', '─'],
            TileType.CORNER: ['└', '┘', '┐', '┌'],
            TileType.T_JUNCTION: ['├', '┬', '┤', '┴'],
            TileType.CROSS: ['┼', '┼', '┼', '┼']
        }
        
        return chars[self.type][self.rotation]


# ============================================================================
# PIPE STATE CLASS
# ============================================================================

class PipeState:
    """
    Trạng thái bài toán: Lưới các tile ống.
    """
    
    def __init__(self, grid: List[List[Tile]], size: int = 7):
        """
        Args:
            grid: 2D list của Tile objects
            size: Kích thước lưới (7 cho 7x7)
        """
        self.grid = [row[:] for row in grid]  # Deep copy
        self.size = size
    
    def __eq__(self, other):
        if not isinstance(other, PipeState):
            return False
        return self.grid == other.grid
    
    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.grid))
    
    def __lt__(self, other):
        # Cho priority queue
        return str(self.grid) < str(other.grid)
    
    @staticmethod
    def from_string(grid_str: str) -> 'PipeState':
        """
        Parse string thành PipeState.
        
        Format:
            | = STRAIGHT vertical (rotation 0)
            - = STRAIGHT horizontal (rotation 1)
            L = CORNER (└, rotation 0)
            J = CORNER (┘, rotation 1)
            7 = CORNER (┐, rotation 2)
            r = CORNER (┌, rotation 3)
            T = T_JUNCTION (├, rotation 0)
            F = T_JUNCTION (┬, rotation 1)
            H = T_JUNCTION (┤, rotation 2)
            E = T_JUNCTION (┴, rotation 3)
            + = CROSS
            . = EMPTY
        
        Example:
            '''
            |-L.
            |.J-
            +TT+
            '''
        """
        lines = [line.strip() for line in grid_str.strip().splitlines() if line.strip()]
        
        char_map = {
            '.': (TileType.EMPTY, 0),
            ' ': (TileType.EMPTY, 0),
            '|': (TileType.STRAIGHT, 0),
            '-': (TileType.STRAIGHT, 1),
            'L': (TileType.CORNER, 0),
            'J': (TileType.CORNER, 1),
            '7': (TileType.CORNER, 2),
            'r': (TileType.CORNER, 3),
            'T': (TileType.T_JUNCTION, 0),
            'F': (TileType.T_JUNCTION, 1),
            'H': (TileType.T_JUNCTION, 2),
            'E': (TileType.T_JUNCTION, 3),
            '+': (TileType.CROSS, 0),
        }
        
        grid = []
        for line in lines:
            row = []
            for char in line:
                if char in char_map:
                    tile_type, rotation = char_map[char]
                    row.append(Tile(tile_type, rotation))
                else:
                    # Default: empty
                    row.append(Tile(TileType.EMPTY, 0))
            grid.append(row)
        
        size = len(grid)
        return PipeState(grid, size)
    
    def get_tile(self, r: int, c: int) -> Tile:
        """Lấy tile tại vị trí (r, c)"""
        return self.grid[r][c]
    
    def set_tile(self, r: int, c: int, tile: Tile) -> 'PipeState':
        """
        Tạo state mới với tile tại (r, c) được thay đổi.
        
        Returns:
            PipeState mới
        """
        new_grid = [row[:] for row in self.grid]
        new_grid[r][c] = tile
        return PipeState(new_grid, self.size)


# ============================================================================
# GAME LOGIC
# ============================================================================

def get_neighbor_pos(r: int, c: int, direction: int, size: int) -> Tuple[int, int]:
    deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
    dr, dc = deltas[direction]
    return ((r + dr) % size, (c + dc) % size)


def is_connected(state: PipeState, r: int, c: int, direction: int) -> bool:
    
    tile = state.get_tile(r, c)
    connections = tile.get_connections()
    
    # Tile hiện tại phải có connection theo direction
    if direction not in connections:
        return False
    
    # Lấy vị trí láng giềng (có wrap)
    nr, nc = get_neighbor_pos(r, c, direction, state.size)
    neighbor_tile = state.get_tile(nr, nc)
    neighbor_connections = neighbor_tile.get_connections()
    
    # Láng giềng phải có connection ngược lại
    opposite_direction = (direction + 2) % 4
    return opposite_direction in neighbor_connections


def count_open_ends(state: PipeState) -> int:
    open_count = 0
    
    for r in range(state.size):
        for c in range(state.size):
            tile = state.get_tile(r, c)
            connections = tile.get_connections()
            
            # Đếm số connection không nối với láng giềng
            for direction in connections:
                if not is_connected(state, r, c, direction):
                    open_count += 1
    
    return open_count


def is_goal(state: PipeState) -> bool:
    return count_open_ends(state) == 0


def get_tiles_with_open_ends(state: PipeState) -> Set[Tuple[int, int]]:
    tiles_to_rotate = set()
    
    for r in range(state.size):
        for c in range(state.size):
            tile = state.get_tile(r, c)
            
            if tile.type == TileType.EMPTY or tile.type == TileType.CROSS:
                continue
            
            connections = tile.get_connections()
            has_open_end = False
            
            # Check nếu tile có open end
            for direction in connections:
                if not is_connected(state, r, c, direction):
                    has_open_end = True
                    break
            
            if has_open_end:
                tiles_to_rotate.add((r, c))
                
                # Thêm láng giềng
                for direction in range(4):
                    nr, nc = get_neighbor_pos(r, c, direction, state.size)
                    neighbor_tile = state.get_tile(nr, nc)
                    if neighbor_tile.type != TileType.EMPTY:
                        tiles_to_rotate.add((nr, nc))
    
    return tiles_to_rotate


def get_successors(state: PipeState, optimized: bool = True) -> List[PipeState]:
    successors = []
    
    if optimized:
        # Chỉ xoay tiles liên quan
        tiles_to_rotate = get_tiles_with_open_ends(state)
        
        if not tiles_to_rotate:
            return []
        
        for r, c in tiles_to_rotate:
            tile = state.get_tile(r, c)
            
            if tile.type == TileType.CROSS:
                continue
            
            rotated_tile = tile.rotate(1)
            new_state = state.set_tile(r, c, rotated_tile)
            successors.append(new_state)
    else:
        # Xoay tất cả tiles (cách cũ)
        for r in range(state.size):
            for c in range(state.size):
                tile = state.get_tile(r, c)
                
                if tile.type == TileType.EMPTY or tile.type == TileType.CROSS:
                    continue
                
                rotated_tile = tile.rotate(1)
                new_state = state.set_tile(r, c, rotated_tile)
                successors.append(new_state)
    
    return successors


# ============================================================================
# HEURISTIC FUNCTIONS
# ============================================================================

def heuristic(state: PipeState) -> int:
    open_ends = count_open_ends(state)
    # Chia 2 vì mỗi kết nối giảm 2 đầu hở
    return open_ends // 2


def heuristic_simple(state: PipeState) -> int:
    return count_open_ends(state)


# ============================================================================
# SEARCH ALGORITHMS
# ============================================================================

def bfs(initial_state: PipeState):
    """BFS - Breadth-First Search"""
    if is_goal(initial_state):
        return initial_state, [initial_state], {'nodes_explored': 0, 'max_frontier_size': 1}
    
    frontier = deque([(initial_state, [initial_state])])
    visited = {initial_state}
    
    nodes_explored = 0
    max_frontier_size = 1
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        current_state, path = frontier.popleft()
        nodes_explored += 1
        
        for successor in get_successors(current_state):
            if successor not in visited:
                visited.add(successor)
                new_path = path + [successor]
                
                if is_goal(successor):
                    stats = {
                        'nodes_explored': nodes_explored,
                        'max_frontier_size': max_frontier_size,
                        'path_length': len(new_path),
                        'visited_states': len(visited)
                    }
                    return successor, new_path, stats
                
                frontier.append((successor, new_path))
    
    stats = {
        'nodes_explored': nodes_explored,
        'max_frontier_size': max_frontier_size,
        'visited_states': len(visited)
    }
    return None, None, stats


def dfs(initial_state: PipeState, max_depth: int = 1000):
    """DFS - Depth-First Search"""
    if is_goal(initial_state):
        return initial_state, [initial_state], {'nodes_explored': 0, 'max_depth': 0}
    
    frontier = [(initial_state, [initial_state], 0)]
    visited = {initial_state}
    
    nodes_explored = 0
    max_frontier_size = 1
    max_depth_reached = 0
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        current_state, path, depth = frontier.pop()
        nodes_explored += 1
        max_depth_reached = max(max_depth_reached, depth)
        
        if depth >= max_depth:
            continue
        
        for successor in get_successors(current_state):
            if successor not in visited:
                visited.add(successor)
                new_path = path + [successor]
                
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
    
    stats = {
        'nodes_explored': nodes_explored,
        'max_frontier_size': max_frontier_size,
        'visited_states': len(visited),
        'max_depth_reached': max_depth_reached
    }
    return None, None, stats


def astar(initial_state: PipeState, show_progress: bool = False):
    if is_goal(initial_state):
        return initial_state, [initial_state], {'nodes_explored': 0, 'max_frontier_size': 1}
    
    counter = 0
    g_score = 0
    h_score = heuristic(initial_state)
    f_score = g_score + h_score
    
    frontier = [(f_score, counter, g_score, initial_state, [initial_state])]
    visited = {initial_state}
    
    nodes_explored = 0
    max_frontier_size = 1
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        
        current_f, _, current_g, current_state, path = heapq.heappop(frontier)
        nodes_explored += 1
        
        # Progress indicator
        if show_progress and nodes_explored % 1000 == 0:
            print(f"\rNodes: {nodes_explored:,}, Frontier: {len(frontier):,}, h={current_f - current_g}", end="", flush=True)
        
        for successor in get_successors(current_state):
            if successor not in visited:
                visited.add(successor)
                counter += 1
                
                new_g = current_g + 1
                new_h = heuristic(successor)
                new_f = new_g + new_h
                new_path = path + [successor]
                
                if is_goal(successor):
                    if show_progress:
                        print()  # Newline
                    stats = {
                        'nodes_explored': nodes_explored,
                        'max_frontier_size': max_frontier_size,
                        'path_length': len(new_path),
                        'visited_states': len(visited),
                        'path_cost': new_g
                    }
                    return successor, new_path, stats
                
                heapq.heappush(frontier, (new_f, counter, new_g, successor, new_path))
    
    if show_progress:
        print()  # Newline
    stats = {
        'nodes_explored': nodes_explored,
        'max_frontier_size': max_frontier_size,
        'visited_states': len(visited)
    }
    return None, None, stats


def hill_climbing(initial_state: PipeState, max_iterations: int = 10000):
    if is_goal(initial_state):
        return initial_state, [initial_state], {'nodes_explored': 0, 'iterations': 0}
    
    current_state = initial_state
    path = [initial_state]
    visited = {initial_state}
    
    nodes_explored = 0
    iterations = 0
    max_successors_size = 0
    
    for iterations in range(max_iterations):
        successors = get_successors(current_state)
        unvisited_successors = [s for s in successors if s not in visited]
        
        if not unvisited_successors:
            stats = {
                'nodes_explored': nodes_explored,
                'iterations': iterations,
                'visited_states': len(visited),
                'stuck': True,
                'reason': 'No unvisited successors'
            }
            return None, path, stats
        
        max_successors_size = max(max_successors_size, len(unvisited_successors))
        
        successors_with_h = []
        for successor in unvisited_successors:
            h_value = heuristic(successor)
            successors_with_h.append((h_value, successor))
            nodes_explored += 1
            
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
        
        successors_with_h.sort(key=lambda x: x[0])
        best_h, best_successor = successors_with_h[0]
        current_h = heuristic(current_state)
        
        if best_h >= current_h:
            stats = {
                'nodes_explored': nodes_explored,
                'iterations': iterations + 1,
                'visited_states': len(visited),
                'stuck': True,
                'reason': f'Local minimum (current h={current_h}, best successor h={best_h})'
            }
            return None, path, stats
        
        current_state = best_successor
        path.append(best_successor)
        visited.add(best_successor)
    
    stats = {
        'nodes_explored': nodes_explored,
        'iterations': max_iterations,
        'visited_states': len(visited),
        'stuck': True,
        'reason': 'Max iterations reached'
    }
    return None, path, stats
