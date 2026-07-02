---
description: Workflow đánh giá toàn bộ codebase sử dụng các công cụ kiểm toán chất lượng tự động kết hợp phân tích kiến trúc Tech Lead.
---
<!--
File: .agents/workflows/code-audit.md
Description: Workflow đánh giá toàn bộ codebase sử dụng các công cụ kiểm toán chất lượng tự động kết hợp phân tích kiến trúc Tech Lead.
Changelog:
- 18:06:00 19/06/2026: [UPDATE] Tích hợp Radon CC, Xenon gate, Complexipy (Cognitive Complexity) vào Scene 2 + Scene 4. (Lê Thanh Vân/Antigravity)
- 17:46:00 19/06/2026: [UPDATE] Tích hợp Vulture (dead code detection) vào Scene 2 RUN_TOOLS và Scene 4 ACT. (Lê Thanh Vân/Antigravity)
- 17:00:00 19/06/2026: [UPDATE] Loại bỏ generate_codebase_graph.py khỏi workflow code-audit vì không trực tiếp quét lỗi hay chấm điểm chất lượng mã nguồn. (Lê Thanh Vân/Antigravity)
- 16:59:00 19/06/2026: [UPDATE] Bổ sung hướng dẫn ruff check và lệnh xuất báo cáo FULL vào workflow. (Lê Thanh Vân/Antigravity)
- 16:57:00 19/06/2026: [UPDATE] Bổ sung git_guard.py và doc_sync.py vào chuỗi công cụ kiểm tra gác cổng. (Lê Thanh Vân/Antigravity)
- 16:55:00 19/06/2026: [UPDATE] Tích hợp quét đồ thị liên kết hệ thống qua scripts/generate_codebase_graph.py. (Lê Thanh Vân/Antigravity)
- 10:57:00 19/06/2026: [UPDATE] Tích hợp Ruff, check_modularity.py và audit_code_quality.py vào các bước quét tự động. (Lê Thanh Vân/Antigravity)
- 13:40:00 23/04/2026: [FIX] Bổ sung YAML frontmatter để kích hoạt lệnh /code-audit. (Antigravity)
- 08:50:00 30/03/2026: [NEW] Khởi tạo workflow audit kỹ thuật hệ thống. (Antigravity)
-->

# Workflow Đánh giá Mã nguồn (Code-Audit) - V2026 SSL Supreme

Workflow này dùng để rà soát toàn bộ hệ thống bằng cách tự động chạy các công cụ kiểm soát chất lượng mã nguồn, kết hợp phân tích kiến trúc của Tech Lead nhằm tối ưu hóa tính bảo trì và độ tin cậy của codebase.

---

## 🤖 SSL REPRESENTATION (Machine-Facing)

```json
{
  "workflow": {
    "workflow_id": "WORKFLOW_CODEBASE_AUDIT",
    "workflow_name": "Technical & Architecture Audit",
    "workflow_goal": "Identify architectural weaknesses, code quality violations, and duplicate logic in the codebase.",
    "expected_inputs": [],
    "constraints": [
      "Principles: Apply Karpathy Simplicity and Surgical Integrity",
      "Tools: Run Ruff, check_modularity.py, audit_code_quality.py, git_guard.py, doc_sync.py, vulture, radon cc, xenon, complexipy",
      "Vulture: Run at confidence 80% (quick) then 60% (deep), use vulture_whitelist.py",
      "Complexity: radon cc --min C for Cyclomatic | complexipy --top 30 --plain for Cognitive | xenon as CI gate",
      "Threshold: Cyclomatic <= Grade C (max 10-25) | Cognitive <= 15 | Average CC must be Grade A/B",
      "Format: Output must be a formal Markdown report in docs/"
    ],
    "entry_scene_id": "S_PREPARE"
  },
  "scenes": [
    {
      "scene_id": "S_PREPARE",
      "scene_type": "PREPARE",
      "scene_goal": "Xác định phạm vi Audit (Toàn bộ project hoặc Module cụ thể).",
      "next_scene_rules": [{"condition": "success", "target": "S_RUN_TOOLS"}]
    },
    {
      "scene_id": "S_RUN_TOOLS",
      "scene_type": "ACT",
      "scene_goal": "Chạy tự động các công cụ kiểm soát chất lượng và gác cổng mã nguồn (Ruff, Modularity, Custom Clean Code AST Auditor, Git Guard, Doc Sync).",
      "next_scene_rules": [{"condition": "success", "target": "S_REASON"}]
    },
    {
      "scene_id": "S_REASON",
      "scene_type": "REASON",
      "scene_goal": "Phân tích nâng cao: Đánh giá database connections, trùng lặp logic thuật toán phức tạp, và AI prompt optimization.",
      "next_scene_rules": [{"condition": "success", "target": "S_ACT"}]
    },
    {
      "scene_id": "S_ACT",
      "scene_type": "ACT",
      "scene_goal": "Tạo báo cáo CODE_AUDIT_REPORT_YYYY_MM_DD.md tổng hợp điểm số tự động và Action Plan.",
      "next_scene_rules": [{"condition": "success", "target": "S_FINALIZE"}]
    },
    {
      "scene_id": "S_FINALIZE",
      "scene_type": "FINALIZE",
      "scene_goal": "Thông báo kết quả cho Anh Lưu và đề xuất phiên Refactor các file điểm thấp.",
      "next_scene_rules": [{"condition": "success", "target": "END_SUCCESS"}]
    }
  ]
}
```

---

## 🎬 SCENE-LEVEL GUIDELINES

### 🛠️ Scene 1: PREPARE (Chuẩn bị)
* Xác định phạm vi quét: toàn bộ project hoặc một module cụ thể (ví dụ: `ui_qt/widgets/contract`).

### 🏃 Scene 2: RUN_TOOLS (Chạy công cụ tự động)
Chạy các công cụ sau để lấy dữ liệu số thực chứng:
1. **Quét Modularity & Coupling**: 
   ```bash
   python scripts/check_modularity.py --scan
   ```
2. **Quét Clean Code & AST rules (Nhanh - Không check trùng lặp)**:
   ```bash
   python scripts/audit_code_quality.py --scan
   ```
3. **Quét Clean Code toàn diện (Bao gồm trùng lặp logic AST)**:
   ```bash
   python scripts/audit_code_quality.py --scan --check-dups
   ```
4. **Đồng bộ tài liệu và Kiểm tra đăng ký file mới (`MAP_TOOLS.md`)**:
   ```bash
   python scripts/doc_sync.py
   ```
5. **Chạy thử chuỗi kiểm tra gác cổng Git (Bảo mật, Modularity, Linter, Quality, Tests)**:
   ```bash
   python scripts/git_guard.py
   ```
6. **Quét lỗi style & định dạng bằng Ruff**:
   ```bash
   ruff check .
   ```
7. **Quét Dead Code bằng Vulture (Nhanh — confidence 80%)**:
   ```bash
   python -m vulture . --min-confidence 80 --exclude ".venv,scratch,docs,backups,tests,scripts"
   ```
   > Ông ý: Bước này chỉ báo các vấn đề **100% chắc chắn** như `unreachable code` và import không dùng rõ ràng.
8. **Quét Dead Code sâu bằng Vulture (Toàn diện — confidence 60%)**:
   ```bash
   python -m vulture . --min-confidence 60 --exclude ".venv,scratch,docs,backups,tests,scripts"
   ```
   > Lưu ý: ở mức 60%, kết quả sẽ có **false positive** do Qt callbacks, config constants, và abstract methods. Cần lọc thủ công hoặc đối chiếu với `vulture_whitelist.py` (nếu đã tạo).
9. **Đo Cyclomatic Complexity bằng Radon CC**:
   ```bash
    python -m radon cc . --min C --show-complexity --average -i "scripts,.venv,scratch,backups,tests"
   ```
   > Ngưỡng chuẩn: Grade A-B là an toàn. Grade C (11-25) = cần chú ý. Grade D+ = refactor ngay. Trung bình toàn dự án phải ở Grade A.
10. **Đo Cognitive Complexity bằng Complexipy (30 hàm phức tạp nhất)**:
    ```bash
    complexipy . --max-complexity-allowed 15 --ignore-complexity --plain --top 30
    ```
    > Ngưỡng chuẩn: <= 15 là an toàn (Google style). Hàm nào vượt 50 = khẩn cấp refactor.
11. **Kiểm tra Gate CI/CD bằng Xenon** (báo lỗi nếu vượt ngưỡng):
    ```bash
    python -m xenon . --max-absolute C --max-modules B --max-average A -i "scripts,.venv,scratch,backups,tests"
    ```
    > **Xenon là công cụ gate**: exit code 0 = pass, exit code 1 = fail. Dùng trong git_guard.py để block commit khi CC vượt ngưỡng.

### 🧠 Scene 3: REASON (Phân tích Tech Lead)
Kết hợp kết quả từ các công cụ trên và phân tích thủ công để phát hiện các lỗi ngầm:
* **Database**: WAL mode, Index query, kết nối Database có đóng đầy đủ qua context manager không.
* **AI & RAG**: Kiểm tra xem các API OpenAI/Gemini có bị rò rỉ gọi trực tiếp thay vì qua wrapper không.
* **Karpathy Check**: Đánh giá xem có module nào đang bị thiết kế quá phức tạp (over-engineer) không.

### 💾 Scene 4: ACT (Xuất báo cáo)
* **Xuất báo cáo định kỳ (Nhanh)**:
  Lưu kết quả quét nhanh vào tệp:
  ```powershell
  python scripts/audit_code_quality.py --scan | Out-File -Encoding utf8 docs/CODE_AUDIT_REPORT_YYYY_MM_DD.md
  ```
* **Xuất báo cáo toàn diện (FULL REPORT)**:
  Lưu kết quả quét toàn bộ (gồm trùng lặp logic AST) vào tệp:
  ```powershell
  python scripts/audit_code_quality.py --scan --check-dups | Out-File -Encoding utf8 docs/CODE_AUDIT_REPORT_FULL.md
  ```
* **Xuất báo cáo Ruff Lint**:
  Lưu kết quả quét style bằng Ruff vào tệp:
  ```powershell
  ruff check . | Out-File -Encoding utf8 docs/RUFF_AUDIT_REPORT.md
  ```
* **Xuất báo cáo Dead Code (Vulture)**:
  Lưu kết quả quét dead code vào tệp:
  ```python
  # Ghi kết quả Vulture ra file (dùng Python wrapper do PowerShell không redirect được exit code 1)
  python -c "
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'vulture', '.', '--min-confidence', '60',
    '--exclude', '.venv,scratch,docs,backups,tests,scripts'], capture_output=True)
output = result.stdout.decode('utf-8', errors='replace') + result.stderr.decode('utf-8', errors='replace')
with open('docs/VULTURE_DEAD_CODE_REPORT.md', 'w', encoding='utf-8') as f:
    f.write('# Dead Code Report (Vulture 60%)\n\n```\n' + output + '```\n')
print('Done:', len(output.splitlines()), 'issues')
"
  ```
* **Nội dung báo cáo bắt buộc**:
  * Điểm số Clean Code trung bình từ `audit_code_quality.py`.
  * Danh sách các file vi phạm Modularity (>500/800 dòng hoặc Coupling > 25).
  * Danh sách lỗi nặng (Blockers) và cảnh báo (Warnings).
  * **[MỚI] Dead Code Summary**: Tổng hợp Vulture — số `unreachable code`, `unused function/class`, top module nhiều dead code nhất.
  * Đồ thị cấu trúc codebase (liên kết hoặc tham chiếu đến [MAP_GRAPH.md](file:///d:/CloudStation/CODE/AI_ASSISTANT/ZZZ.DANG%20TEST/docs/architecture/MAP_GRAPH.md)).
  * Sơ đồ lặp logic thuật toán (AST Similarity) trong báo cáo FULL.
  * Bảng hành động (Action Plan) xếp theo thứ tự ưu tiên.

### 🏁 Scene 5: FINALIZE (Hoàn tất)
* Ghi nhật ký công việc: `## [AUDIT] Đánh giá chất lượng hệ thống: {Score}/10`.
* Đề xuất Anh Lưu cho phép refactor các tệp tin có điểm số thấp nhất.
* Đề xuất tạo `vulture_whitelist.py` để loại false positive khỏi các lần scan tiếp theo.
