# TEST CASES SUMMARY - 7x7 PIPES WRAP PUZZLE


## Test Cases List

### DỄ (3 cases) - Giải được <10s

| # | Tên | Open ends | Thời gian | Mô tả |
|---|-----|-----------|-----------|-------|
| 1 | test01_easy_tiny | 8 | <10s | 1 box siêu nhỏ |
| 2 | test02_easy_tall | 8 | <10s | 1 box cao |
| 3 | test03_easy_frame | 6 | <10s | Frame 7x7 |

### VỪA (3 cases) - Giải được 10-60s

| # | Tên | Open ends | Thời gian | Mô tả |
|---|-----|-----------|-----------|-------|
| 5 | test05_easy_nested | 10 | 10-60s | Double frame |
| 7 | test07_medium_l_shape | 14 | 10-60s | L-shape lớn |
| 8 | test08_medium_connected | 14 | 10-60s | Connected boxes |

### KHÓ (4 cases) - Giải được 60-180s

| # | Tên | Open ends | Thời gian | Mô tả |
|---|-----|-----------|-----------|-------|
| 4 | test04_easy_two | 16 | 60-180s | 2 boxes riêng biệt |
| 6 | test06_medium_three | 16 | 60-180s | 3 boxes xa nhau |
| 10 | test10_medium_nested | 18 | 60-180s | Triple nested |
| 11 | test11_hard_five | 22 | 60-180s | 5 boxes |

### EXTREME (5 cases) - >180s hoặc timeout

| # | Tên | Open ends | Thời gian | Đặc điểm | Mô tả |
|---|-----|-----------|-----------|----------|-------|
| 9 | test09_medium_four_small | 28 | >180s | STRAIGHT+CORNER | 4 boxes |
| 12 | test12_hard_six | 28 | >180s | STRAIGHT+CORNER | 6 boxes |
| 13 | test13_hard_dense | 28 | >180s | STRAIGHT+CORNER | 8 boxes dense |
| 14 | test14_extreme_cross | 40 | TIMEOUT | **CROSS** ⚠️ | Multiple CROSS |
| 15 | test15_extreme_max | 50 | UNSOLVABLE | **CROSS** ⚠️ | Max CROSS |

---

## Detailed Summary Table

```
#    Test Name                           Difficulty   Open Ends    Est. Time           
--------------------------------------------------------------------------------
1    test01_easy_tiny                    DỄ           8            <10s                
2    test02_easy_tall                    DỄ           8            <10s                
3    test03_easy_frame                   DỄ           6            <10s                
4    test04_easy_two                     KHÓ          16           60-180s             
5    test05_easy_nested                  VỪA          10           10-60s              
6    test06_medium_three                 KHÓ          16           60-180s             
7    test07_medium_l_shape               VỪA          14           10-60s              
8    test08_medium_connected             VỪA          14           10-60s              
9    test09_medium_four_small            EXTREME      28           >180s               
10   test10_medium_nested                KHÓ          18           60-180s             
11   test11_hard_five                    KHÓ          22           60-180s             
12   test12_hard_six                     EXTREME      28           >180s               
13   test13_hard_dense                   EXTREME      28           >180s               
14   test14_extreme_cross                EXTREME      40           TIMEOUT / UNSOLVABLE
15   test15_extreme_max                  EXTREME      50           TIMEOUT / UNSOLVABLE
```

---

## Category Breakdown

| Category | Số lượng | Open ends | Giải được | Ghi chú |
|----------|----------|-----------|-----------|---------|
| **DỄ** | 3 cases | 6-8 | Có | <10s |
| **VỪA** | 3 cases | 10-14 | Có | 10-60s |
| **KHÓ** | 4 cases | 16-22 | Có | 60-180s |
| **EXTREME (không CROSS)** | 3 cases | 28 | Khó | >180s |
| **EXTREME (có CROSS)** | 2 cases | 40-50 | Không | Timeout |

**Tiles sử dụng:**
- Có CROSS/T-JUNCTION: **2 cases** (test14-15)
- Chỉ STRAIGHT + CORNER: **13 cases** (test01-13)

---

## Đề xuất sử dụng

### 1. Demo an toàn cho thầy
Chạy test01-test08 (DỄ + VỪA + 1-2 KHÓ đầu)
- Chắc chắn giải được trong <60s
- Show được các độ khó khác nhau

### 2. Nếu thầy hỏi khó hơn
Chạy test09-test13 (EXTREME không CROSS)
- Khó nhưng vẫn giải được (có thể >180s)
- Show thuật toán xử lý được case phức tạp

### 3. Chứng minh giới hạn thuật toán
Chạy test14-test15 (EXTREME với CROSS)
- Chắc chắn timeout hoặc không giải được
- Dùng để giải thích:
  - CROSS tạo branching factor khổng lồ
  - State space: 4^n với n = số open ends
  - Giới hạn của A* với heuristic admissible

---

## Lý do CROSS gây timeout

### Vấn đề với CROSS (+)

CROSS có 4 connections: [0, 1, 2, 3] (lên, phải, xuống, trái)

**Tất cả 4 rotations đều giống nhau về connections:**
- Rotation 0°: [0, 1, 2, 3]
- Rotation 90°: [1, 2, 3, 0] → sau normalize: [0, 1, 2, 3]
- Rotation 180°: [2, 3, 0, 1] → sau normalize: [0, 1, 2, 3]
- Rotation 270°: [3, 0, 1, 2] → sau normalize: [0, 1, 2, 3]

**Hậu quả:**
- Mỗi CROSS tạo ra 4 states "khác nhau" nhưng có vẻ "giống nhau"
- Thuật toán phải explore tất cả
- Với nhiều CROSS → exponential explosion
- Test14 (40 open ends): ~2^20 states cần explore
- Test15 (50 open ends): ~2^25 states → RAM overflow

---

## Files Location

```
test_inputs/
├── test01_easy_tiny.txt
├── test02_easy_tall.txt
├── test03_easy_frame.txt
├── test04_easy_two.txt
├── test05_easy_nested.txt
├── test06_medium_three.txt
├── test07_medium_l_shape.txt
├── test08_medium_connected.txt
├── test09_medium_four_small.txt
├── test10_medium_nested.txt
├── test11_hard_five.txt
├── test12_hard_six.txt
├── test13_hard_dense.txt
├── test14_extreme_cross.txt      [CROSS]
└── test15_extreme_max.txt         [CROSS]
```

---

## Chạy test

```bash
# Chạy 1 test cụ thể
python3 main.py < test_inputs/test01_easy_tiny.txt

# Chạy test comparison (so sánh các thuật toán)
python3 test_comparison.py

# Chạy test đơn giản
python3 test_simple.py
```

---

## Sample Output

### Test DỄ (test01_easy_tiny.txt)

```
================================================================================
TEST: test01_easy_tiny.txt
================================================================================

INITIAL STATE:
---------
|└─┐    |
|│ │    |
|┌─┘    |
|       |
|       |
|       |
|       |
---------

Open ends: 8
Difficulty: DỄ

[OK] SOLVED in 0.13s

Statistics:
  - Nodes explored: 268
  - Path length: 9
  - Time: 0.13s

FINAL STATE (SOLVED):
---------
|┌─└    |
|│ │    |
|┐─┘    |
|       |
|       |
|       |
|       |
---------

Final open ends: 0
```

### Test EXTREME với CROSS (test14_extreme_cross.txt)

```
================================================================================
TEST: test14_extreme_cross.txt
================================================================================

INITIAL STATE:
---------
|└─┐ └─┐|
|│┼ ││┼|
|┌─┘┌─┘│|
|└─┼ └┼┐|
|│┼ ││┼│|
|┌─┘┌─┘│|
|       |
---------

Open ends: 40
Difficulty: EXTREME

[TIMEOUT] NOT SOLVED after 600s
Nodes explored: 1,500,000+
Frontier size: >2,000,000 states
```


