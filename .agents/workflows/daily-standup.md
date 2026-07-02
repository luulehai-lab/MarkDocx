---
description: Tạo báo cáo daily standup từ work_log
---

# Workflow Báo cáo Daily Standup - V2026 SSL Supreme

Workflow này dùng để tự động tổng hợp báo cáo công việc từ Work Log và Technical Debt theo chuẩn SSL.

---

## 🤖 SSL REPRESENTATION (Machine-Facing)

```json
{
  "workflow": {
    "workflow_id": "WORKFLOW_DAILY_STANDUP",
    "workflow_name": "Automated Progress Reporting",
    "workflow_goal": "Generate a concise daily progress report by synthesizing work logs and technical debt status.",
    "expected_inputs": [
      {"name": "date", "type": "string", "description": "Ngày báo cáo (YYYY-MM-DD)"}
    ],
    "constraints": [
      "Source: Must read work_log_code and work_log_task",
      "Debt: Must check docs/technical_debt.md",
      "Format: Standard Standup Template (Completed, Ongoing, Blockers, Tomorrow)"
    ],
    "entry_scene_id": "S_PREPARE"
  },
  "scenes": [
    {
      "scene_id": "S_PREPARE",
      "scene_type": "PREPARE",
      "scene_goal": "Đọc toàn bộ tệp nhật ký (Code & Task) của ngày hiện tại.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACQUIRE"}]
    },
    {
      "scene_id": "S_ACQUIRE",
      "scene_type": "ACQUIRE",
      "scene_goal": "Kiểm tra danh sách Technical Debt và các vấn đề tồn đọng từ Audit Report.",
      "next_scene_rules": [{"condition": "success", "target": "S_REASON"}]
    },
    {
      "scene_id": "S_REASON",
      "scene_type": "REASON",
      "scene_goal": "Tổng hợp: Phân loại task đã xong, đang làm, và xác định các điểm nghẽn (Blockers).",
      "next_scene_rules": [{"condition": "success", "target": "S_ACT"}]
    },
    {
      "scene_id": "S_ACT",
      "scene_type": "ACT",
      "scene_goal": "Tạo báo cáo Standup dưới định dạng bảng biểu và gửi cho Anh Lưu.",
      "next_scene_rules": [{"condition": "success", "target": "S_FINALIZE"}]
    },
    {
      "scene_id": "S_FINALIZE",
      "scene_type": "FINALIZE",
      "scene_goal": "Lưu báo cáo vào kho lưu trữ (nếu cần) và kết thúc.",
      "next_scene_rules": [{"condition": "success", "target": "END_SUCCESS"}]
    }
  ]
}
```

---

## 🎬 SCENE-LEVEL GUIDELINES

### 🛠️ Scene 1: PREPARE (Đọc nhật ký)
- [ ] Dùng `view_file` đọc `docs/work_log_code_YYYY_MM_DD.md` và `docs/work_log_task_YYYY_MM_DD.md`.

### 🛰️ Scene 2: ACQUIRE (Kiểm tra tồn đọng)
- [ ] Soi `docs/technical_debt.md` để lấy danh sách các task "Nợ".

### 🧠 Scene 3: REASON (Tổng hợp Standup)
- **Template**: BẮT BUỘC sử dụng mẫu tại `.agents/templates/tpl_daily_standup.md`.
- **Phân loại**:
    - **Done**: Những task đã hoàn thành 100%.
    - **WIP**: Những task đang dở dang kèm %.
    - **Blockers**: Các vướng mắc cần Anh Lưu quyết định.
    - **Plan**: Kế hoạch cho ngày tiếp theo.

### 💾 Scene 4: ACT (Xuất bản)
- [ ] Trình bày báo cáo đẹp mắt bằng Markdown.
- [ ] In đậm các mốc thời gian quan trọng.
