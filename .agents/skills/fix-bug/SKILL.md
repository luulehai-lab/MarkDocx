---
name: Fix Bug (SSL v2026)
description: Standardized workflow for listing, reproducing, and fixing bugs using the SSL (Scheduling-Structural-Logical) model.
---
<!-- 
FILE: .agents/skills/fix-bug/SKILL.md
CHANGELOG:
- 16:50:00 04/05/2026: [REFACTOR] Nâng cấp kỹ năng Fix Bug lên chuẩn SSL v2026 (ArXiv:2604.24026). (Antigravity)
- 09:10:00 06/05/2026: [UPDATE] Tích hợp quy tắc Chống tuyệt vọng kỹ thuật (Anti-Technical Desperation). (Antigravity)
- 17:45:00 15/05/2026: [UPDATE] Tích hợp Kỷ luật Tự kiểm chứng (Self-Testing Principle). (Antigravity)
-->

# 🐛 Fix Bug Workflow (SSL v2026)

Sử dụng skill này khi sửa lỗi hoặc xử lý behavior không mong muốn. Quy trình này được cấu trúc theo mô hình **SSL (Scheduling-Structural-Logical)** để đảm bảo tính an toàn và chính xác tuyệt đối.

---

## 🤖 SSL REPRESENTATION (Machine-Facing)

```json
{
  "skill": {
    "skill_id": "SKILL_FIX_BUG",
    "skill_name": "Fix Bug",
    "skill_goal": "Identify, reproduce, and fix software bugs with minimal side effects.",
    "expected_inputs": [
      {"name": "traceback", "type": "str", "description": "Lỗi từ console hoặc log"},
      {"name": "target_file", "type": "str", "description": "File nghi ngờ gây lỗi"},
      {"name": "conditions", "type": "str", "description": "Bối cảnh xảy ra lỗi"}
    ],
    "dependencies": [
      {"type": "capability", "value": "python_execution"},
      {"type": "permission", "value": "filesystem.read_write"}
    ],
    "control_flow_features": {
      "has_branch": true,
      "has_loop": true,
      "requires_verification": true
    },
    "entry_scene_id": "S_PREPARE"
  },
  "scenes": [
    {
      "scene_id": "S_PREPARE",
      "scene_type": "PREPARE",
      "scene_goal": "Xác định vị trí và điều kiện gây lỗi.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACQUIRE"}]
    },
    {
      "scene_id": "S_ACQUIRE",
      "scene_type": "ACQUIRE",
      "scene_goal": "Tạo môi trường tái hiện lỗi (Reproduction).",
      "next_scene_rules": [{"condition": "success", "target": "S_REASON"}]
    },
    {
      "scene_id": "S_REASON",
      "scene_type": "REASON",
      "scene_goal": "Phân tích nguyên nhân gốc rễ (Root Cause Analysis).",
      "next_scene_rules": [{"condition": "success", "target": "S_ACT"}]
    },
    {
      "scene_id": "S_ACT",
      "scene_type": "ACT",
      "scene_goal": "Thực hiện sửa lỗi tối thiểu (Surgical Fix).",
      "next_scene_rules": [{"condition": "success", "target": "S_VERIFY"}]
    },
    {
      "scene_id": "S_VERIFY",
      "scene_type": "VERIFY",
      "scene_goal": "Xác minh fix và kiểm tra lỗi tác động (Regression).",
      "next_scene_rules": [{"condition": "success", "target": "S_FINALIZE"}]
    },
    {
      "scene_id": "S_FINALIZE",
      "scene_type": "FINALIZE",
      "scene_goal": "Cập nhật nhật ký và đóng task.",
      "next_scene_rules": [{"condition": "success", "target": "END_SUCCESS"}]
    }
  ]
}
```

---

## 🎬 SCENE-LEVEL GUIDELINES

### 🔍 Scene 1: PREPARE (Xác định vị trí)

- **Mục tiêu**: Định vị chính xác dòng code "tội đồ" và hiểu bối cảnh kiến trúc.
- **Hành động (Primitives)**:
  - `READ` file `docs/architecture/ARCHITECTURE_MAP.md` (BẮT BUỘC).
  - `READ` file `docs/architecture/SYSTEM_CONVENTIONS.md` để đối soát tiền lệ fix.
  - `READ` file gây lỗi dựa trên traceback.
  - `GREP` tìm kiếm các keyword liên quan đến thông báo lỗi.
- **Checklist**:
  - [ ] Đã xác định đúng file/line từ traceback chưa?
  - [ ] Đã hiểu điều kiện (input/state) gây ra lỗi chưa?
  - [ ] Đã đọc bản đồ để tránh phá vỡ kiến trúc module?

### 🧪 Scene 2: ACQUIRE (Tạo Reproduction/Self-Testing Script)

- **Mục tiêu**: Có một script độc lập để "bấm nút là thấy lỗi". **BẮT BUỘC** sử dụng dữ liệu thực tế (Real data) hoặc Mock data sát thực tế.
- **Hành động (Primitives)**:
  - `WRITE` file `tests/reproduction/reproduce_bug_XXX.py`.
  - `CALL_TOOL` thực thi script để xác nhận lỗi xảy ra (Actual Output).
- **Mẫu Script**:

```python
def reproduce():
    # Minimal code to trigger the bug
    pass

if __name__ == "__main__":
    reproduce()
```

### 🔬 Scene 3: REASON (Phân tích Root Cause)

- **Mục tiêu**: Hiểu TẠI SAO nó lỗi, không chỉ là sửa ngọn. **CHỐNG TUYỆT VỌNG**.
- **Hành động (Primitives)**:
  - `READ` các file liên quan (nhắm mắt không sửa code).
  - Phân loại lỗi: Logic, Type, State, Permission, hay External.
  - Đối soát `docs/technical_standards.md` nếu là lỗi kỹ thuật.
- **Lưu ý Chống tuyệt vọng**:
  - > [!CAUTION]
    >
  - > Nếu thấy code quá rối, **PHẢI** dừng lại báo cáo Anh Lưu thay vì đoán mò.
    >
  - > Tuyệt đối không nghĩ đến việc hard-code để "xong việc cho nhanh".
    >

### 🛠️ Scene 4: ACT (Sửa lỗi - Safe Mode)

- **Mục tiêu**: Vá lỗi với sự xâm lấn tối thiểu nhưng cực kỳ chuẩn mực về cấu trúc.
- **Hành động (Primitives)**:
  - `REPLACE_FILE_CONTENT` đoạn code gây lỗi.
- **Constraints (Ràng buộc)**:
  - [!IMPORTANT]
  - **Surgical Fix**: Chỉ sửa đúng chỗ lỗi. Cấm refactor lan man xung quanh.
  - **Strict Type Hints & Google Docstrings**: Bắt buộc bổ sung đầy đủ Type Hints cho các đối số/kiểu trả về và Google-style Docstrings cho bất kỳ hàm, phương thức nào được chỉnh sửa hoặc tạo mới để vá lỗi. Cấm sửa code mà để lại hàm "mồ côi" không có mô tả/kiểu dữ liệu.
  - **One bug per fix**: Không tiện tay sửa thêm cái khác.

### ✅ Scene 5: VERIFY (Xác minh & Regression)

- **Mục tiêu**: Đảm bảo lỗi đã hết và không đẻ ra lỗi mới.
- **Hành động (Primitives)**:
  - `CALL_TOOL` chạy lại Reproduction Script (Kết quả phải PASS).
  - `CALL_TOOL` chạy `pytest` cho toàn bộ module liên quan.
  - **CHỐNG LỖI HỆ THỐNG**: Chạy workflow `/check-gemini` để đảm bảo không lọt API cấm.
- **Checklist**:
  - [ ] Lỗi cũ đã hết? (Xác minh bằng script tại Scene 2).
  - [ ] Đã có dữ liệu mẫu (Mock data) để Anh Lưu tự kiểm chứng chưa?
  - [ ] Các tính năng cũ không hỏng?
  - [ ] Test các trường hợp biên (None, Empty, Boundary)?
  - [ ] Đã cập nhật Bản đồ kiến trúc (nếu fix làm thay đổi logic chính)?

### 📝 Scene 6: FINALIZE (Hoàn tất)

- **Mục tiêu**: Ghi lại lịch sử để Anh Lưu và đội ngũ nắm bắt.
- **Hành động (Primitives)**:
  - `UPDATE` Header Changelog trong file code.
  - `WRITE` (Append) vào `docs/work_log_code_YYYY_MM_DD.md`.

---

## 🚀 CÁC LỖI VẶC CẦN TRÁNH (Audit Checklist)

1. **Over-engineering**: Đã đảm bảo fix tối thiểu chưa?
2. **Thiếu Type Hints & Google Docstrings**: Có hàm hoặc class được sửa đổi/viết mới nào bị thiếu Type Hints hoặc Docstrings chuẩn Google không? (Tuyệt đối KHÔNG được bỏ sót).
3. **Chết yểu Fix**: Đã thực sự chạy script tái hiện lỗi sau khi fix chưa?
4. **Hardcode**: Có đang dùng "băng keo cá nhân" (hardcode) để vá lỗi không?
5. **Traceback**: Còn dòng `print()` nào sót lại không?
6. **Type Safety**: Đã thêm kiểm tra `is None` cho các biến rủi ro chưa?
