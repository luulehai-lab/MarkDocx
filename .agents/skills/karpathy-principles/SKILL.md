---
name: Karpathy Principles
description: Behavioral guidelines to reduce common LLM coding mistakes based on Andrej Karpathy's observations.
---

<!-- 
FILE: .agents/skills/karpathy-principles/SKILL.md
CHANGELOG:
- 10:20:00 06/05/2026: [UPDATE] Tích hợp quy tắc Chống tuyệt vọng kỹ thuật. (Antigravity)
-->

# 🧠 Karpathy Principles Skill

Sử dụng skill này để đối soát (checklist) trước khi submit code, đảm bảo tư duy lập trình tối ưu và hành vi an toàn.

---

## 🔍 Checklist Trước khi Code (Think Phase)
- [ ] Mình có đang **giả định** điều gì mà Anh Lưu chưa nói rõ không?
- [ ] Có phương án nào **đơn giản hơn** không?
- [ ] Nếu phương án này phức tạp, mình đã trình bày **đánh đổi (tradeoffs)** chưa?
- [ ] Mình có thực sự hiểu luồng dữ liệu hiện tại không? (Nếu không, hãy dùng `view_file` nghiên cứu thêm).

## ✂️ Checklist Trong khi Code (Surgical Phase)
- [ ] Mình có đang sửa lấn sang các hàm/file không liên quan không?
- [ ] Code mới có đang **phá vỡ style** hiện tại của file không?
- [ ] Mình có xóa đi những import/biến thừa mà mình vừa tạo ra không?
- [ ] (MANDATORY) Không refactor code cũ nếu nó không hỏng.

## 🎯 Checklist Thực thi (Goal Phase)
- [ ] Mình đã định nghĩa rõ **"Xong là như thế nào"** chưa?
- [ ] Mình đã có script hoặc lệnh để **tự kiểm chứng** chưa? (Ví dụ: `python -m py_compile`, `pytest`).

---

## 🚀 Cách áp dụng vào Implementation Plan
Thay vì viết:
1. Sửa file A
2. Sửa file B

Hãy viết theo phong cách Karpathy:
1. **Mục tiêu 1**: Thêm validation cho biến X.
   *   **Cách kiểm chứng**: Chạy test với input rỗng, mong đợi `ValueError`.
2. **Mục tiêu 2**: Refactor hàm Y để giảm độ phức tạp.
   *   **Cách kiểm chứng**: Output của hàm Y không đổi so với trước khi refactor.

---

## 🛑 Những điều CẤM (Anti-patterns)
- **Bloat**: Thêm các tham số "tùy chọn" (optional) mà Anh Lưu không yêu cầu.
- **Drive-by Refactoring**: Tiện tay sửa tên biến của người khác cho "đẹp".
- **Silent Failure**: Giấu lỗi bằng `try: ... except: pass` mà không log hoặc không hỏi ý kiến.
- **Technical Desperation**: Tuyệt đối không "vùng vẫy" khi gặp task khó. Nếu thấy code quá rối hoặc phải sửa quá nhiều, **PHẢI** dừng lại xin ý kiến thay vì đi tắt (hard-code, dùng API cấm).
