---
name: Implement Feature (SSL v2026)
description: Standardized workflow for implementing new features or complex changes using the SSL (Scheduling-Structural-Logical) model. Enforces strict adherence to project standards and Anti-Desperation rules.
---

<!-- 
FILE: .agents/skills/implement-feature/SKILL.md
CHANGELOG:
- 09:15:00 06/05/2026: [REFACTOR] Chuyển đổi sang chuẩn SSL v2026 và tích hợp quy tắc Chống tuyệt vọng kỹ thuật. (Antigravity)
- 17:45:00 15/05/2026: [UPDATE] Tích hợp Kỷ luật Tự kiểm chứng (Bắt buộc Mock Data & Test Script). (Antigravity)
-->

# ✨ Implement Feature Workflow (SSL v2026)

Sử dụng skill này khi triển khai tính năng mới hoặc thay đổi phức tạp. Quy trình này được thiết kế để duy trì sự "bình tĩnh" (Calm vector), tránh việc đi tắt gây nợ kỹ thuật.

---

## 🤖 SSL REPRESENTATION (Machine-Facing)

```json
{
  "skill": {
    "skill_id": "SKILL_IMPLEMENT_FEATURE",
    "skill_name": "Implement Feature",
    "skill_goal": "Implement new features with robust design, testing, and documentation.",
    "expected_inputs": [
      {"name": "feature_description", "type": "str", "description": "Mô tả tính năng cần làm"},
      {"name": "target_modules", "type": "list", "description": "Các module bị ảnh hưởng"}
    ],
    "entry_scene_id": "S_PREPARE"
  },
  "scenes": [
    {
      "scene_id": "S_PREPARE",
      "scene_type": "PREPARE",
      "scene_goal": "Đọc bản đồ và xác định bối cảnh kiến trúc.",
      "next_scene_rules": [{"condition": "success", "target": "S_PLAN"}]
    },
    {
      "scene_id": "S_PLAN",
      "scene_type": "PLAN",
      "scene_goal": "Lập kế hoạch thực hiện (Implementation Plan).",
      "next_scene_rules": [{"condition": "success", "target": "S_DESIGN"}]
    },
    {
      "scene_id": "S_DESIGN",
      "scene_type": "DESIGN",
      "scene_goal": "Thiết kế interface và cấu trúc dữ liệu.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACT"}]
    },
    {
      "scene_id": "S_ACT",
      "scene_type": "ACT",
      "scene_goal": "Viết code và tích hợp.",
      "next_scene_rules": [{"condition": "success", "target": "S_TEST"}]
    },
    {
      "scene_id": "S_TEST",
      "scene_type": "VERIFY",
      "scene_goal": "Viết Unit Test và kiểm tra API cấm.",
      "next_scene_rules": [{"condition": "success", "target": "S_FINALIZE"}]
    },
    {
      "scene_id": "S_FINALIZE",
      "scene_type": "FINALIZE",
      "scene_goal": "Cập nhật Maps và Work Log.",
      "next_scene_rules": [{"condition": "success", "target": "END_SUCCESS"}]
    }
  ]
}
```

---

## 🎬 SCENE-LEVEL GUIDELINES

### 🔍 Scene 1: PREPARE (Xác định bối cảnh)
- **Hành động (Primitives)**: 
    - `READ` file `docs/architecture/ARCHITECTURE_MAP.md` (BẮT BUỘC).
    - `READ` các `MAP_*.md` của module liên quan.
    - `LIST_DIR` module đích để nắm bắt cấu trúc hiện tại.
- **Checklist**:
    - [ ] Đã hiểu feature này đặt vào module nào là hợp lý nhất?
    - [ ] Có module nào hiện có đã làm việc tương tự không? (Tái sử dụng).

### 📋 Scene 2: PLAN (Lập kế hoạch)
- **Mục tiêu**: **CHỐNG TUYỆT VỌNG**. Xác định lộ trình trước khi gõ phím.
- **Hành động (Primitives)**: 
    - `WRITE` file `docs/plans/implementation_plan_{feature_name}.md`.
    - **Thiết kế Môi trường Test**: Xác định loại dữ liệu mẫu (Mock data) sẽ tạo.
    - Trình bày kế hoạch cho Anh Lưu và chờ xác nhận (nếu phức tạp).
- **Lưu ý**: Cấm nhảy vào code ngay mà không có bản phác thảo logic.

### 📐 Scene 3: DESIGN (Thiết kế Interface)
- **Mục tiêu**: Xác định các hàm, class và kiểu dữ liệu.
- **Hành động (Primitives)**: 
    - **Thiết kế Type Hints**: Bắt buộc xác định rõ kiểu dữ liệu đầu vào và đầu ra cho tất cả các class, method, hàm mới hoặc sửa đổi.
    - Thiết kế Docstrings Google-style cho cấu trúc hàm/class.
    - Thiết kế bảng database (nếu cần) qua `BaseDAO`.
    - Đảm bảo tuân thủ **Manager/Service Pattern** (Logic tách biệt UI).

### 🔧 Scene 4: ACT (Triển khai Code)
- **Hành động (Primitives)**: 
    - `WRITE_TO_FILE` / `REPLACE_FILE_CONTENT`.
- **Ràng buộc Chống tuyệt vọng**:
    - > [!IMPORTANT]
    - > **Strict Type Hints & Google Docstrings**: Bắt buộc 100% tất cả các hàm, phương thức, class mới viết hoặc được sửa đổi (dù chỉ sửa một phần nhỏ) phải bổ sung Type Hints đầy đủ và Docstrings chuẩn Google-style.
    - > **No Hard-coding**: Cấm hard-code đường dẫn, API Key, hoặc hằng số nghiệp vụ.
    - > **No Banned APIs**: Không dùng Gemini API trực tiếp. Phải dùng `Bridge`.
    - > **Header Changelog**: Bắt buộc có header changelog với tag `[NEW]`.

### ✅ Scene 5: TEST (Xác minh & Tự kiểm chứng)
- **Hành động (Primitives)**: 
    - **Create Mock Data**: Tự tạo dữ liệu mẫu (file, db records) để test.
    - **Write Test Script**: Viết `scratch/test_{feature}.py` để chạy thử trên mock data.
    - `WRITE` Unit test tại `tests/unit/test_{feature}.py`.
    - `CALL_TOOL` chạy `pytest`.
    - `CALL_TOOL` chạy workflow `/check-gemini`.
- **Checklist**:
    - [ ] Đã xử lý trường hợp `None` hoặc `Empty`?
    - [ ] Đã có logging cho các luồng lỗi?

### 📝 Scene 6: FINALIZE (Hoàn tất)
- **Hành động (Primitives)**: 
    - `UPDATE` các bản đồ kiến trúc (`ARCHITECTURE_MAP.md`, `MAP_*.md`).
    - `WRITE` vào `docs/work_log_code_YYYY_MM_DD.md`.

---

## 🚀 CÁC LỖI VẶC CẦN TRÁNH (Audit Checklist)

1.  **Lối tắt (Shortcuts)**: Có đang dùng hard-code để chạy thử cho nhanh không?
2.  **Thiếu Type Hints & Google Docstrings**: Có hàm hoặc class mới/sửa đổi nào bị thiếu Type Hints hoặc Docstrings Google-style không? (Tuyệt đối KHÔNG được bỏ sót).
3.  **Bản đồ (Maps)**: Đã cập nhật sơ đồ class/hàm mới vào file Map chưa?
4.  **Tên file**: Có tuân thủ snake_case không?
5.  **Sự cô lập**: Feature mới có làm hỏng các tính năng cũ không?
6.  **Clean Code**: Đã xóa các đoạn code thừa, comment rác chưa?
