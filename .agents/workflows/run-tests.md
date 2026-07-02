---
description: Chạy test suite nhanh với auto-run annotation
---

# Workflow Chạy Kiểm thử (Run-Tests) - V2026 SSL Supreme

Workflow này cung cấp các kịch bản chạy kiểm thử tự động để đảm bảo tính ổn định của hệ thống theo chuẩn SSL.

---

## 🤖 SSL REPRESENTATION (Machine-Facing)

```json
{
  "workflow": {
    "workflow_id": "WORKFLOW_TEST_EXECUTION",
    "workflow_name": "Standard Test Suite Execution",
    "workflow_goal": "Run automated tests to verify code integrity and functional correctness.",
    "expected_inputs": [
      {"name": "test_path", "type": "string", "description": "Đường dẫn thư mục hoặc file test"}
    ],
    "constraints": [
      "Report: Must use verbose output (-v)",
      "Fail-Fast: Use --lf to re-run only last failures when debugging",
      "Coverage: Mandatory for production-ready releases"
    ],
    "entry_scene_id": "S_PREPARE"
  },
  "scenes": [
    {
      "scene_id": "S_PREPARE",
      "scene_type": "PREPARE",
      "scene_goal": "Kiểm tra sự hiện diện của thư mục tests/ và các tệp tin test liên quan.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACT"}]
    },
    {
      "scene_id": "S_ACT",
      "scene_type": "ACT",
      "scene_goal": "Thực thi bộ test bằng pytest với các cấu hình (Verbose, Coverage, Last-Failed).",
      "next_scene_rules": [{"condition": "success", "target": "S_VERIFY"}]
    },
    {
      "scene_id": "S_VERIFY",
      "scene_type": "VERIFY",
      "scene_goal": "Phân tích kết quả: Xác định tỷ lệ pass/fail và các điểm gây nghẽn.",
      "next_scene_rules": [{"condition": "success", "target": "S_FINALIZE"}]
    },
    {
      "scene_id": "S_FINALIZE",
      "scene_type": "FINALIZE",
      "scene_goal": "Báo cáo tóm tắt kết quả test và ghi nhật ký.",
      "next_scene_rules": [{"condition": "success", "target": "END_SUCCESS"}]
    }
  ]
}
```

---

## 🎬 SCENE-LEVEL GUIDELINES

### ⚙️ Scene 1: ACT (Thực thi)
// turbo
```powershell
# Chạy toàn bộ
python -m pytest tests/ -v
# Chạy lại các file bị fail
python -m pytest tests/ --lf -v
# Kiểm tra Coverage
python -m pytest tests/ --cov=. --cov-report=term-missing
```

### 🧠 Scene 2: VERIFY (Phân tích)
- [ ] Nếu có lỗi, AI phải tự động đọc log lỗi và đề xuất Fix Bug workflow.

### 🏁 Scene 3: FINALIZE (Hoàn tất)
- [ ] Ghi nhật ký: `## [TEST] Chạy kiểm thử: {Passed}/{Total} passed`.
