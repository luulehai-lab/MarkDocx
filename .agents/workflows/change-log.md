---
description: Cập nhật header changelog cho các file đã sửa code
---
<!--
File: .agents/workflows/change-log.md
Description: Workflow hỗ trợ AI tự động cập nhật header Changelog cho các file code đã chỉnh sửa.
Changelog:
- 09:40:00 26/03/2026: [NEW] Khởi tạo workflow cập nhật Changelog file header. (Antigravity)
-->

# Workflow Cập nhật Header (Change-Log) - V2026 SSL Supreme

Workflow này đảm bảo mọi tệp tin mã nguồn đều có header Changelog đầy đủ và chính xác theo chuẩn SSL.

---

## 🤖 SSL REPRESENTATION (Machine-Facing)

```json
{
  "workflow": {
    "workflow_id": "WORKFLOW_CHANGELOG_HEADER_UPDATE",
    "workflow_name": "Source File Header Synchronization",
    "workflow_goal": "Ensure all modified files have a standard header with accurate changelog entries.",
    "expected_inputs": [
      {"name": "modified_files", "type": "list", "description": "Danh sách file đã sửa"}
    ],
    "constraints": [
      "Order: Newest entries must be at the top of the changelog",
      "Format: Python use #, Markdown use <!-- -->",
      "Tags: Only use [NEW], [FIX], [UPDATE], [REFACTOR], [DOCS], [UI]"
    ],
    "entry_scene_id": "S_PREPARE"
  },
  "scenes": [
    {
      "scene_id": "S_PREPARE",
      "scene_type": "PREPARE",
      "scene_goal": "Liệt kê danh sách tệp tin đã chỉnh sửa trong phiên làm việc hiện tại.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACQUIRE"}]
    },
    {
      "scene_id": "S_ACQUIRE",
      "scene_type": "ACQUIRE",
      "scene_goal": "Đọc nội dung hiện tại của từng tệp tin để kiểm tra cấu trúc header.",
      "next_scene_rules": [{"condition": "success", "target": "S_REASON"}]
    },
    {
      "scene_id": "S_REASON",
      "scene_type": "REASON",
      "scene_goal": "Soạn thảo nội dung thay đổi súc tích và chọn Tag phù hợp.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACT"}]
    },
    {
      "scene_id": "S_ACT",
      "scene_type": "ACT",
      "scene_goal": "Thực thi ghi đè/cập nhật header cho từng tệp tin bằng replace_file_content.",
      "next_scene_rules": [{"condition": "success", "target": "S_FINALIZE"}]
    },
    {
      "scene_id": "S_FINALIZE",
      "scene_type": "FINALIZE",
      "scene_goal": "Thông báo danh sách file đã cập nhật header thành công.",
      "next_scene_rules": [{"condition": "success", "target": "END_SUCCESS"}]
    }
  ]
}
```

---

## 🎬 SCENE-LEVEL GUIDELINES

### 🛠️ Scene 1: PREPARE (Kiểm kê)
- [ ] Xác định các file đã thực thi `write_to_file` hoặc `replace_file_content`.

### 🧠 Scene 2: REASON (Soạn thảo)
- **Cấu trúc Log**: `HH:MM:SS DD/MM/YYYY: [TAG] [Mô tả] (Antigravity)`.
- **Mẫu Header**:
    - **Python**: `# Tên file: / CHỨC NĂNG: / CHANGELOG:`.
    - **Markdown**: `<!-- File: / Description: / Changelog: -->`.

### 💾 Scene 3: ACT (Thực thi)
- [ ] Chèn nội dung mới lên đầu danh sách CHANGELOG.
- [ ] Bảo toàn nội dung cũ phía dưới.

### 🏁 Scene 4: FINALIZE (Hoàn tất)
- [ ] Báo cáo: "Đã cập nhật header cho X tệp tin".

