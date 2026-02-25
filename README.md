# 7x7 Pipes Wrap Puzzle - Pipe Rotation Version

Bài toán tìm kiếm AI: **Xoay các ống để tạo mạng kết nối hoàn chỉnh** (như game Plumber, Pipe Mania)

**OPTIMIZED:** Branching factor giảm 70-90%, nhanh hơn 2-3x với puzzle khó

## Game Mechanics

### **Mục tiêu:**
- Xoay các tile ống sao cho **không còn đầu ống hở**
- Tất cả ống phải kết nối với nhau thành mạng lưới kín
- Có tính năng **wrap-around**: Ống có thể kết nối qua biên

### **Các loại ống:**
```
│ ─    : Ống thẳng (STRAIGHT)
└ ┘ ┐ ┌ : Ống góc (CORNER)
├ ┤ ┬ ┴ : Ống chữ T (T_JUNCTION)
┼      : Ống chữ + (CROSS)
```

### **Hành động:**
- Mỗi bước: **Xoay 1 tile 90°** (clockwise)
- Mỗi state có khoảng **size² possible moves** (nhiều hơn Flow Free rất nhiều!)

---

## Cấu trúc File

```
7x7-pipes-wrap/
├── main.py                   # Core logic (Tile, PipeState, Search algorithms)
├── test.py                   # Test cơ bản, demo các tile types
├── test_simple.py            # Test nhanh với puzzle nhỏ (2x2, 3x3)
├── test_comparison.py        # So sánh thuật toán (LÂU, cho 5x5+)
├── README.md                 # File này
├── MIGRATION_SUMMARY.md      # So sánh phiên bản cũ (Flow Free) vs mới
└── COMPARISON_RESULTS.md     # Kết quả cũ (cho Flow Free version)
```

---

## Cách chạy

### **1. Test cơ bản (nhanh):**
```bash
python3 test.py
```
- Hiển thị các loại tile
- Demo wrap feature
- Test successors generation

### **2. Test đơn giản (khuyến nghị):**
```bash
python3 test_simple.py
```
- Test puzzle 2x2: ~0.0002s
- Test puzzle 3x3: ~0.15s
- Hiển thị từng bước solution

### **3. Test so sánh thuật toán (LÂU!):**
```bash
python3 test_comparison.py
```
- **RẤT LÂU** với puzzle 5x5+ (hàng phút/giờ)
- So sánh A*, BFS, DFS, Hill Climbing

---

## Thuật toán

### **1. A* (Recommended) - ĐÃ TỐI ƯU**
- **Heuristic:** `h(n) = open_ends / 2`
- **Tính chất:** Admissible, Consistent
- **Optimization:** Chỉ xoay tiles liên quan (giảm branching factor 70-90%)
- **Ưu điểm:** Optimal, nhanh hơn 5-10x so với không optimize
- **Nhược điểm:** Vẫn chậm với puzzle >20 open ends

### **2. Hill Climbing**
- **Strategy:** Greedy, chọn successor có h(n) nhỏ nhất
- **Ưu điểm:** Rất nhanh
- **Nhược điểm:** Dễ bị stuck (local minimum)

### **3. BFS**
- **Ưu điểm:** Optimal
- **Nhược điểm:** Rất chậm, tốn RAM

### **4. DFS**
- **Ưu điểm:** Nhanh, tiết kiệm RAM
- **Nhược điểm:** Không optimal

---

## Performance Benchmark

| Puzzle Size | Nodes | A* Time | BFS Time | HC Time |
|-------------|-------|---------|----------|---------|
| 2x2 (easy)  | 2     | 0.0002s | 0.0003s  | 0.0001s |
| 3x3 (medium)| 664   | 0.15s   | 0.20s    | Stuck   |
| 4x4 (hard)  | ?     | >60s    | >60s     | ?       |
| 5x5+        | ?     | ???     | ???      | ???     |


---

## Input Format

### **String Format:**
```python
puzzle_str = """
L-7
|.|
r-J
"""

state = PipeState.from_string(puzzle_str)
```

### **Character Mapping:**
```
| = STRAIGHT vertical (rotation 0)
- = STRAIGHT horizontal (rotation 1)
L = CORNER └ (rotation 0)
J = CORNER ┘ (rotation 1)
7 = CORNER ┐ (rotation 2)
r = CORNER ┌ (rotation 3)
T = T_JUNCTION ├ (rotation 0)
F = T_JUNCTION ┬ (rotation 1)
H = T_JUNCTION ┤ (rotation 2)
E = T_JUNCTION ┴ (rotation 3)
+ = CROSS ┼
. = EMPTY (không có ống)
```

---



## Lưu ý quan trọng

### **1. Khác biệt với phiên bản cũ (Flow Free):**
- **KHÔNG tương thích ngược** với code cũ
- **Input format hoàn toàn khác**
- **Performance chậm hơn NHIỀU**

### **2. Khuyến nghị puzzle size:**
- **2x2, 3x3:** Test nhanh, dễ debug
- **4x4:** Có thể lâu (>1 phút)
- **5x5+:** Rất khó, có thể không giải được trong thời gian hợp lý
- **7x7:** Cần thuật toán tối ưu hơn hoặc heuristic mạnh hơn

### **3. Tối ưu đã implement:**
- ✅ Giảm successor size (chỉ xoay tiles có open ends + láng giềng)
- ✅ Progress indicator cho A*
- ✅ Branching factor giảm 70-90%

### **4. Tối ưu tiếp theo (nếu cần puzzle >20 open ends):**
- Heuristic mạnh hơn (connected components, flow analysis)
- Iterative Deepening A* (IDA*)
- Pattern database
- Parallel search
