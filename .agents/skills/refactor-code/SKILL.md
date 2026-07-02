---
name: Refactor Code (SSL v2026)
description: Safe workflow for code cleanup, optimization, and technical debt resolution using the SSL (Scheduling-Structural-Logical) model.
---

<!-- 
FILE: .agents/skills/refactor-code/SKILL.md
CHANGELOG:
- 16:52:00 04/05/2026: [REFACTOR] Nâng cấp kỹ năng Refactor Code lên chuẩn SSL v2026. (Antigravity)
- 09:20:00 06/05/2026: [UPDATE] Tích hợp quy tắc Chống tuyệt vọng kỹ thuật và kỷ luật đọc Map. (Antigravity)
- 17:45:00 15/05/2026: [UPDATE] Tích hợp Kỷ luật Tự kiểm chứng (Xác minh Baseline vs New). (Antigravity)
-->

# 🛡️ Safe Refactor Workflow (SSL v2026)

Sử dụng skill này khi cải thiện chất lượng code mà không làm thay đổi hành vi bên ngoài (Input/Output). Cấu trúc SSL giúp quá trình tái cấu trúc diễn ra an toàn, có thể khôi phục (reversible) và kiểm soát rủi ro.

---

## 🤖 SSL REPRESENTATION (Machine-Facing)

```json
{
  "skill": {
    "skill_id": "SKILL_REFACTOR",
    "skill_name": "Refactor Code",
    "skill_goal": "Reorganize code for better maintainability without changing logic.",
    "expected_inputs": [
      {"name": "target_file", "type": "str", "description": "File cần refactor"},
      {"name": "strategy", "type": "str", "description": "Chiến lược (Split, Merge, Cleanup...)"}
    ],
    "constraints": [
      "No behavior change allowed",
      "Public API must remain stable",
      "Mandatory backup before execution"
    ],
    "entry_scene_id": "S_PREPARE"
  },
  "scenes": [
    {
      "scene_id": "S_PREPARE",
      "scene_type": "PREPARE",
      "scene_goal": "Tạo phao cứu sinh (Backup) và ghi nhận trạng thái gốc (Baseline).",
      "next_scene_rules": [{"condition": "success", "target": "S_ACQUIRE"}]
    },
    {
      "scene_id": "S_ACQUIRE",
      "scene_type": "ACQUIRE",
      "scene_goal": "Phân tích cấu trúc và chốt danh sách API công khai.",
      "next_scene_rules": [{"condition": "success", "target": "S_REASON"}]
    },
    {
      "scene_id": "S_REASON",
      "scene_type": "REASON",
      "scene_goal": "Lập kế hoạch điều hướng (Redirection Strategy).",
      "next_scene_rules": [{"condition": "success", "target": "S_ACT"}]
    },
    {
      "scene_id": "S_ACT",
      "scene_type": "ACT",
      "scene_goal": "Thực hiện tách/ghép và điều hướng logic.",
      "next_scene_rules": [{"condition": "success", "target": "S_VERIFY"}]
    },
    {
      "scene_id": "S_VERIFY",
      "scene_type": "VERIFY",
      "scene_goal": "Đối soát logic và chạy test suite.",
      "next_scene_rules": [{"condition": "success", "target": "S_FINALIZE"}]
    },
    {
      "scene_id": "S_FINALIZE",
      "scene_type": "FINALIZE",
      "scene_goal": "Dọn dẹp code rác và cập nhật nhật ký.",
      "next_scene_rules": [{"condition": "success", "target": "END_SUCCESS"}]
    }
  ]
}
```

---

## 🎬 SCENE-LEVEL GUIDELINES

### ✈️ Scene 1: PREPARE (Phao cứu sinh)
- **Mục tiêu**: Đảm bảo có đường lùi và hiểu vị trí trong kiến trúc tổng thể.
- **Hành động (Primitives)**: 
    - `READ` file `docs/architecture/ARCHITECTURE_MAP.md` (BẮT BUỘC).
    - `COPY` file mục tiêu sang thư mục `_backups/`.
    - `CALL_TOOL` chạy `pytest` để ghi nhận baseline test.
- **Checklist**:
    - [ ] Đã có file backup chưa?
    - [ ] Baseline test có đang PASS không?
    - [ ] Đã xác định ảnh hưởng của việc refactor đến các module xung quanh qua Map?

### 📂 Scene 2: ACQUIRE (Chốt API)
- **Mục tiêu**: Đảm bảo không làm "đứt dây" liên kết với các module khác.
- **Hành động (Primitives)**: 
    - `READ` file để xác định các hàm/class public.
    - `WRITE` ghi chú tạm thời về danh sách hàm cần bảo toàn.

### 🔀 Scene 3: REASON & ACT (Điều hướng)
- **Mục tiêu**: Thực hiện thay đổi mang tính "phẫu thuật" từng bước một. **CHỐNG TUYỆT VỌNG**.
- **Hành động (Primitives)**: 
    - `WRITE` tạo module mới (Copy code sang, chưa xóa ở file cũ).
    - `REPLACE_FILE_CONTENT` tại file cũ để chuyển hướng (Delegation) gọi sang file mới.
- **Nguyên tắc Chống tuyệt vọng**:
    - > [!IMPORTANT]
    - > **Strict Type Hints & Google Docstrings**: Bắt buộc 100% tất cả các hàm, phương thức, class mới viết, tái cấu trúc hoặc sửa đổi phải bổ sung Type Hints đầy đủ và Docstrings chuẩn Google-style.
    - > **One step at a time**: Không refactor quá nhiều thứ cùng lúc.
    - > **No Shortcuts**: Tuyệt đối không xóa code cũ khi chưa test xong code mới.
    - > **Maintain Verbatim**: Đảm bảo logic nghiệp vụ được giữ nguyên 100%.

### ✅ Scene 4: VERIFY (Đối soát logic & Tự kiểm chứng)
- **Mục tiêu**: Chứng minh 100% logic được bảo toàn.
- **Hành động (Primitives)**: 
    - **Baseline Comparison**: Chạy cùng một bộ test script trên cả bản cũ và bản mới.
    - `CALL_TOOL` dùng `diff` để so sánh bản Backup và bản hiện tại.
    - `GREP -c "def "` đối soát số lượng hàm.
    - `CALL_TOOL` chạy full test suite và so sánh với Baseline.
    - **CHỐNG LỖI HỆ THỐNG**: Chạy workflow `/check-gemini` để đảm bảo không lọt API cấm.
    - **Cập nhật Map**: Cập nhật lại `docs/architecture/ARCHITECTURE_MAP.md` với cấu trúc mới.

### 🧹 Scene 5: FINALIZE (Dọn dẹp)
- **Mục tiêu**: Làm sạch codebase.
- **Hành động (Primitives)**: 
    - `REPLACE` xóa các import/biến không còn dùng.
    - `UPDATE` Header Changelog.
    - `WRITE` nhật ký công việc vào `docs/work_log_code_YYYY_MM_DD.md`.

---

## 🚀 CÁC LỖI VẶC CẦN TRÁNH (Audit Checklist)

1.  **Circular Imports**: Tách file có gây lỗi import vòng quanh không?
2.  **Thiếu Type Hints & Google Docstrings**: Có phần code nào được tái cấu trúc, viết mới hoặc sửa đổi bị thiếu Type Hints hoặc Docstrings Google-style không? (Tuyệt đối KHÔNG được bỏ sót).
3.  **Missing References**: Đã cập nhật import cho các file khác đang gọi module này chưa?
4.  **Accidental Deletion**: Số lượng hàm sau khi tách có khớp với bản gốc không?
5.  **Behavior Change**: Input/Output có bị thay đổi dù chỉ 1 dấu cách không?
6.  **Quên Backup**: Đây là lỗi chí mạng, TUYỆT ĐỐI không được quên.
