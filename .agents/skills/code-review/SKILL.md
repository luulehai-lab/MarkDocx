---
name: Code Review
description: Workflow kiểm tra code trước khi hoàn thành. Bao gồm Security, Performance, Best Practices.
---

<!-- 
FILE: .agents/skills/code-review/SKILL.md
CHANGELOG:
- 10:15:00 06/05/2026: [UPDATE] Tích hợp checklist Chống tuyệt vọng kỹ thuật. (Antigravity)
-->

# 🔍 Code Review Workflow

Sử dụng skill này để tự review code trước khi submit hoặc kết thúc task.

---

## 1. Security Checklist 🔐

### 1.1 Input Validation
- [ ] Tất cả user input được validate/sanitize
- [ ] Không có SQL injection risk (dùng parameterized queries)
- [ ] Không có Path traversal risk (validate file paths)

### 1.2 Secrets & Credentials
- [ ] Không hardcode passwords, API keys, tokens
- [ ] Secrets được load từ environment variables hoặc `.env`
- [ ] File `.env` đã được thêm vào `.gitignore`

### 1.3 Error Messages
- [ ] Error messages không leak thông tin nhạy cảm (stack traces, DB schema)
- [ ] User-facing errors rõ ràng nhưng không chi tiết technical

---

## 2. Performance Checklist ⚡

### 2.1 Database
- [ ] Không có N+1 query problem
- [ ] Các query lớn có LIMIT/pagination
- [ ] Indexes đã được tạo cho các cột thường xuyên filter/search

### 2.2 Memory & Resources
- [ ] Không load toàn bộ large files vào memory (dùng streaming)
- [ ] Connections/handles được close properly (dùng `with` statement)
- [ ] Không có memory leaks trong loops

### 2.3 Async & Blocking
- [ ] I/O operations không block main thread
- [ ] Heavy computations được chạy trong worker threads

---

## 3. Code Quality Checklist 📋

### 3.1 Readability
- [ ] Function names rõ ràng, mô tả action
- [ ] Variables có tên meaningful (không `x`, `temp`, `data`)
- [ ] Comments giải thích WHY, không phải WHAT

### 3.2 Maintainability
- [ ] Functions <= 50 lines (nếu dài hơn, cần split)
- [ ] Không duplicate code (DRY principle)
- [ ] Magic numbers → constants với tên rõ nghĩa

### 3.3 Error Handling
- [ ] Không có bare `except:` hoặc `except Exception:`
- [ ] Specific exceptions được catch và handle
- [ ] Đã dùng `logger.error(..., exc_info=True)`

---

## 4. Testing Checklist ✅

- [ ] Unit tests đã được viết cho logic mới
- [ ] Edge cases được cover (empty input, None, boundary values)
- [ ] Mocks được dùng cho external dependencies
- [ ] Tests pass locally: `pytest tests/`

---

## 5. Documentation Checklist 📚

- [ ] Docstrings cho public methods
- [ ] File header với CHANGELOG đã được cập nhật
- [ ] `work_log_YYYY_MM_DD.md` đã được ghi nhận

---

## Quick Commands

```bash
# Run all checks
python -m pytest tests/ -v
python -m pylint {changed_files}
python -m mypy {changed_files}

# Security scan (nếu có)
bandit -r {changed_files}
```

## 6. Anti-Technical Desperation Checklist 🛡️

### 6.1 Logic Integrity
- [ ] KHÔNG có hard-code logic nghiệp vụ (dùng config/DB).
- [ ] KHÔNG dùng Gemini API trực tiếp (phải qua Bridge).
- [ ] KHÔNG có code thừa, code "để dành cho tương lai".

### 6.2 Structural Integrity
- [ ] Đã cập nhật `ARCHITECTURE_MAP.md` và `MAP_*.md` tương ứng.
- [ ] Changelog Header đầy đủ và đúng chuẩn.
- [ ] Đã chạy `/check-gemini` để đối soát lần cuối.

---

## Khi nào PHẢI dừng lại và hỏi Human

> [!CAUTION]
> Dừng và request review nếu:
> - Có thay đổi liên quan đến authentication/authorization
> - Có thay đổi database schema
> - Có xử lý file upload/download
> - Cảm thấy đang "vùng vẫy" với code (Desperation mode)
> - Không chắc chắn về business logic
