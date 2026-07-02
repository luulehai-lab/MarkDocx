---
description: Kiểm tra toàn bộ codebase, xuất báo cáo và hoàn thiện Type Hints & Docstrings chuẩn Google Style theo mô hình cuốn chiếu an toàn.
---
<!--
File: .agents/workflows/type-hints-docstrings.md
Description: Workflow hướng dẫn AI tự động quét toàn bộ codebase bằng AST parser, lập báo cáo chất lượng tài liệu và hoàn thiện cuốn chiếu (incremental).
CHANGELOG:
- 17:38:00 12/06/2026: [STRICT] Cập nhật Scene 6: Bắt buộc dừng lại chờ phê duyệt từ Anh Lưu, cấm tự ý commit code. (Antigravity)
- 09:42:00 19/05/2026: [UPDATE] Nâng cấp mô hình quét vĩ mô toàn codebase và chiến lược hoàn thiện cuốn chiếu an toàn. (Antigravity)
- 09:30:00 19/05/2026: [NEW] Khởi tạo workflow kiểm tra và hoàn thiện Type Hints & Docstrings. (Antigravity)
-->

# 📝 Workflow Hoàn thiện Type Hints & Docstrings - V2026 SSL Supreme

Workflow này hướng dẫn AI thực hiện kiểm tra toàn diện chất lượng tài liệu và chú thích kiểu trên toàn bộ codebase bằng bộ công cụ phân tích tĩnh AST, xuất báo cáo tổng quan, và thực thi chiến lược hoàn thiện cuốn chiếu (Incremental Refactoring) an toàn, hiệu quả theo Master Rules.

---

## 🤖 SSL REPRESENTATION (Machine-Facing)

```json
{
  "workflow": {
    "workflow_id": "WORKFLOW_TYPE_HINTS_DOCSTRINGS_V2",
    "workflow_name": "Codebase-wide Type Hints & Docstrings Audit and Incremental Standardization",
    "workflow_goal": "Audit the entire codebase to detect missing type hints and docstrings, generate a global markdown report, and incrementally refactor files module-by-module.",
    "expected_inputs": [
      {"name": "audit_only", "type": "boolean", "description": "Nếu True, chỉ chạy quét codebase và cập nhật báo cáo mà chưa sửa code", "default": false},
      {"name": "target_module", "type": "string", "description": "Chỉ định module hoặc đường dẫn cụ thể để hoàn thiện cuốn chiếu (ví dụ: core/database)", "default": ""}
    ],
    "constraints": [
      "Macro-audit: Use tools/maintenance/audit_codebase_docs.py to get exact statistics",
      "Safety First: Banned bulk-rewriting of hundreds of files in one turn. Max 5 files per turn to avoid token explosion and compile errors",
      "Docstring Standard: Google Style (Args, Returns, Raises)",
      "Type Hints Standard: Strict (use typing or Python 3.10+ native types)"
    ],
    "entry_scene_id": "S_PREPARE"
  },
  "scenes": [
    {
      "scene_id": "S_PREPARE",
      "scene_type": "PREPARE",
      "scene_goal": "Thực thi công cụ quét tĩnh AST để kiểm kê toàn bộ codebase và cập nhật báo cáo docs/codebase_docs_audit.md.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACQUIRE"}]
    },
    {
      "scene_id": "S_ACQUIRE",
      "scene_type": "ACQUIRE",
      "scene_goal": "Phân tích file báo cáo docs/codebase_docs_audit.md để lập bản đồ thiếu sót, thống kê số liệu và trình bày lộ trình cuốn chiếu cho người dùng.",
      "next_scene_rules": [
        {"condition": "audit_only == true", "target": "S_FINALIZE"},
        {"condition": "success", "target": "S_REASON"}
      ]
    },
    {
      "scene_id": "S_REASON",
      "scene_type": "REASON",
      "scene_goal": "Chọn phân hệ/module mục tiêu (hoặc các file core quan trọng) để lên kế hoạch thiết kế Type Hints và Docstrings chi tiết.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACT"}]
    },
    {
      "scene_id": "S_ACT",
      "scene_type": "ACT",
      "scene_goal": "Cập nhật mã nguồn cuốn chiếu cho nhóm file mục tiêu bằng replace_file_content hoặc multi_replace_file_content.",
      "next_scene_rules": [{"condition": "success", "target": "S_VERIFY"}]
    },
    {
      "scene_id": "S_VERIFY",
      "scene_type": "VERIFY",
      "scene_goal": "Thực thi py_compile và suite kiểm thử để xác nhận code chạy ổn định và an toàn sau khi cập nhật.",
      "next_scene_rules": [{"condition": "success", "target": "S_FINALIZE"}]
    },
    {
      "scene_id": "S_FINALIZE",
      "scene_type": "FINALIZE",
      "scene_goal": "Cập nhật header changelog của các file đích, ghi nhận nhật ký (work_log) và commit Git các tệp tin đã hoàn thiện.",
      "next_scene_rules": [{"condition": "success", "target": "END_SUCCESS"}]
    }
  ]
}
```

---

## 🎬 SCENE-LEVEL GUIDELINES

### 🔍 Scene 1: PREPARE (Quét tĩnh codebase)
AI chạy công cụ quét tĩnh AST để phân tích toàn bộ cấu trúc dự án:
// turbo
```powershell
python tools/maintenance/audit_codebase_docs.py
```
*Lưu ý: Lệnh này tự động phân tích tất cả file `.py` trong workspace (bỏ qua `.venv`, `.git`, v.v.) và xuất báo cáo ra `docs/codebase_docs_audit.md`.*

### 📥 Scene 2: ACQUIRE (Trình bày Báo cáo & Lộ trình)
- AI đọc file [codebase_docs_audit.md](file:///d:/CloudStation/CODE/AI_ASSISTANT/ZZZ.DANG%20TEST/docs/codebase_docs_audit.md).
- Trình bày cho Anh Lưu bảng thống kê chi tiết gồm:
  - Tổng số file Python thiếu sót.
  - Tổng số lỗi (issues) tài liệu & type hint.
  - Phân tích độ ưu tiên (Priority): Các tệp core kết nối DB, API, Services được xếp hạng ưu tiên cao nhất, các tệp script nhỏ hoặc UI xếp sau.
- Đề xuất lộ trình hoàn thiện theo từng nhóm module (ví dụ: Nhóm 1: `core/database/`, Nhóm 2: `core/services/`, Nhóm 3: `agents/`...).

### 🧠 Scene 3: REASON (Thiết kế chi tiết cho module mục tiêu)
AI phân tích logic mã nguồn của nhóm file đang xử lý để thiết kế:
1. **Type Hints nghiêm ngặt**:
   - Sử dụng `Optional`, `List`, `Dict`, `Union` chuẩn từ `typing` hoặc native syntax.
   - Định dạng rõ ràng kiểu dữ liệu cho tham số đầu vào và kiểu trả về `->`.
2. **Google-Style Docstrings**:
   - Đảm bảo đầy đủ: `Summary`, `Args`, `Returns`, `Raises` (nếu có).

### 💾 Scene 4: ACT (Cập nhật cuốn chiếu - Incremental Update)
- **Quy tắc vàng**: **KHÔNG** sửa đổi hàng loạt toàn bộ codebase trong 1 lượt chạy. Chỉ tiến hành hoàn thiện cuốn chiếu tối đa **3-5 tệp tin core** trong một turn để kiểm soát chất lượng, tránh lỗi xung đột mã nguồn và token.
- Sử dụng `replace_file_content` hoặc `multi_replace_file_content` để chèn Type Hints và Docstrings mà tuyệt đối không động chạm logic chạy của code.

### 🧪 Scene 5: VERIFY (Kiểm chứng an toàn)
- Chạy kiểm tra cú pháp nhanh cho từng file vừa chỉnh sửa:
  // turbo
  ```powershell
  python -m py_compile <path_to_file>
  ```
- Chạy toàn bộ suite test bằng `/run-tests` để đảm bảo code hoạt động hoàn hảo.

### 🏁 Scene 6: FINALIZE (Ghi nhận & Báo cáo)
1. **Cập nhật Header Changelog**: Thêm dòng thay đổi vào đầu các tệp code đã hoàn thiện với tag `[DOCS]`.
2. **Cập nhật Work Log**: Ghi nhận hoạt động chi tiết vào file nhật ký `docs/work_log_code_YYYY_MM_DD.md`.
3. **Báo cáo & Chờ Duyệt (MANDATORY)**: Báo cáo danh sách file đã hoàn thiện cho Anh Lưu, hướng dẫn anh test và chờ anh ra lệnh commit. AI TUYỆT ĐỐI không được tự ý commit.
