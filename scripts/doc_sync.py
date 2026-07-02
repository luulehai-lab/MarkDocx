# Tên file: scripts/doc_sync.py
# CHỨC NĂNG: Tự động hóa cập nhật Changelog ở đầu file và đồng bộ đăng ký file mới vào MAP_TOOLS.md
# CHANGELOG:
# - 11:49:13 02/07/2026: [NEW] Cập nhật mã nguồn (Antigravity)
# - 11:40:33 23/06/2026: [UPDATE] feat(notebook): support creating new task groups independently and manage virtual groups (Antigravity)
# - 11:35:00 23/06/2026: [FIX] Sửa get_git_changes chỉ lấy các file staged (diff --cached) để tránh tự động add các file untracked. (Antigravity)
# - 17:03:17 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 17:00:33 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 16:00:27 18/06/2026: [NEW] feat: integrate proactive modularity protocol into local rules.md (Antigravity)
# - 17:23:56 12/06/2026: [NEW] feat: integrate proactive modularity protocol into local rules.md (Antigravity)
# - 16:53:43 12/06/2026: [NEW] Thêm công cụ tự động hóa Changelog & Doc Sync (Antigravity)
# - 17:00:00 12/06/2026: [NEW] Khởi tạo công cụ tự động cập nhật Changelog và đồng bộ bản đồ MAP_TOOLS.md (Lê Thanh Vân/Antigravity)

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Thư mục gốc dự án
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Thư mục loại trừ khỏi quét
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


def run_git_command(args: list[str], cwd: Path) -> str:
    """
    Chạy lệnh Git an toàn trên Windows.
    """
    import subprocess

    try:
        result = subprocess.run(
            args, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="ignore", check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        git_path = r"C:\Program Files\Git\cmd\git.exe"
        if os.path.exists(git_path):
            args[0] = git_path
            try:
                result = subprocess.run(
                    args, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="ignore", check=True
                )
                return result.stdout.strip()
            except Exception as ex:
                raise RuntimeError(f"Lệnh Git thất bại: {ex}") from ex
        raise RuntimeError("Không tìm thấy lệnh Git trên hệ thống.") from e


def get_git_changes(cwd: Path) -> list[tuple[str, str]]:
    """
    Lấy danh sách các tệp tin đã staged (cached) chuẩn bị commit từ Git.
    """
    changes: list[tuple[str, str]] = []
    try:
        # Chỉ lấy các file đã staged thông qua git diff --cached --name-status
        status_out = run_git_command(["git", "diff", "--cached", "--name-status"], cwd)
        if status_out:
            for line in status_out.splitlines():
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    state, file_path = parts[0], parts[1].strip('"')
                    if any(part in Path(file_path).parts for part in EXCLUDE_DIRS):
                        continue
                    if "D" in state:
                        status = "DELETE"
                    elif "A" in state:
                        status = "NEW"
                    else:
                        status = "MODIFY"
                    changes.append((file_path, status))
    except Exception as e:
        print(f"⚠️ Lỗi lấy thay đổi staged từ Git: {e}")
    return changes


def get_last_commit_message(cwd: Path) -> str:
    """
    Lấy message commit gần nhất.
    """
    try:
        msg = run_git_command(["git", "log", "-1", "--pretty=%B"], cwd)
        if msg:
            return msg.splitlines()[0].strip()
    except Exception as e:
        # Ghi nhận lỗi git log nhưng không crash chương trình
        _ = e
    return "Cập nhật mã nguồn"


def update_file_changelog(file_path: Path, tag: str, desc: str) -> bool:
    """Chèn dòng changelog mới vào phần header của file.

    Args:
        file_path: Đường dẫn đến tệp tin cần cập nhật.
        tag: Nhãn thay đổi (NEW, UPDATE, FIX, REFACTOR).
        desc: Mô tả ngắn gọn thay đổi.

    Returns:
        bool: True nếu cập nhật thành công, False nếu ngược lại.
    """
    if not file_path.exists() or not file_path.is_file():
        return False

    suffix = file_path.suffix.lower()
    # Chỉ xử lý các file mã nguồn và tài liệu quan trọng
    if suffix not in {".py", ".md", ".bat", ".sh"}:
        return False

    try:
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"⚠️ Không thể đọc file {file_path.name}: {e}")
        return False

    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%d/%m/%Y")
    # Dòng changelog mới cần chèn
    new_entry = f"- {time_str} {date_str}: [{tag}] {desc} (Antigravity)"

    # Định nghĩa mẫu tìm kiếm CHANGELOG dựa trên loại file
    changelog_pattern = None
    replacement_template = None

    if suffix == ".py":
        changelog_pattern = re.compile(r"(#\s*CHANGELOG:\s*\n)")
        replacement_template = f"\\1# {new_entry}\n"
    elif suffix == ".md":
        changelog_pattern = re.compile(r"(<!--\s*CHANGELOG:\s*\n)", re.IGNORECASE)
        replacement_template = f"\\1- {new_entry}\n"
    elif suffix in {".bat", ".sh"}:
        comment_char = "::" if suffix == ".bat" else "#"
        changelog_pattern = re.compile(rf"({comment_char}\s*CHANGELOG:\s*\n)", re.IGNORECASE)
        replacement_template = f"\\1{comment_char} {new_entry}\n"

    if changelog_pattern and replacement_template:
        if changelog_pattern.search(content):
            # Kiểm tra xem dòng changelog này đã tồn tại trong file chưa (tránh trùng lặp)
            if new_entry in content:
                return False

            new_content = changelog_pattern.sub(replacement_template, content, count=1)
            try:
                with open(file_path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(new_content)
                print(f"   📝 Đã cập nhật Changelog cho: `{file_path.name}`")
                try:
                    run_git_command(["git", "add", str(file_path)], PROJECT_ROOT)
                except Exception as ge:
                    print(f"   ⚠️ Lỗi git add file {file_path.name}: {ge}")
                return True
            except Exception as e:
                print(f"   ⚠️ Lỗi ghi file {file_path.name}: {e}")
        else:
            # Nếu file chưa có header changelog, tự tạo header mẫu ở đầu file
            # (chỉ áp dụng cho file Python mới tạo)
            if suffix == ".py":
                rel_path = file_path.relative_to(PROJECT_ROOT).as_posix()
                header = f"# Tên file: {rel_path}\n# CHỨC NĂNG: {desc}\n# CHANGELOG:\n# {new_entry}\n\n"
                try:
                    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
                        f.write(header + content)
                    print(f"   🆕 Khởi tạo Header Changelog cho: `{file_path.name}`")
                    try:
                        run_git_command(["git", "add", str(file_path)], PROJECT_ROOT)
                    except Exception as ge:
                        print(f"   ⚠️ Lỗi git add file {file_path.name}: {ge}")
                    return True
                except Exception as e:
                    print(f"   ⚠️ Lỗi ghi header file {file_path.name}: {e}")

    return False


def sync_map_tools(new_files: list[Path], project_root: Path) -> None:
    """
    Kiểm tra và tự động cảnh báo/đăng ký file mới vào MAP_TOOLS.md.
    """
    map_file = project_root / "docs" / "architecture" / "MAP_TOOLS.md"
    if not map_file.exists():
        return

    try:
        with open(map_file, encoding="utf-8", errors="ignore") as f:
            map_content = f.read()
    except Exception as e:
        print(f"⚠️ Lỗi đọc MAP_TOOLS.md: {e}")
        return

    unregistered_files = []
    for new_file in new_files:
        if new_file.suffix != ".py":
            continue
        rel_name = new_file.name
        # Kiểm tra xem tên file đã xuất hiện trong MAP_TOOLS.md chưa
        if f"`{rel_name}`" not in map_content:
            unregistered_files.append(new_file)

    if unregistered_files:
        print("\n📢 3. ĐỒNG BỘ BẢN ĐỒ KIẾN TRÚC (MAP_TOOLS.md)...")
        for uf in unregistered_files:
            rel_path = uf.relative_to(project_root).as_posix()
            print(f"   ⚠️ CẢNH BÁO: File mới `{rel_path}` CHƯA được đăng ký trong MAP_TOOLS.md!")
            print(f"      -> Vui lòng mở [MAP_TOOLS.md](file:///{map_file.as_posix()}) để đăng ký thông tin.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Công cụ tự động hóa Changelog & Doc Sync")
    parser.add_argument("-t", "--task", type=str, help="Mô tả thay đổi (nếu trống sẽ lấy từ commit gần nhất)")
    parser.add_argument("-g", "--tag", type=str, help="Tag changelog (NEW, UPDATE, FIX, REFACTOR)")
    args = parser.parse_args()

    print("🔍 Đang quét các file thay đổi từ Git...")
    changes = get_git_changes(PROJECT_ROOT)
    if not changes:
        print("ℹ️ Không phát hiện thay đổi nào từ Git.")
        sys.exit(0)

    # Xác định mô tả
    desc = args.task
    if not desc:
        desc = get_last_commit_message(PROJECT_ROOT)

    # Phân loại và xử lý từng file
    new_files_to_sync = []

    print("✍️ 2. Đang kiểm tra và cập nhật Changelog tệp tin...")
    for rel_path_str, status in changes:
        file_path = PROJECT_ROOT / rel_path_str
        if not file_path.exists():
            continue

        # Xác định tag changelog
        file_tag = args.tag
        if not file_tag:
            if status == "NEW":
                file_tag = "NEW"
            elif any(k in desc.lower() for k in ["fix", "bug", "sửa lỗi"]):
                file_tag = "FIX"
            elif "refactor" in desc.lower():
                file_tag = "REFACTOR"
            else:
                file_tag = "UPDATE"

        # Cập nhật changelog ở đầu file
        update_file_changelog(file_path, file_tag, desc)

        if status == "NEW" and file_path.suffix == ".py":
            new_files_to_sync.append(file_path)

    # Đồng bộ đăng ký MAP_TOOLS.md
    if new_files_to_sync:
        sync_map_tools(new_files_to_sync, PROJECT_ROOT)

    print("\n✅ Hoàn thành quy trình Changelog & Doc-Sync!")


if __name__ == "__main__":
    main()
