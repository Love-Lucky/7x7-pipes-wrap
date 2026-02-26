# HƯỚNG DẪN CHẠY TEST AN TOÀN

## ⚠️ QUAN TRỌNG: Tránh tràn RAM và máy bị lag!

---

## 1. Scripts An Toàn Đã Tạo

### 1.1. `run_test_safe.py` - Chạy 1 test
```bash
python3 run_test_safe.py test_inputs/test07_medium_l_shape.txt
```

**Tính năng:**
- ✅ Tự động dừng nếu RAM > 500 MB
- ✅ Timeout sau 120 giây
- ✅ Cảnh báo khi test quá khó (>30 open ends)
- ✅ Có thể Ctrl+C để dừng

### 1.2. `run_all_tests_safe.py` - Chạy nhiều tests
```bash
python3 run_all_tests_safe.py
```

**Tính năng:**
- ✅ Chỉ chạy test01-08 (an toàn)
- ✅ Tự động SKIP test09-15 (quá khó)
- ✅ Lưu kết quả vào CSV
- ✅ Có summary cuối cùng

---

## 2. Test Cases An Toàn vs Nguy Hiểm

### ✅ AN TOÀN (Test 01-08):
```
test01-03: DỄ (6-8 open ends)
  - RAM: <10 MB
  - Time: <10s
  - Status: ✅ Rất an toàn

test04-05: VỪA (10-16 open ends)
  - RAM: 10-50 MB
  - Time: 10-60s
  - Status: ✅ An toàn

test06-08: VỪA-KHÓ (14-16 open ends)
  - RAM: 50-300 MB
  - Time: 30-120s
  - Status: ⚠️ Hơi chậm nhưng OK
```

### ⚠️ NGUY HIỂM (Test 09-13):
```
test09-13: EXTREME (28 open ends, KHÔNG CROSS)
  - RAM: 500 MB - 2 GB
  - Time: 180-600s (3-10 phút)
  - Status: ⚠️ Có thể chạy nhưng RẤT CHẬM
  - Khuyến nghị: CHỈ chạy nếu cần thiết
```

### ❌ CỰC KỲ NGUY HIỂM (Test 14-15):
```
test14-15: EXTREME với CROSS (40-50 open ends)
  - RAM: >2 GB, có thể >10 GB
  - Time: >600s hoặc không bao giờ xong
  - Status: ❌ KHÔNG NÊN CHẠY!
  - Lý do: CROSS tạo exponential explosion
```

---

## 3. Cách Monitor RAM Khi Chạy Test

### 3.1. Trên macOS/Linux:

**Terminal 1 - Chạy test:**
```bash
python3 run_test_safe.py test_inputs/test07_medium_l_shape.txt
```

**Terminal 2 - Monitor RAM:**
```bash
# Xem process Python đang dùng bao nhiêu RAM
watch -n 1 'ps aux | grep python3 | grep -v grep'

# Hoặc dùng Activity Monitor (macOS)
# Mở Activity Monitor → tìm python3 → xem Memory
```

### 3.2. Dấu hiệu nguy hiểm:

❌ **RAM tăng quá nhanh** (>100 MB/giây)
❌ **RAM > 1 GB** và vẫn tăng
❌ **Máy bắt đầu lag** (chuột chậm, switching apps chậm)
❌ **Swap memory tăng cao** (đọc/ghi disk liên tục)

**→ NGẮT NGAY LẬP TỨC bằng Ctrl+C!**

---

## 4. Cách Dừng Process An Toàn

### 4.1. Trong terminal đang chạy:
```bash
# Nhấn Ctrl+C
# Script sẽ tự động cleanup và hiển thị stats
```

### 4.2. Từ terminal khác:
```bash
# Tìm PID
ps aux | grep python3 | grep main.py

# Kill process
kill <PID>

# Nếu không stop, force kill
kill -9 <PID>
```

### 4.3. Trên macOS - Activity Monitor:
1. Mở Activity Monitor
2. Tìm process `Python` hoặc `python3`
3. Click → Quit (hoặc Force Quit nếu cần)

---

## 5. Kế Hoạch Chạy Test An Toàn

### 5.1. Giai đoạn 1 - Test DỄ (test01-03):
```bash
python3 run_all_tests_safe.py
# Chọn chỉ chạy test01-03
```

**Expected:**
- Time: <30s total
- RAM: <20 MB
- ✅ Chắc chắn OK

### 5.2. Giai đoạn 2 - Test VỪA (test04-08):
```bash
# Chạy từng test một để monitor
python3 run_test_safe.py test_inputs/test04_easy_two.txt
python3 run_test_safe.py test_inputs/test05_easy_nested.txt
...
```

**Expected:**
- Time: 10-120s per test
- RAM: 50-300 MB
- ⚠️ Monitor kỹ test07-08

### 5.3. Giai đoạn 3 - Test KHÓ (OPTIONAL):

**KHÔNG NÊN CHẠY** test09-15 trừ khi:
- Máy có RAM >8 GB
- Không có công việc quan trọng đang chạy
- Đã backup code

**Nếu muốn thử:**
```bash
# CHỈ thử 1 test, monitor RẤT KỸ
python3 run_test_safe.py test_inputs/test09_medium_four_small.txt

# Nếu thấy RAM > 500 MB hoặc >60s → CTRL+C NGAY!
```

---

## 6. Ghi Kết Quả Vào Excel

### Sau khi chạy xong:

```bash
# File CSV đã được tạo
test_results.csv
```

### Mở bằng Excel:
1. Mở Excel
2. File → Open → chọn `test_results.csv`
3. Các cột:
   - Test: Tên test case
   - Status: SOLVED / TIMEOUT / CANCELLED
   - Open_Ends: Số open ends ban đầu
   - Nodes: Số nodes explored
   - Time_s: Thời gian (giây)
   - RAM_MB: RAM peak (MB)
   - Path_Length: Độ dài solution

### Hoặc copy thủ công vào Excel:

| Test | Status | Open Ends | Nodes | Time (s) | RAM (MB) |
|------|--------|-----------|-------|----------|----------|
| test01 | SOLVED | 8 | 268 | 0.13 | 5 |
| test07 | SOLVED | 14 | 27,982 | 38.45 | 285 |
| ... | ... | ... | ... | ... | ... |

---

## 7. Khuyến Nghị Cuối Cùng

### ✅ NÊN LÀM:

1. **Chạy test01-08** - An toàn 100%
2. **Monitor RAM** khi chạy test06-08
3. **Lưu kết quả** ngay sau mỗi test
4. **Sẵn sàng Ctrl+C** nếu RAM cao
5. **Đóng apps khác** trước khi test để giải phóng RAM

### ❌ KHÔNG NÊN LÀM:

1. **Chạy test14-15** - Chắc chắn tràn RAM!
2. **Chạy nhiều tests song song** - RAM overflow
3. **Để máy không giám sát** khi chạy test khó
4. **Force quit Python** khi có thể Ctrl+C
5. **Chạy test khi đang có công việc quan trọng**

---

## 8. Xử Lý Khi Máy Bị Lag

### Nếu máy đột nhiên lag nặng:

1. **Ctrl+C ngay** trong terminal
2. Nếu không stop được:
   - macOS: Cmd+Option+Esc → Force Quit Python
   - Linux: `killall python3`
3. Nếu vẫn lag:
   - Đợi 10-20 giây (Python đang cleanup)
   - Không force shutdown máy
4. Sau khi stop:
   - Check RAM đã giải phóng chưa
   - Đóng terminal và mở lại

### Dấu hiệu cần stop ngay:

- 🔴 RAM > 80% total RAM của máy
- 🔴 Swap memory tăng nhanh
- 🔴 Fan máy chạy ầm ầm
- 🔴 Máy không respond trong >10 giây
- 🔴 Cursor di chuyển giật lag

**→ CTRL+C NGAY LẬP TỨC!**

---

## 9. Demo Cho Thầy

### Chiến lược an toàn:

**Trước buổi demo:**
1. Chạy test01-08 để có sẵn kết quả
2. Lưu output vào file hoặc screenshot
3. Ghi số liệu vào Excel

**Trong buổi demo:**
1. **KHÔNG chạy code trực tiếp** - quá nguy hiểm!
2. **Show kết quả đã chạy** từ Excel/screenshot
3. Giải thích tại sao test14-15 không chạy được
4. Nếu thầy yêu cầu chạy → chỉ chạy test01-03 (DỄ, <10s)

### Nếu bắt buộc phải chạy trực tiếp:

```bash
# CHỈ chạy test DỄ
python3 run_test_safe.py test_inputs/test01_easy_tiny.txt

# Giải trong <1s, RAM <10 MB
# An toàn 100%
```

---

## 10. Backup Plan

### Nếu test bị timeout hoặc RAM overflow:

1. **Không panic!** - Đây là expected behavior
2. **Giải thích cho thầy**:
   - Test case quá khó
   - Search space exponential
   - RAM không đủ để explore hết
   - Đây là **giới hạn của thuật toán A*** với puzzle phức tạp
3. **Show công thức** exponential complexity
4. **Đề xuất cải tiến**:
   - IDA* (Iterative Deepening)
   - Beam Search
   - Local Search
   - Parallel computing

---

**TÓM TẮT**: 

✅ **Chạy test01-08 là AN TOÀN**

⚠️ **test09-13 CẨN THẬN, có thể skip**

❌ **test14-15 TUYỆT ĐỐI KHÔNG CHẠY** (dùng để giải thích lý thuyết thôi)

Luôn sẵn sàng **Ctrl+C** khi thấy RAM cao hoặc máy lag!
