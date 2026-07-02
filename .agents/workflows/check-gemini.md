---
description: Kiểm tra toàn bộ code (bao gồm scripts tmp) xem có gọi Gemini API trực tiếp không
---
<!--
File: .agents/workflows/check-gemini.md
Description: Workflow kiểm tra toàn bộ code để tìm các lời gọi Gemini API hoặc API Key trái phép.
Changelog:
- 08:38:00 30/03/2026: [NEW] Khởi tạo workflow kiểm tra Gemini API. (Antigravity)
- 10:35:00 30/04/2026: [UPDATE] Cho phép API Key trong app_secrets.py và các file embedding. (Antigravity)
-->



# Workflow Kiểm tra Bảo mật API (Check-Gemini) - V2026 SSL Supreme

Workflow này dùng để quét toàn bộ mã nguồn nhằm phát hiện việc sử dụng Gemini API hoặc API Key trái phép theo chuẩn SSL.

---

## 🤖 SSL REPRESENTATION (Machine-Facing)

```json
{
  "workflow": {
    "workflow_id": "WORKFLOW_GEMINI_API_AUDIT",
    "workflow_name": "API Key & Direct Call Security Audit",
    "workflow_goal": "Detect unauthorized direct Gemini API calls or hardcoded API Keys in the codebase.",
    "expected_inputs": [],
    "constraints": [
      "Exceptions: Allow API Key in app_secrets.py and embedding_utils.py only",
      "Scope: Must scan project root, tmp/, and scripts/",
      "Policy: Prefer IDE-provided models or AgentBridge for 0đ processing"
    ],
    "entry_scene_id": "S_PREPARE"
  },
  "scenes": [
    {
      "scene_id": "S_PREPARE",
      "scene_type": "PREPARE",
      "scene_goal": "Khởi động quy trình quét PowerShell trên toàn bộ cây thư mục.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACQUIRE"}]
    },
    {
      "scene_id": "S_ACQUIRE",
      "scene_type": "ACQUIRE",
      "scene_goal": "Thực thi các lệnh grep_search/PowerShell để tìm các mẫu API trái phép.",
      "next_scene_rules": [{"condition": "success", "target": "S_REASON"}]
    },
    {
      "scene_id": "S_REASON",
      "scene_type": "REASON",
      "scene_goal": "Phân tích kết quả: Loại trừ các ngoại lệ hợp lệ và xác định các điểm vi phạm.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACT"}]
    },
    {
      "scene_id": "S_ACT",
      "scene_type": "ACT",
      "scene_goal": "Báo cáo các vi phạm và yêu cầu gỡ bỏ API Key hoặc chuyển sang Bridge.",
      "next_scene_rules": [{"condition": "success", "target": "S_FINALIZE"}]
    },
    {
      "scene_id": "S_FINALIZE",
      "scene_type": "FINALIZE",
      "scene_goal": "Ghi nhật ký kiểm toán bảo mật.",
      "next_scene_rules": [{"condition": "success", "target": "END_SUCCESS"}]
    }
  ]
}
```

---

## 🎬 SCENE-LEVEL GUIDELINES

### 🛰️ Scene 1: ACQUIRE (Quét mã nguồn)
// turbo
```powershell
# Quét tìm Gemini SDK và API_KEY
Get-ChildItem -Path "." -Recurse -Include *.py, *.md, *.js, *.ipynb, *.txt -Exclude "node_modules", ".git", ".venv", "app_secrets.py", "embedding_utils.py" | Select-String -Pattern "google-generativeai", "genai\.", "Gemini", "model\.generate_content", "generative_model", "API_KEY" -CaseSensitive:$false
```

### 🧠 Scene 2: REASON (Phân tích vi phạm)
- **Hợp lệ**: API Key trong `app_secrets.py` hoặc `embedding_utils.py`.
- **Vi phạm**: API Key hardcode trong `tmp/`, `scripts/` hoặc các module tính năng.

### 💾 Scene 3: ACT (Xử lý)
- [ ] Xóa bỏ API Key vi phạm.
- [ ] Thay thế lệnh gọi trực tiếp bằng `AgentBridgeAgent` nếu cần xử lý 0đ.

### 🏁 Scene 4: FINALIZE (Hoàn tất)
- [ ] Ghi nhật ký: `## [SECURITY] Kiểm tra Gemini API: {Status}`.
