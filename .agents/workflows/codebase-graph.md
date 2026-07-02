---
description: Công cụ phân tích cú pháp AST và truy vết tác động codebase cho AI Assistant.
---

<!--
File: .agents/workflows/codebase-graph.md
Description: Workflow tự động hóa quét codebase và truy vết tác động (Impact Analysis) cho dự án AI Assistant.
CHANGELOG:
- 17:45:00 28/05/2026: [NEW] Khởi tạo workflow codebase-graph tích hợp hiến pháp Chương 23 (Lê Thanh Vân/Antigravity)
-->

# 🌐 WORKFLOW: CODEBASE GRAPH & IMPACT ANALYSIS (AI ASSISTANT)

> [!NOTE]
> Workflow này giúp Anh Lưu và Agent dễ dàng chạy quét hệ thống và truy vết các điểm ảnh hưởng khi thay đổi logic code của AI Assistant theo đúng kỷ luật **Chương 23: Kỷ luật Codebase Graph và Phân tích tác động**.

---

## 🔄 1. Quét & Làm mới Đồ thị Codebase (Scan & Sync)

Sử dụng lệnh này sau khi thêm mới file, sửa đổi hàm, hoặc hoàn thiện một task để cập nhật lại file JSON đồ thị toàn cục và sơ đồ trực quan hóa Mermaid cho AI Assistant.

// turbo
```powershell
python scripts/generate_codebase_graph.py --scan
```

---

## 🔍 2. Truy vết Tác động (Impact Analysis)

Trước khi sửa đổi bất kỳ class hoặc hàm cốt lõi nào (ví dụ: `orchestrator.py`, `core/services/`), hãy chạy lệnh này để phát hiện toàn bộ các vị trí bị ảnh hưởng gián tiếp, phòng ngừa lỗi hồi quy.

> [!IMPORTANT]
> Thay thế `<tên_thành_phần>` bằng tên thực thể cần kiểm tra (ví dụ: `GarminService` hoặc `NetflixService.get_netflix_data`).

// turbo
```powershell
python scripts/generate_codebase_graph.py --impact <tên_thành_phần>
```

---

## 📊 3. Xuất sơ đồ Mermaid cho module cụ thể

Nếu chỉ muốn xuất sơ đồ Mermaid cho một vài module cụ thể của AI Assistant để phân tích nhanh:

// turbo
```powershell
python scripts/generate_codebase_graph.py --mermaid "core.services,ui_qt"
```
