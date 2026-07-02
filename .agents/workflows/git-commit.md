---
description: Thực hiện commit Git an toàn và đồng bộ mã nguồn theo chuẩn dự án
---
<!--
File: .agents/workflows/git-commit.md
Description: Workflow hướng dẫn và thực thi commit Git an toàn, tuân thủ kỷ luật tự kiểm chứng (Self-Testing) và cập nhật nhật ký đầy đủ.
CHANGELOG:
- 12:02:00 02/07/2026: [UPDATE] Cấu hình tự động push lên GitHub (nhánh master/main) ngay sau khi commit thành công. (Antigravity)
- 17:35:00 12/06/2026: [STRICT] Cập nhật quy trình: Bắt buộc chờ phê duyệt từ Anh Lưu sau khi anh đã test thủ công trước khi chạy lệnh Git Commit. (Antigravity)
- 15:35:00 26/05/2026: [NEW] Khởi tạo workflow git-commit an toàn cho dự án. (Antigravity)
-->

# Workflow Commit Git An Toàn (Safe Git Commit) - V2026 SSL Supreme

Workflow này đảm bảo mọi hành động lưu trữ mã nguồn vào Git đều tuân thủ nghiêm ngặt **Quy trình Git An Toàn (Safe Git Workflow)**, ngăn chặn commit code dở dang hoặc code lỗi lên nhánh chính.

---

## 🤖 SSL REPRESENTATION (Machine-Facing)

```json
{
  "workflow": {
    "workflow_id": "WORKFLOW_GIT_COMMIT",
    "workflow_name": "Safe Git Commit & Sync",
    "workflow_goal": "Commit and sync codebase changes securely only after green tests and updated logs.",
    "expected_inputs": [
      {"name": "commit_type", "type": "string", "description": "feat, fix, refactor, docs, chore, etc."},
      {"name": "commit_scope", "type": "string", "description": "Phạm vi thay đổi (ví dụ: dxf, ui, core)"},
      {"name": "commit_msg", "type": "string", "description": "Nội dung thông điệp mô tả ngắn gọn thay đổi"}
    ],
    "constraints": [
      "Green Code: Never commit code that fails tests or contains syntax errors.",
      "Type Hints & Docstrings: Required for all new/modified classes and functions.",
      "Changelog Headers: Ensure all modified files have updated changelog headers.",
      "Work Log: Work log files must be updated before committing.",
      "Map Sync: Architecture maps must be updated if new modules or paths are introduced.",
      "Auto Push: Automatically push committed code to remote GitHub repository."
    ],
    "entry_scene_id": "S_PREPARE_STATUS"
  },
  "scenes": [
    {
      "scene_id": "S_PREPARE_STATUS",
      "scene_type": "PREPARE",
      "scene_goal": "Kiểm tra trạng thái Git hiện tại để xác định danh sách tệp tin thay đổi.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACQUIRE_VERIFICATION"}]
    },
    {
      "scene_id": "S_ACQUIRE_VERIFICATION",
      "scene_type": "ACQUIRE",
      "scene_goal": "Đối soát và xác nhận các điều kiện an toàn (Green Code, Type Hints, Docs, Architecture Map).",
      "next_scene_rules": [{"condition": "success", "target": "S_REASON_MESSAGE"}]
    },
    {
      "scene_id": "S_REASON_MESSAGE",
      "scene_type": "REASON",
      "scene_goal": "Xây dựng commit message chuẩn và chuẩn bị nội dung Work Log.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACT_COMMIT"}]
    },
    {
      "scene_id": "S_ACT_COMMIT",
      "scene_type": "ACT",
      "scene_goal": "Thực hiện Git Add có chọn lọc, commit và tự động đẩy code lên GitHub repository.",
      "next_scene_rules": [{"condition": "success", "target": "S_FINALIZE_REPORT"}]
    },
    {
      "scene_id": "S_FINALIZE_REPORT",
      "scene_type": "FINALIZE",
      "scene_goal": "Hiển thị log commit cuối cùng và báo cáo trạng thái sạch sẽ cho Anh Lưu.",
      "next_scene_rules": [{"condition": "success", "target": "END_SUCCESS"}]
    }
  ]
}
```

---

## 🎬 SCENE-LEVEL GUIDELINES

### 🔍 Scene 1: PREPARE (Kiểm tra trạng thái)
- [ ] Chạy lệnh: `git status`
- [ ] Xác định các tệp tin đang ở trạng thái `Untracked` hoặc `Modified`.
- [ ] **Lọc file rác**: Đảm bảo không add các file log (`*.log`), file backup nháp (`*.bak`, `*.tmp`) hay cơ sở dữ liệu tạm thời vào index của Git. Cần bổ sung vào `.gitignore` ngay nếu phát hiện file rác ngoài danh mục.

### 🧪 Scene 2: ACQUIRE (Đối soát chất lượng & Kiểm thử)
- [ ] **Xác minh Kiểm thử (Green Code)**: 
    - Đảm bảo đã chạy test suite thành công (ví dụ: `pytest` hoặc test script tại `scratch/`).
    - *Cấm tuyệt đối commit code dở dang hoặc bị lỗi cú pháp/runtime.*
- [ ] **Xác minh Type Hints & Docstrings**: 
    - Kiểm tra xem các hàm hoặc lớp mới/được chỉnh sửa đã có đầy đủ Type hints đầu vào/kiểu trả về và Google-style docstrings chưa.
- [ ] **Xác minh Header Changelog**:
    - Mỗi tệp tin mã nguồn được sửa đổi phải được thêm dòng Changelog ở phần comment header đầu file.
- [ ] **Xác minh Bản đồ Kiến trúc (Architecture Map)**:
    - Nếu có thêm file mới hoặc thay đổi liên kết hệ thống, đảm bảo đã cập nhật `docs/architecture/ARCHITECTURE_MAP.md` hoặc các modular maps tương ứng.

### ✍️ Scene 3: REASON (Soạn thông điệp & Ghi nhật ký)
- [ ] **Viết Commit Message chuẩn**:
    - Sử dụng chuẩn Conventional Commits: `[type](scope): message`
    - Ví dụ: `feat(dxf-boq): support parsing circle geometries and export to excel`
    - Type hợp lệ: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`.
- [ ] **Cập nhật Work Log**:
    - Phải đảm bảo file nhật ký hôm nay `docs/work_log_code_YYYY_MM_DD.md` đã ghi lại chi tiết các thay đổi của task này. 
    - *Nguyên tắc cập nhật log: Đọc trước bằng view_file rồi chèn lên đầu, cấm ghi đè mất lịch sử.*

### 💾 Scene 4: ACT (Thực thi Git)
- [ ] **Manual Test & Approval (MANDATORY)**:
    - AI Agent BẮT BUỘC phải dừng lại, báo cáo mã nguồn đã hoàn thiện và yêu cầu Anh Lưu test thủ công thực tế trên ứng dụng.
    - CẤM TUYỆT ĐỐI AI tự ý chạy lệnh commit. Chỉ tiếp tục khi Anh Lưu xác nhận bằng văn bản: "OK, commit đi em" hoặc tương tự.
- [ ] **Git Add có chọn lọc**: 
    - Khuyến nghị add cụ thể các tệp tin liên quan trực tiếp: `git add file1 file2...`
    - Hạn chế `git add .` bừa bãi.
- [ ] **Git Commit**: 
    - Thực thi: `git commit -m "[commit_type]([commit_scope]): [commit_msg]"` (Chỉ thực thi khi đã có sự đồng ý rõ ràng của Anh Lưu).
- [ ] **Git Push (Tự động đồng bộ GitHub)**: 
    - Bắt buộc thực hiện đẩy mã nguồn lên GitHub ngay sau khi commit thành công để đảm bảo mã nguồn luôn được đồng bộ: `git push origin [tên-nhánh]` (ví dụ: `git push origin master` hoặc `git push origin main`).

### 🏁 Scene 5: FINALIZE (Báo cáo & Tổng hợp)
- [ ] Chạy `git log -n 1` để lấy thông tin commit vừa tạo.
- [ ] Báo cáo chi tiết commit hash và danh sách file đã commit cho Anh Lưu.
