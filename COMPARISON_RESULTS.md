# 📊 SO SÁNH THUẬT TOÁN TÌM KIẾM

## Bài toán: 7x7 Pipes Wrap Puzzle

Tài liệu này so sánh 4 thuật toán tìm kiếm:
- **A*** (A-star) - Informed search với heuristic
- **Hill Climbing** - Local search greedy
- **BFS** (Breadth-First Search) - Blind search optimal
- **DFS** (Depth-First Search) - Blind search nhanh

---

## 🎯 Kết quả Test

### Test 1: Đơn giản (1 màu, 5x5)

```
Trạng thái ban đầu:
A . . . A
. . . . .
. . . . .
. . . . .
. . . . .
```



**Phân tích:**
- A* và BFS cùng tìm được optimal solution (path = 25)
- A* duyệt ít node hơn BFS một chút (~0.08%)
- Hill Climbing stuck ở local minimum sau 21 bước
- DFS may mắn tìm được solution optimal với chỉ 25 nodes!

---

### Test 2: Vừa phải (2 màu, 5x5)

```
Trạng thái ban đầu:
A . . . B
. . . . .
. . . . .
. . . . .
B . . . A
```



**Phân tích:**
- A* giảm 3.4% nodes so với BFS
- Tốc độ A* và BFS tương đương (~11s vs 10s)
- Hill Climbing stuck sớm hơn (17 bước)
- DFS vẫn nhanh nhất với 5,763 nodes

---

### Test 3: Khó hơn (3 màu, 5x5)

```
Trạng thái ban đầu:
A B . C .
. . . . .
. . . . .
. . . . .
. C . B A
```



**Phân tích:**
- A* giảm 10.3% nodes so với BFS (tốt nhất!)
- Puzzle khó hơn → Heuristic giúp A* hiệu quả hơn
- Hill Climbing stuck rất sớm (7 bước)
- DFS chỉ cần 969 nodes!

---

## 📈 Tổng hợp So sánh

### 1. A* vs BFS

**So sánh Nodes:**
```
Test 1:  A* giảm 0.08%  (1,434,673 vs 1,435,809)
Test 2:  A* giảm 3.4%   (714,141 vs 739,523)
Test 3:  A* giảm 10.3%  (173,448 vs 193,290)
```

**So sánh Tốc độ:**
```
Test 1:  A* chậm hơn 1.1x  (22.77s vs 20.74s)
Test 2:  A* chậm hơn 1.1x  (11.30s vs 10.17s)
Test 3:  A* chậm hơn 1.1x  (2.49s vs 2.22s)
```

**Kết luận:**
- A* **optimal** như BFS
- A* duyệt **ít node hơn** (1-10%)
- A* **không nhanh hơn** BFS do overhead priority queue
- Càng khó, A* càng hiệu quả hơn (10% giảm nodes ở test 3)

### 2. Hill Climbing

**Kết quả:**
- **Stuck ở tất cả test cases**
- **Cực kỳ nhanh**: 0.0002-0.0004s
- **Không tìm được solution hoàn chỉnh**

**Lý do stuck:**
```
Test 1: Stuck at h=3  (local minimum)
Test 2: Stuck at h=5  (local minimum)
Test 3: Stuck at h=13 (local minimum)
```

**Giải thích:**
- Heuristic `h(n) = max(manhattan, empty_cells)` tạo **plateau**
- Nhiều states có cùng giá trị h → Hill Climbing không biết chọn
- Cần cải tiến: Random restart, Simulated Annealing, Tabu Search

### 3. DFS

**Điểm mạnh:**
- **Nhanh nhất** trong các thuật toán tìm được solution
- **May mắn tìm được optimal** trong tất cả test cases
- **Tiết kiệm bộ nhớ** (O(depth))

**Điểm yếu:**
- Không đảm bảo optimal (may mắn trong test này)
- Có thể bị stuck ở nhánh sâu vô hạn

---


##Biểu đồ So sánh

### Nodes Explored
```
Test 1:
BFS:     1,435,809
A*:      1,434,673
DFS:    25
HC:     48

Test 2:
BFS:    739,523
A*:     714,141
DFS:    5,763
HC:     37

Test 3:
BFS:    193,290
A*:     173,448
DFS:    969
HC:     17
```

### Thời gian (seconds)
```
Test 1:
A*:     22.77s
BFS:    20.74s
DFS:    0.0015s
HC:      0.0004s

Test 2:
A*:     11.30s
BFS:    10.17s
DFS:    0.04s
HC:     0.0003s

Test 3:
A*:     2.49s
BFS:    2.22s
DFS:    0.007s
HC:     0.0002s
```

---



