---
description: Checklist kiểm tra trước khi deploy hoặc release
---

# Workflow Kiểm tra Triển khai (Deploy-Check) - V2026 SSL Supreme

Workflow này dùng để đảm bảo mọi bản phát hành đều đạt tiêu chuẩn Diamond (Chất lượng, Hiệu suất, Bảo mật) theo chuẩn SSL.

---

## 🤖 SSL REPRESENTATION (Machine-Facing)

```json
{
  "workflow": {
    "workflow_id": "WORKFLOW_DEPLOYMENT_CHECKLIST",
    "workflow_name": "Pre-Release Diamond Quality Audit",
    "workflow_goal": "Perform a comprehensive technical audit before any production deployment or release.",
    "expected_inputs": [],
    "constraints": [
      "Rule 61: Tmp folder must have < 10 files",
      "Diamond Architecture: All facades and handlers must be importable",
      "Testing: All core tests must pass with zero critical errors"
    ],
    "entry_scene_id": "S_PREPARE"
  },
  "scenes": [
    {
      "scene_id": "S_PREPARE",
      "scene_type": "PREPARE",
      "scene_goal": "Dọn dẹp môi trường: Xóa file rác trong tmp/ và cập nhật changelog.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACQUIRE"}]
    },
    {
      "scene_id": "S_ACQUIRE",
      "scene_type": "ACQUIRE",
      "scene_goal": "Thực thi bộ test suite và linting rà soát lỗi cú pháp.",
      "next_scene_rules": [{"condition": "success", "target": "S_REASON"}]
    },
    {
      "scene_id": "S_REASON",
      "scene_type": "REASON",
      "scene_goal": "Kiểm tra kiến trúc: Import thử các Facade chính và UI Workers.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACT"}]
    },
    {
      "scene_id": "S_ACT",
      "scene_type": "ACT",
      "scene_goal": "Chạy thử ứng dụng ở chế độ Dry-Run để xác nhận khởi động không crash.",
      "next_scene_rules": [{"condition": "success", "target": "S_FINALIZE"}]
    },
    {
      "scene_id": "S_FINALIZE",
      "scene_type": "FINALIZE",
      "scene_goal": "Báo cáo trạng thái 'Ready to Deploy' và ghi nhật ký hệ thống.",
      "next_scene_rules": [{"condition": "success", "target": "END_SUCCESS"}]
    }
  ]
}
```

---

## 🎬 SCENE-LEVEL GUIDELINES

### 🛠️ Scene 1: ACQUIRE (Kiểm tra chất lượng)
// turbo
```powershell
# Chạy bộ test
python -m pytest tests/ -v
# Kiểm tra lỗi nghiêm trọng
python -m pylint agents/ core/ ui_qt/ --rcfile=.pylintrc --errors-only
```

### 🧠 Scene 2: REASON (Kiến trúc & Anti-Bloat)
// turbo
```powershell
# Kiểm tra Diamond Architecture
python -c "import agents.agent_bridge_agent; from agents.agent_bridge_agent import AgentBridgeAgent; a=AgentBridgeAgent(); print('Bridge OK')"
# Rule 61 Check
python -c "import os; cnt=len(os.listdir('tmp')); print('Rule 61 OK') if cnt < 10 else print(f'WARNING: {cnt} files in tmp')"
```

### 💾 Scene 3: ACT (Khởi động thử)
// turbo
```powershell
python main_qt.py --dry-run
```

### 🏁 Scene 4: FINALIZE (Hoàn tất)
- [ ] Ghi nhật ký: `## [DEPLOY] Kiểm tra triển khai: {Version} - OK`.
