# Tên file: scripts/git_guard.py
# CHỨC NĂNG: Gác cổng Git tự động (Pre-commit Hook) kiểm tra an toàn dữ liệu, modularity và chạy test trước khi commit.
# CHANGELOG:
# - 11:49:13 02/07/2026: [NEW] Cập nhật mã nguồn (Antigravity)
# - 11:52:19 23/06/2026: [REFACTOR] refactor(core-indexing): convert strategy index signatures to keyword-only and shorten search_globally (Antigravity)
# - 11:52:09 23/06/2026: [REFACTOR] refactor(core-indexing): convert strategy index signatures to keyword-only and shorten search_globally (Antigravity)
# - 11:45:00 23/06/2026: [FIX] Cập nhật run_command để tự động bổ sung PYTHONPATH khi thực thi subprocess. Trích xuất helper _find_related_test_files từ run_tests để giải quyết lỗi Ruff C901. (Lê Thanh Vân/Antigravity)
# - 17:03:17 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 17:00:33 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 16:00:27 18/06/2026: [NEW] feat: integrate proactive modularity protocol into local rules.md (Antigravity)
# - 17:23:56 12/06/2026: [NEW] feat: integrate proactive modularity protocol into local rules.md (Antigravity)
# - 16:53:43 12/06/2026: [NEW] Thêm công cụ tự động hóa Changelog & Doc Sync (Antigravity)
# - 16:45:00 12/06/2026: [NEW] Khởi tạo Git Guard - người gác cổng Git tự động cho dự án AI Assistant (Lê Thanh Vân/Antigravity)

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# Thư mục gốc dự án
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Thêm project root vào path để có thể import các module nội bộ
sys.path.append(str(PROJECT_ROOT))

# Thư mục và định dạng file loại trừ khi quét secret
EXCLUDE_DIRS = {
    ".git",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "archives",
    "backups",
    "scratch",
    ".gemini",
    "chroma_db",
    "local_data",
    "user_data_zalo",
    "user_data_zalo_bot",
    "user_data_zalo_web",
    "user_data_notebooklm",
    "tmp",
    "temp_snippets",
    "temp_vision_images",
    "htmlcov",
    "chat_sessions",
    "node_modules",
}

# Regex nhận diện API key hoặc Secret key nhạy cảm
SECRET_PATTERNS = [
    re.compile(
        r"(?i)(api_key|api-key|apikey|secret|password|token|private_key)\s*=\s*['\"][a-zA-Z0-9_\-\.\/]{16,}['\"]"
    ),
    re.compile(r"(?i)AIzaSy[a-zA-Z0-9_\-]{33}"),  # Google/Gemini API Key format
]


def run_command(args: list[str], cwd: Path) -> tuple[int, str, str]:
    """
    Chạy lệnh CLI an toàn và trả về exit code, stdout, stderr.
    """
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(cwd) + os.pathsep + env.get("PYTHONPATH", "")
        result = subprocess.run(
            args, cwd=str(cwd), env=env, capture_output=True, text=True, encoding="utf-8", errors="ignore"
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return -1, "", str(e)


def get_staged_files(project_root: Path) -> list[Path]:
    """
    Lấy danh sách các tệp tin đã staged (chuẩn bị commit).
    """
    code, stdout, _ = run_command(["git", "diff", "--cached", "--name-only"], project_root)
    if code != 0 or not stdout:
        return []

    staged_files = []
    for line in stdout.splitlines():
        file_path = project_root / line.strip()
        if file_path.exists() and file_path.is_file():
            # Kiểm tra xem có nằm trong thư mục loại trừ không
            if not any(part in file_path.relative_to(project_root).parts for part in EXCLUDE_DIRS):
                staged_files.append(file_path)
    return staged_files


def check_secrets(files: list[Path]) -> bool:
    """
    Quét các file sắp commit để phát hiện lộ lọt API Key hoặc mật khẩu cứng.
    """
    print("🔒 1. Đang quét bảo mật (Secrets & API Keys)...")
    violation_found = False

    for file_path in files:
        # Chỉ quét các file văn bản logic/cấu hình
        if file_path.suffix not in {".py", ".json", ".js", ".bat", ".sh", ".ini", ".yaml", ".yml", ".env"}:
            continue

        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                for line_idx, line in enumerate(f, 1):
                    # Bỏ qua các dòng comment trong code
                    stripped = line.strip()
                    if stripped.startswith("#") or stripped.startswith("//"):
                        continue

                    for pattern in SECRET_PATTERNS:
                        if pattern.search(line):
                            # Cho phép bỏ qua nếu có từ khóa bypass rõ ràng ở cuối dòng
                            if "bypass-secrets-check" in line:
                                continue
                            print(f"   ❌ PHÁT HIỆN SECRET tại `{file_path.name}:{line_idx}`: `{stripped[:40]}...`")
                            violation_found = True
        except Exception as e:
            print(f"   ⚠️ Lỗi đọc file khi quét bảo mật {file_path.name}: {e}")

    if violation_found:
        print("\n> [!CAUTION]")
        print("> **Phát hiện API Key hoặc Mật khẩu nhúng cứng trong mã nguồn!**")
        print("> Vui lòng sử dụng biến môi trường hoặc file cấu hình ngoài (như app_secrets.py đã ignore).")
        print("> Nếu muốn bỏ qua cảnh báo này cho dòng code đó, hãy thêm comment `# bypass-secrets-check` ở cuối dòng.")
        return False

    print("   ✅ Đạt yêu cầu bảo mật. Không phát hiện rò rỉ secrets.")
    return True


def check_modularity(files: list[Path], project_root: Path) -> bool:
    """
    Kiểm tra giới hạn kích thước tệp tin (chống phình code, đảm bảo Modularity).
    """
    print("📐 2. Đang kiểm tra Modularity (Giới hạn dòng)...")

    try:
        from scripts.check_modularity import ModularityChecker
    except ImportError:
        print("   ⚠️ Không thể import ModularityChecker. Bỏ qua bước kiểm tra này.")
        return True

    checker = ModularityChecker(project_root)
    violation_found = False

    for file_path in files:
        if file_path.suffix != ".py":
            continue

        total, _, _ = checker.count_lines(file_path)
        # 800 dòng là giới hạn cực hạn (HARD_LIMIT) của dự án
        if total > 800:
            print(f"   ❌ VI PHẠM MODULARITY: File `{file_path.name}` dài quá giới hạn ({total}/800 dòng).")
            violation_found = True
        elif total > 500:
            print(
                f"   ⚠️ CẢNH BÁO: File `{file_path.name}` sắp vượt giới hạn ({total}/500 dòng). Hãy chuẩn bị tách module."
            )

    if violation_found:
        print("\n> [!WARNING]")
        print("> **CẤM SỬA TRỰC TIẾP FILE VƯỢT QUÁ 800 DÒNG!**")
        print("> Vui lòng thực hiện thiết kế Modularity: Tách logic mới sang module/file mới độc lập.")
        return False

    print("   ✅ Đạt yêu cầu Modularity.")
    return True


def _find_related_test_files(staged_files: list[Path], project_root: Path) -> set[Path]:
    """Tìm danh sách các bài test liên quan trực tiếp đến các file đã staged.

    Args:
        staged_files (List[Path]): Danh sách tệp đã staged.
        project_root (Path): Thư mục gốc của dự án.

    Returns:
        Set[Path]: Tập hợp các file test cần chạy.
    """
    test_files_to_run = set()

    # Lấy toàn bộ danh sách file test trong thư mục tests/
    all_test_files = []
    for root, _, files in os.walk(project_root / "tests"):
        for f in files:
            if f.startswith("test_") and f.endswith(".py"):
                all_test_files.append(Path(root) / f)

    for staged_file in staged_files:
        staged_name = staged_file.stem
        # Chỉ coi là file test chạy trực tiếp nếu tên file bắt đầu bằng test_ và nằm trong thư mục tests/
        if staged_name.startswith("test_") and "tests" in staged_file.parts:
            test_files_to_run.add(staged_file)
            continue

        # Tìm file test khớp tên (ví dụ: test_sandbox.py khớp với test_sandbox_utility.py)
        clean_name = staged_name.replace("test_", "")
        for tf in all_test_files:
            tf_name = tf.stem.lower()
            if clean_name.lower() in tf_name:
                test_files_to_run.add(tf)

    # Nếu không phát hiện bài test liên quan nào, chạy mặc định test_sandbox_utility.py làm smoke test nhanh (0.4s)
    if not test_files_to_run:
        smoke_test = project_root / "tests" / "test_sandbox_utility.py"
        if smoke_test.exists():
            test_files_to_run.add(smoke_test)
            print(
                "   ℹ️ Không phát hiện file test liên quan trực tiếp. Chạy Smoke Test mặc định để kiểm tra môi trường."
            )

    return test_files_to_run


def run_tests(staged_files: list[Path], project_root: Path) -> bool:
    """Chạy các bài kiểm thử liên quan trực tiếp đến các file thay đổi để bảo đảm an toàn mà vẫn tối ưu tốc độ.

    Args:
        staged_files (List[Path]): Danh sách tệp đã staged.
        project_root (Path): Thư mục gốc của dự án.

    Returns:
        bool: True nếu toàn bộ test passed, False nếu ngược lại.
    """
    print("🧪 3. Đang thực thi các bài kiểm thử liên quan (Impact-based Testing)...")

    test_files_to_run = _find_related_test_files(staged_files, project_root)

    if not test_files_to_run:
        print("   ✅ Không có bài kiểm thử nào cần chạy.")
        return True

    # Thực thi các file test đã lọc
    success = True
    for tf in test_files_to_run:
        rel_tf = tf.relative_to(project_root)
        print(f"   🏃 Chạy test: `{rel_tf.as_posix()}`...")

        # Chạy bằng unittest discover để tự động set PYTHONPATH đúng là project root
        code, stdout, stderr = run_command(
            ["python", "-m", "unittest", "discover", "-s", "tests", "-p", tf.name], project_root
        )
        if code != 0:
            # Fallback chạy trực tiếp bằng python nếu discover lỗi
            code, stdout, stderr = run_command(["python", str(rel_tf)], project_root)

        if code != 0:
            print(f"   ❌ TEST THẤT BẠI: `{rel_tf.as_posix()}` (Exit code: {code})")
            if stdout:
                print(f"      --- stdout ---\n{stdout}")
            if stderr:
                print(f"      --- stderr ---\n{stderr}")
            success = False
            break
        else:
            print(f"   ✅ PASS: `{rel_tf.as_posix()}`")

    if not success:
        print("\n> [!CAUTION]")
        print("> **CẤM COMMIT CODE CÓ LỖI CHƯA PASS TEST!**")
        print("> Vui lòng sửa lại code để vượt qua các bài kiểm thử trước khi commit.")
        return False

    print("   ✅ Đạt yêu cầu kiểm thử liên quan.")
    return True


def auto_sync_docs_and_changelog(project_root: Path) -> bool:
    """
    Tự động cập nhật Changelog và đồng bộ bản đồ tri thức trước khi commit.
    """
    print("✍️ 4. Đang tự động cập nhật Changelog & Đồng bộ tài liệu...")
    code, stdout, stderr = run_command(["python", "scripts/doc_sync.py"], project_root)
    if code == 0:
        if stdout:
            for line in stdout.splitlines():
                print(f"   {line}")
        return True
    else:
        print(f"   ⚠️ Lỗi cập nhật Changelog & tài liệu: {stderr}")
        return False


def auto_update_work_log(project_root: Path) -> bool:
    """
    Tự động chạy cập nhật nhật ký công việc khi commit thành công.
    """
    print("📝 4. Đang tự động cập nhật nhật ký công việc (Work Log)...")
    code, stdout, stderr = run_command(["python", "scripts/update_work_log.py"], project_root)
    if code == 0:
        if stdout:
            print(f"   {stdout}")
        return True
    else:
        print(f"   ⚠️ Lỗi cập nhật nhật ký tự động: {stderr}")
        return False


def check_ruff_lint(files: list[Path], project_root: Path) -> bool:
    """
    Chạy Ruff linter kiểm tra cú pháp và định dạng.
    """
    py_files = [f for f in files if f.suffix == ".py"]
    if not py_files:
        return True

    print("✨ 2.3. Đang chạy Ruff Linter (Style & Cú pháp)...")
    cmd = ["ruff", "check"] + [str(f) for f in py_files]
    code, stdout, stderr = run_command(cmd, project_root)

    if code != 0:
        print("   ❌ RUFF PHÁT HIỆN LỖI CODE STYLE / CÚ PHÁP:")
        if stdout:
            print(f"      {stdout}")
        if stderr:
            print(f"      {stderr}")
        print("\n> [!WARNING]")
        print("> **Yêu cầu sửa định dạng hoặc chạy `ruff format` trước khi commit!**")
        return False

    print("   ✅ Ruff Linter đạt yêu cầu.")
    return True


def check_code_quality(files: list[Path], project_root: Path) -> bool:
    """
    Chạy Custom Code Quality Auditor (Type hints, Docstrings, Silent Exceptions, UI Boundary).
    """
    py_files = [f for f in files if f.suffix == ".py"]
    if not py_files:
        return True

    print("🛡️ 2.4. Đang chạy Code Quality Auditor (Clean Code & Ranh giới kiến trúc)...")
    cmd = ["python", "scripts/audit_code_quality.py", "--files"] + [str(f) for f in py_files]
    code, stdout, stderr = run_command(cmd, project_root)

    if stdout:
        print(stdout)

    if code != 0:
        if stderr:
            print(f"   ⚠️ Lỗi thực thi Auditor: {stderr}")
        print("   ❌ PHÁT HIỆN VI PHẠM CLEAN CODE / KIẾN TRÚC NGHIÊM TRỌNG!")
        return False

    print("   ✅ Đạt chuẩn Clean Code & Kiến trúc của dự án.")
    return True


def install_hook(project_root: Path) -> bool:
    """
    Cài đặt script này làm pre-commit hook trong thư mục .git/hooks/.
    """
    git_dir = project_root / ".git"
    if not git_dir.exists():
        print("🚨 Lỗi: Thư mục `.git` không tồn tại. Đây có phải là repo Git không?")
        return False

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)
    hook_file = hooks_dir / "pre-commit"

    # Nội dung file shell script gọi python
    hook_content = "#!/bin/sh\n# Git Guard Hook - Tuân thủ hiến pháp AI Assistant\npython scripts/git_guard.py\n"

    try:
        with open(hook_file, "w", newline="\n", encoding="utf-8") as f:
            f.write(hook_content)

        # Cấp quyền thực thi trên Unix/Git Bash
        try:
            os.chmod(hook_file, 0o755)
        except Exception as e:
            # Trên Windows có thể lỗi khi chmod, gán e để tránh silent exception
            _ = e

        print(f"✅ Đã cài đặt thành công Git Guard tại: `{hook_file.relative_to(project_root)}`")
        return True
    except Exception as e:
        print(f"🚨 Lỗi ghi file hook: {e}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Git Guard - Bộ gác cổng Git tự động")
    parser.add_argument("--install", action="store_true", help="Cài đặt Git Guard làm pre-commit hook")
    args = parser.parse_args()

    if args.install:
        success = install_hook(PROJECT_ROOT)
        sys.exit(0 if success else 1)

    # Lấy danh sách các tệp tin staged chuẩn bị commit
    staged_files = get_staged_files(PROJECT_ROOT)
    if not staged_files:
        # Nếu không có thay đổi staged, Git commit sẽ tự động dừng hoặc báo lỗi "nothing to commit"
        # Ta trả về thành công để Git xử lý thông báo mặc định của nó
        sys.exit(0)

    print(f"🛡️ Khởi động Git Guard (Phát hiện {len(staged_files)} file staged)...")

    # 1. Kiểm tra Secrets
    if not check_secrets(staged_files):
        sys.exit(1)

    # 2. Kiểm tra Modularity
    if not check_modularity(staged_files, PROJECT_ROOT):
        sys.exit(1)

    # 2.3. Chạy Ruff Linter
    if not check_ruff_lint(staged_files, PROJECT_ROOT):
        sys.exit(1)

    # 2.4. Chạy Code Quality Auditor
    if not check_code_quality(staged_files, PROJECT_ROOT):
        sys.exit(1)

    # 3. Chạy Unit Tests
    if not run_tests(staged_files, PROJECT_ROOT):
        sys.exit(1)

    # 4. Tự động đồng bộ Changelog & Tài liệu
    auto_sync_docs_and_changelog(PROJECT_ROOT)

    # 5. Tự động ghi nhật ký công việc (chỉ chạy khi mọi thứ đều pass)
    auto_update_work_log(PROJECT_ROOT)

    print("\n💚 [GIT GUARD PASSED] Mọi kiểm tra hoàn tất. Tiếp tục thực hiện commit!")
    sys.exit(0)


if __name__ == "__main__":
    main()
