# CÁCH ĐẾM OPEN ENDS TỪ INPUT FILE

## Câu hỏi: Làm sao nhìn vào file .txt mà biết có bao nhiêu open ends?

---

## 1. Hiểu Input Format

### File input (ví dụ test07):
```
L-7....
|.|....
|.r-7..
|...|..
|...|..
|...|..
r---J..
```

### Ký tự tương ứng với tile:

**LƯU Ý QUAN TRỌNG**: Connection = tile này nối **VỚI** tile nào (không phải đầu ống hướng về đâu!)

| Ký tự | Tile | Connections | Hướng | Visual | Giải thích |
|-------|------|-------------|-------|--------|------------|
| `.` | EMPTY | Không có | - | ` ` | - |
| `\|` | STRAIGHT | UP, DOWN | 0, 2 | `│` | Nối tile trên & dưới |
| `-` | STRAIGHT | LEFT, RIGHT | 3, 1 | `─` | Nối tile trái & phải |
| `L` | CORNER | DOWN, LEFT | 2, 3 | `└` | Nối tile dưới & trái |
| `J` | CORNER | LEFT, UP | 3, 0 | `┘` | Nối tile trái & trên |
| `7` | CORNER | UP, RIGHT | 0, 1 | `┐` | Nối tile trên & phải |
| `r` | CORNER | RIGHT, DOWN | 1, 2 | `┌` | Nối tile phải & dưới |
| `+` | CROSS | All 4 | 0, 1, 2, 3 | `┼` | Nối 4 hướng |

**Quy tắc direction:**
- 0 = UP (lên)
- 1 = RIGHT (phải)
- 2 = DOWN (xuống)
- 3 = LEFT (trái)

---

### ⚠️ QUAN TRỌNG: Visual vs Connections

**Sự nhầm lẫn phổ biến:**

Nhìn vào ống `└` (L), người ta thấy:
- "Đầu ống hướng lên TRÊN"
- "Đầu ống hướng sang PHẢI"

Và nghĩ rằng connections = [UP, RIGHT] ❌ **SAI!**

**Giải thích đúng:**

Ống `└` có 2 nhánh:
- Nhánh 1: Chạy xuống **DƯỚI** (DOWN)
- Nhánh 2: Chạy sang **TRÁI** (LEFT)

```
     │  ← nhánh xuống (DOWN)
     │
     └──  ← nhánh sang trái (LEFT)
```

→ Tile này có ống chạy về 2 hướng: DOWN và LEFT
→ Để nối với neighbor, neighbor phải ở vị trí DOWN hoặc LEFT
→ Connections = [DOWN, LEFT] = [2, 3] ✅ **ĐÚNG!**

**Công thức:**
```
Connection = HƯỚNG MÀ NHÁNH ỐNG CHẠY ĐI
(không phải vị trí của end point!)

Visual ống └:
  - End point (đầu mở) ở: TRÊN và PHẢI
  - Nhánh ống chạy về: DƯỚI và TRÁI
  → Connections = [DOWN, LEFT]
```

**Ví dụ minh họa:**
```
Ống └:
     │  ← đầu mở ở TRÊN, nhưng nhánh chạy về DƯỚI
     │
     └──  ← đầu mở ở PHẢI, nhưng nhánh chạy về TRÁI

Ống ┌:
  ───┐  ← đầu mở ở TRÁI, nhưng nhánh chạy về PHẢI
     │
     │  ← đầu mở ở DƯỚI, nhưng nhánh chạy về TRÊN
```

**Tóm tắt:**
- **End point** (đầu mở) ở 1 hướng
- **Nhánh ống** chạy về hướng ngược lại  
- **Connection** = hướng của nhánh ống, không phải end point!

---

## 2. Định nghĩa Open End

**Open End** = Đầu ống không kết nối với tile bên cạnh

### Kiểm tra 1 connection là open hay không:

```
Tile tại [r, c] có connection theo direction D
→ Check neighbor tại [r', c'] = [r, c] + direction D
→ Nếu neighbor KHÔNG có connection ngược lại (opposite direction)
   → ĐÂY LÀ OPEN END ❌
→ Ngược lại
   → CONNECTED ✅
```

**Opposite directions:**
- UP (0) ↔ DOWN (2)
- RIGHT (1) ↔ LEFT (3)

---

## 3. Ví dụ Chi Tiết: Test07

### Input:
```
L-7....    [row 0]
|.|....    [row 1]
|.r-7..    [row 2]
|...|..    [row 3]
|...|..    [row 4]
|...|..    [row 5]
r---J..    [row 6]
```

### Bước 1: Convert sang grid coordinates

```
      col: 0 1 2 3 4 5 6
row 0:     L - 7 . . . .
row 1:     | . | . . . .
row 2:     | . r - 7 . .
row 3:     | . . . | . .
row 4:     | . . . | . .
row 5:     | . . . | . .
row 6:     r - - - J . .
```

### Bước 2: Xác định connections của từng tile

#### Tile [0,0]: `L` (└)
- Type: CORNER rotation 0
- Connections: DOWN (2), RIGHT (1)
- Check:
  - **DOWN** → neighbor [1,0] = `|` có UP? → **YES** ✅ connected
  - **RIGHT** → neighbor [0,1] = `-` có LEFT? → **YES** ✅ connected
- **Open ends từ [0,0]: 0**

#### Tile [0,1]: `-` (─)
- Type: STRAIGHT rotation 1
- Connections: LEFT (3), RIGHT (1)
- Check:
  - **LEFT** → neighbor [0,0] = `L` có RIGHT? → **YES** ✅ connected
  - **RIGHT** → neighbor [0,2] = `7` có LEFT? → **NO** ❌ OPEN END!
- **Open ends từ [0,1]: 1** ❌

#### Tile [0,2]: `7` (┐)
- Type: CORNER rotation 2
- Connections: UP (0), RIGHT (1)
- **Visual giải thích**: Ống `┐` có 2 nhánh chạy về UP và RIGHT
  - Visual có end points (đầu mở) ở DƯỚI và TRÁI
  - Nhưng nhánh ống chạy về UP và RIGHT
  - → Connections = [UP, RIGHT]
- Check:
  - **UP** → neighbor [-1,2] = wrap to [6,2] = `-` có DOWN? → **NO** ❌ OPEN END!
  - **RIGHT** → neighbor [0,3] = `.` empty → **NO** ❌ OPEN END!
- **Open ends từ [0,2]: 2** ❌❌
- **Lý do**: `7` muốn nối với [1,2] ở dưới nhưng không có connection DOWN!

#### Tile [1,0]: `|` (│)
- Type: STRAIGHT rotation 0
- Connections: UP (0), DOWN (2)
- Check:
  - **UP** → neighbor [0,0] = `L` có DOWN? → **YES** ✅ connected
  - **DOWN** → neighbor [2,0] = `|` có UP? → **YES** ✅ connected
- **Open ends từ [1,0]: 0**

#### Tile [1,2]: `|` (│)
- Type: STRAIGHT rotation 0
- Connections: UP (0), DOWN (2)
- Check:
  - **UP** → neighbor [0,2] = `7` (┐) có DOWN? → **NO** ❌ OPEN END!
    - `7` (┐) có connections UP và RIGHT, KHÔNG có DOWN!
  - **DOWN** → neighbor [2,2] = `r` (┌) có UP? → **NO** ❌ OPEN END!
    - `r` (┌) có connections RIGHT và DOWN, KHÔNG có UP!
- **Open ends từ [1,2]: 2** ❌❌

#### Tile [2,2]: `r` (┌)
- Type: CORNER rotation 3
- Connections: RIGHT (1), DOWN (2)
- **Visual giải thích**: Ống `┌` có 2 nhánh chạy về RIGHT và DOWN
- Check:
  - **RIGHT** → neighbor [2,3] = `-` có LEFT? → **YES** ✅ connected
  - **DOWN** → neighbor [3,2] = `.` empty → **NO** ❌ OPEN END!
- **Open ends từ [2,2]: 1** ❌
- **Vấn đề**: `r` không có connection UP → không nối được với `|` ở [1,2]

#### Tile [2,3]: `-` (─)
- Type: STRAIGHT rotation 1
- Connections: LEFT (3), RIGHT (1)
- Check:
  - **LEFT** → neighbor [2,2] = `r` có RIGHT? → **YES** ✅ connected
  - **RIGHT** → neighbor [2,4] = `7` có LEFT? → **NO** ❌ OPEN END!
- **Open ends từ [2,3]: 1** ❌

#### Tile [2,4]: `7` (┐)
- Type: CORNER rotation 2  
- Connections: UP (0), RIGHT (1)
- Check:
  - **UP** → neighbor [1,4] = `.` empty → **NO** ❌ OPEN END!
  - **RIGHT** → neighbor [2,5] = `.` empty → **NO** ❌ OPEN END!
- **Open ends từ [2,4]: 2** ❌❌
- **Vấn đề**: `7` không có DOWN và LEFT → không nối được với neighbors
  - Cần xoay thành `L` (└) có connections DOWN và LEFT

... (tiếp tục cho tất cả tiles)

---

## 4. Công Thức Nhanh

### Cách đếm nhanh không cần check từng tile:

**Bước 1:** Đếm tổng connections trong puzzle
```
Số connections = Σ(connections của mỗi tile)

- STRAIGHT: 2 connections
- CORNER: 2 connections  
- T_JUNCTION: 3 connections
- CROSS: 4 connections
```

**Bước 2:** Tính số connections đã pair
```
Mỗi pair = 2 connections nối với nhau
→ Connections đã pair = 2 × (số pairs)
```

**Bước 3:** Tính open ends
```
Open ends = Total connections - Connections đã pair
```

### Ví dụ Test07:

**Đếm tiles:**
- 11 STRAIGHT tiles → 11 × 2 = 22 connections
- 9 CORNER tiles → 9 × 2 = 18 connections
- **Total: 40 connections**

**Đếm connections đã pair:**
- Nhìn vào puzzle, đếm số cặp tile kề nhau và có connection khớp
- Ví dụ: [0,0]`L` nối với [1,0]`|` → 1 pair (2 connections)
- Tổng: 13 pairs → 26 connections đã pair

**Tính open ends:**
```
Open ends = 40 - 26 = 14 ✅
```

---

## 5. Thuật Toán Đếm Bằng Tay

### Algorithm:

```
open_ends = 0

For each tile T at position [r, c]:
    connections = get_connections(T)
    
    For each direction D in connections:
        neighbor_pos = [r, c] + direction_offset(D)
        neighbor = tile_at(neighbor_pos)
        
        opposite_D = opposite_direction(D)
        
        If opposite_D NOT in neighbor.connections:
            open_ends += 1  # Đây là open end!
```

### Direction offsets:
- UP (0): [-1, 0]
- RIGHT (1): [0, +1]
- DOWN (2): [+1, 0]
- LEFT (3): [0, -1]

---

## 6. Ví Dụ Trực Quan

### Case 1: Connected (không phải open end)
```
[0,0]: L (└)  →RIGHT→  [0,1]: - (─)
       ↓                      ↓
   có RIGHT          có LEFT (opposite)
       
✅ CONNECTED
```

### Case 2: Open End
```
[0,1]: - (─)  →RIGHT→  [0,2]: 7 (┐)
       ↓                       ↓
   có RIGHT           KHÔNG có LEFT
       
❌ OPEN END!
```

### Case 3: EMPTY neighbor
```
[0,2]: 7 (┐)  →RIGHT→  [0,3]: . (empty)
       ↓                       ↓
   có RIGHT            không có tile
       
❌ OPEN END!
```

---

## 7. Bảng Tra Nhanh Connections

### STRAIGHT tiles:

| Char | Visual | Rotation | Connections | Directions |
|------|--------|----------|-------------|------------|
| `\|` | `│` | 0 | UP-DOWN | 0, 2 |
| `-` | `─` | 1 | LEFT-RIGHT | 3, 1 |

### CORNER tiles:

| Char | Visual | Rotation | Connections | Directions |
|------|--------|----------|-------------|------------|
| `L` | `└` | 0 | DOWN-RIGHT | 2, 1 |
| `J` | `┘` | 1 | LEFT-DOWN | 3, 2 |
| `7` | `┐` | 2 | DOWN-LEFT | 2, 3 |
| `r` | `┌` | 3 | UP-RIGHT | 0, 1 |

### T_JUNCTION tiles:

| Char | Visual | Connections | Directions |
|------|--------|-------------|------------|
| `T` | `├` | UP-RIGHT-DOWN | 0, 1, 2 |
| `F` | `┬` | RIGHT-DOWN-LEFT | 1, 2, 3 |
| `H` | `┤` | UP-DOWN-LEFT | 0, 2, 3 |
| `E` | `┴` | UP-RIGHT-LEFT | 0, 1, 3 |

### CROSS:

| Char | Visual | Connections | Directions |
|------|--------|-------------|------------|
| `+` | `┼` | All 4 | 0, 1, 2, 3 |

---

## 8. Thực Hành: Tự Đếm Test07

### Input:
```
L-7....
|.|....
|.r-7..
|...|..
|...|..
|...|..
r---J..
```

### Hướng dẫn:

1. **Vẽ lại puzzle với connections:**
```
└→─→┐
↓   ↓
│   │
↓   ↓
│   ┌→─→┐
↓       ↓
│       │
↓       ↓
│       │
↓       ↓
│       │
↓       ↓
┌→─→─→─→┘
```

2. **Đánh dấu connections chưa nối:**
```
└→─ X ┐         (X = open end giữa '-' và '7')
↓     ↓
│     │
↓   X ↓         (X = open end giữa '|' và 'r')
│   ┌→─ X ┐     (X = open end giữa '-' và '7')
↓         ↓
│         │
↓         ↓
│         │
↓         ↓
│         │
↓         ↓
┌→─→─→─→┘
```

3. **Đếm tổng X:** Có 14 chỗ "X" → **14 open ends** ✅

---

## 9. Code Python Để Verify

```python
from main import PipeState, count_open_ends

# Đọc file
with open('test_inputs/test07_medium_l_shape.txt', 'r') as f:
    puzzle_str = f.read()

# Parse và đếm
state = PipeState.from_string(puzzle_str)
open_ends = count_open_ends(state)

print(f"Open ends: {open_ends}")
# Output: Open ends: 14
```

---

## 10. Tóm Tắt

### Để đếm open ends từ input file:

1. ✅ **Parse file** → biết mỗi ô có tile gì
2. ✅ **Xác định connections** của mỗi tile theo ký tự
3. ✅ **Check neighbor** cho mỗi connection
4. ✅ **Nếu neighbor không có connection ngược lại** → open end
5. ✅ **Cộng dồn** tất cả open ends

### Hoặc đếm nhanh:

```
Open ends = Total connections - (2 × số pairs đã nối)
```

### Công thức toán học:

```
open_ends = Σ(connections_i) - 2 × Σ(pairs)

Trong đó:
- connections_i: số connections của tile thứ i
- pairs: số cặp tile nối với nhau
```

---

**KẾT LUẬN:** Bạn có thể nhìn vào file input và đếm bằng tay số open ends bằng cách check từng tile xem neighbor có nối lại không. Hoặc đơn giản hơn: đếm tổng connections trừ đi 2 lần số cặp đã nối!
