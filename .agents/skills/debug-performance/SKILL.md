---
name: Debug Performance
description: Workflow phân tích và tối ưu hiệu suất. Bao gồm profiling, memory analysis, và bottleneck identification.
---

# ⚡ Debug Performance Workflow

Sử dụng skill này khi ứng dụng chạy chậm, tiêu tốn nhiều RAM, hoặc cần tối ưu hiệu suất.

---

## Phase 1: Thu thập thông tin 📊

### 1.1 Xác định vấn đề
**Hỏi user hoặc phân tích logs:**
- [ ] Chậm ở đâu? (Startup? Specific feature? General?)
- [ ] Chậm bao lâu? (Baseline vs hiện tại)
- [ ] Xảy ra khi nào? (Luôn luôn? Sau một thời gian? Với data lớn?)

### 1.2 Baseline Measurement
```python
import time

start = time.perf_counter()
# ... code cần đo ...
elapsed = time.perf_counter() - start
print(f"Elapsed: {elapsed:.4f}s")
```

---

## Phase 2: Profiling 🔬

### 2.1 CPU Profiling (cProfile)
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# ... code cần profile ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 slow functions
```

### 2.2 Line Profiling (line_profiler)
```bash
# Install: pip install line_profiler
kernprof -l -v script.py
```

### 2.3 Memory Profiling
```python
# Install: pip install memory_profiler
from memory_profiler import profile

@profile
def memory_heavy_function():
    # ... code ...
    pass
```

---

## Phase 3: Các Pattern Thường Gặp 🎯

### 3.1 Database Bottlenecks

**Triệu chứng**: Slow với data lớn, CPU low nhưng chờ lâu

**Giải pháp**:
```python
# BAD: N+1 Query
for project in projects:
    tasks = db.query(f"SELECT * FROM tasks WHERE project_id = {project.id}")

# GOOD: Single query với JOIN hoặc IN clause
project_ids = [p.id for p in projects]
tasks = db.query("SELECT * FROM tasks WHERE project_id IN (?)", project_ids)
```

**Check indexes**:
```sql
EXPLAIN QUERY PLAN SELECT * FROM tasks WHERE project_id = 123;
```

### 3.2 Memory Leaks

**Triệu chứng**: RAM tăng dần theo thời gian

**Giải pháp**:
```python
# BAD: Accumulating in list
results = []
for item in large_dataset:
    results.append(process(item))

# GOOD: Generator/Iterator
def process_items(dataset):
    for item in dataset:
        yield process(item)
```

### 3.3 Blocking I/O

**Triệu chứng**: UI đơ, main thread blocked

**Giải pháp (PyQt6)**:
```python
from PyQt6.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    finished = pyqtSignal(object)
    
    def run(self):
        result = heavy_operation()
        self.finished.emit(result)
```

### 3.4 String Concatenation

**Triệu chứng**: Chậm khi build large strings

```python
# BAD
result = ""
for item in items:
    result += str(item)

# GOOD
result = "".join(str(item) for item in items)
```

---

## Phase 4: Optimization Strategies 🚀

### 4.1 Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(key):
    # ... complex calculation ...
    return result
```

### 4.2 Lazy Loading
```python
class LazyLoader:
    def __init__(self):
        self._data = None
    
    @property
    def data(self):
        if self._data is None:
            self._data = self._load_data()
        return self._data
```

### 4.3 Batch Processing
```python
# BAD: One-by-one
for item in items:
    db.insert(item)

# GOOD: Batch insert
db.insert_many(items)
```

---

## Phase 5: Verification ✅

### 5.1 So sánh Before/After
```python
# Ghi lại metrics
# BEFORE: 2.5s, 150MB RAM
# AFTER:  0.3s, 45MB RAM
# Improvement: 8.3x faster, 3.3x less memory
```

### 5.2 Regression Testing
```bash
# Đảm bảo optimization không break functionality
pytest tests/ -v
```

---

## Checklist Tổng Kết

- [ ] Đã xác định rõ vấn đề (slow/memory/blocking)
- [ ] Đã đo baseline
- [ ] Đã profile và tìm ra bottleneck
- [ ] Đã apply fix phù hợp
- [ ] Đã verify improvement
- [ ] Đã chạy regression tests
- [ ] Đã update `work_log_YYYY_MM_DD.md` với `[PERFORMANCE]` tag

---

## Tools Reference

| Tool | Purpose | Install |
|------|---------|---------|
| cProfile | CPU profiling (built-in) | - |
| line_profiler | Line-by-line timing | `pip install line_profiler` |
| memory_profiler | Memory usage | `pip install memory_profiler` |
| py-spy | Sampling profiler | `pip install py-spy` |
| tracemalloc | Memory tracing (built-in) | - |
