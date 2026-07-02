# Tên file: scripts/update_work_log.py
# CHỨC NĂNG: Tự động hóa cập nhật nhật ký công việc (work_log) từ các file thay đổi thực tế của Git
# CHANGELOG:
# - 11:49:13 02/07/2026: [NEW] Cập nhật mã nguồn (Antigravity)
# - 16:07:29 23/06/2026: [REFACTOR] refactor(word-export): optimize rendering structure and resolve all 12 linter errors in export_word_renderer (Antigravity)
# - 15:58:00 23/06/2026: [REFACTOR] Phân rã hàm get_git_changes và sửa lỗi exception chaining B904 (Antigravity)
# - 11:37:28 23/06/2026: [UPDATE] feat(notebook): support creating new task groups independently and manage virtual groups (Antigravity)
# - 11:34:57 23/06/2026: [UPDATE] feat(notebook): support creating new task groups independently and manage virtual groups (Antigravity)
# - 11:25:00 23/06/2026: [UPDATE] Thay đổi thư mục lưu log mặc định sang docs/work_logs/ để làm sạch docs/ (Antigravity)
# - 17:03:17 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 17:00:33 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 16:00:27 18/06/2026: [NEW] feat: integrate proactive modularity protocol into local rules.md (Antigravity)
# - 17:23:56 12/06/2026: [NEW] feat: integrate proactive modularity protocol into local rules.md (Antigravity)
# - 16:53:43 12/06/2026: [NEW] Thêm công cụ tự động hóa Changelog & Doc Sync (Antigravity)
# - 16:40:00 12/06/2026: [NEW] Khởi tạo công cụ cập nhật work_log tự động qua Git CLI (Lê Thanh Vân/Antigravity)

import argparse
import os
import subprocess
from datetime import datetime
from pathlib import Path

# Thư mục loại trừ khỏi danh sách thay đổi để tránh ghi log các tệp tin tạm/rác
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

# Các phần mở rộng tệp tin tạm/rác cần bỏ qua
EXCLUDE_EXTENSIONS = {
    ".db-shm",
    ".db-wal",
    ".pyc",
    ".bak",
    ".coverage",
    ".sqlite-journal",
    ".log",
    "-shm",
    "-wal",
    ".tmp",
}


def run_git_command(args: list[str], cwd: Path) -> str:
    """Chạy lệnh Git an toàn trên Windows với cơ chế fallback đường dẫn tuyệt đối."""
    try:
        result = subprocess.run(
            args, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="ignore", check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        # Thử đường dẫn Git mặc định trên Windows nếu lệnh thông thường lỗi hoặc không tìm thấy
        git_path = r"C:\Program Files\Git\cmd\git.exe"
        if os.path.exists(git_path):
            args[0] = git_path
            try:
                result = subprocess.run(
                    args, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="ignore", check=True
                )
                return result.stdout.strip()
            except subprocess.CalledProcessError as e2:
                raise RuntimeError(f"Lệnh Git thất bại: {e2.stderr.strip()}") from e2
        if isinstance(e, subprocess.CalledProcessError):
            raise RuntimeError(f"Lệnh Git thất bại: {e.stderr.strip()}") from e
        raise RuntimeError("Không tìm thấy lệnh Git trên hệ thống.") from e


def _get_changes_from_files(cwd: Path, files: str) -> list[tuple[str, str]]:
    """Lấy danh sách thay đổi từ danh sách file cụ thể."""
    changes: list[tuple[str, str]] = []
    file_list = [f.strip() for f in files.split(",") if f.strip()]
    for file_path in file_list:
        p_path = Path(file_path)
        # Loại bỏ nếu thuộc thư mục hoặc đuôi file rác
        if any(part in p_path.parts for part in EXCLUDE_DIRS) or p_path.suffix in EXCLUDE_EXTENSIONS:
            continue
        if "docs" in p_path.parts and p_path.name.startswith("work_log_"):
            continue

        full_path = cwd / p_path
        if not full_path.exists():
            status = "DELETE"
        else:
            status = "MODIFY"
            try:
                # Check git status cho file cụ thể này
                git_status = run_git_command(["git", "status", "--porcelain", str(file_path)], cwd)
                if git_status:
                    state = git_status[:2]
                    if "D" in state:
                        status = "DELETE"
                    elif "A" in state or "??" in state:
                        status = "NEW"
            except Exception:
                pass
        changes.append((file_path.replace("\\", "/"), status))
    return changes


def _get_changes_from_status(cwd: Path, staged_only: bool) -> list[tuple[str, str]]:
    """Quét trạng thái hiện tại (chưa commit bao gồm staged + unstaged + untracked)."""
    changes: list[tuple[str, str]] = []
    try:
        status_out = run_git_command(["git", "status", "--porcelain"], cwd)
        if not status_out:
            return []
        for line in status_out.splitlines():
            if len(line) < 4:
                continue
            state = line[:2]
            file_path = line[3:].strip()

            # Xử lý tệp tin bị đổi tên (ví dụ: R  old -> new)
            if " -> " in file_path:
                parts = file_path.split(" -> ")
                file_path = parts[1].strip()

            file_path = file_path.strip('"')
            p_path = Path(file_path)

            # Loại bỏ các file thuộc thư mục loại trừ hoặc có đuôi file rác
            if any(part in p_path.parts for part in EXCLUDE_DIRS) or p_path.suffix in EXCLUDE_EXTENSIONS:
                continue

            # Loại bỏ các file log work_log_*.md để tránh tự ghi nhận chính nó
            if "docs" in p_path.parts and p_path.name.startswith("work_log_"):
                continue

            # Lọc theo staged_only nếu được yêu cầu
            if staged_only and state[0] in (" ", "?"):
                continue

            # Phân loại trạng thái
            if "D" in state:
                status = "DELETE"
            elif "A" in state or "??" in state:
                status = "NEW"
            else:
                status = "MODIFY"

            changes.append((file_path, status))
    except Exception as e:
        print(f"⚠️ Không thể lấy status hiện tại: {e}")
    return changes


def _get_changes_from_head(cwd: Path) -> list[tuple[str, str]]:
    """Lấy danh sách thay đổi từ commit HEAD gần nhất."""
    changes: list[tuple[str, str]] = []
    try:
        diff_out = run_git_command(["git", "diff-tree", "--no-commit-id", "--name-status", "-r", "HEAD"], cwd)
        if not diff_out:
            return []
        for line in diff_out.splitlines():
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                state, file_path = parts[0], parts[1].strip('"')
                p_path = Path(file_path)

                if any(part in p_path.parts for part in EXCLUDE_DIRS) or p_path.suffix in EXCLUDE_EXTENSIONS:
                    continue

                if "docs" in p_path.parts and p_path.name.startswith("work_log_"):
                    continue

                if "D" in state:
                    status = "DELETE"
                elif "A" in state:
                    status = "NEW"
                else:
                    status = "MODIFY"

                changes.append((file_path, status))
    except Exception as e:
        print(f"⚠️ Không thể lấy diff của commit gần nhất: {e}")
    return changes


def get_git_changes(cwd: Path, files: str | None = None, staged_only: bool = False) -> list[tuple[str, str]]:
    """Lấy danh sách các tệp tin đã thay đổi và trạng thái tương ứng từ Git hoặc tham số.

    Args:
        cwd: Thư mục làm việc.
        files: Danh sách file cụ thể phân tách bằng dấu phẩy.
        staged_only: Chỉ lấy các thay đổi đã được staged.

    Returns:
        Danh sách các tuple file thay đổi và trạng thái.
    """
    if files:
        changes = _get_changes_from_files(cwd, files)
        return sorted(changes, key=lambda x: x[0])

    changes = _get_changes_from_status(cwd, staged_only)

    if not changes and not staged_only:
        changes = _get_changes_from_head(cwd)

    return sorted(changes, key=lambda x: x[0])


def get_last_commit_message(cwd: Path) -> str:
    """
    Lấy nội dung thông điệp commit gần nhất để làm mô tả tác vụ mặc định.

    Args:
        cwd (Path): Thư mục làm việc.

    Returns:
        str: Thông điệp commit.
    """
    try:
        msg = run_git_command(["git", "log", "-1", "--pretty=%B"], cwd)
        # Lấy dòng đầu tiên của commit message
        if msg:
            return msg.splitlines()[0].strip()
    except Exception as e:
        # Bỏ qua nếu lệnh git log thất bại
        _ = e
    return "Cập nhật mã nguồn hệ thống"


def auto_detect_type(changes: list[tuple[str, str]]) -> str:
    """
    Tự động phát hiện loại nhật ký dựa trên phần lớn các tệp sửa đổi.

    Args:
        changes (List[Tuple[str, str]]): Danh sách tệp thay đổi.

    Returns:
        str: 'task' nếu chủ yếu là tài liệu nghiệp vụ, ngược lại là 'code'.
    """
    if not changes:
        return "code"

    task_extensions = {".md", ".docx", ".xlsx", ".pdf", ".txt"}
    task_count = 0
    code_count = 0

    for file_path, _ in changes:
        p = Path(file_path)
        # Các tệp nằm trong docs/ nhưng không phải docs/architecture/ thì được coi là tài liệu nghiệp vụ
        if "docs" in p.parts:
            if "architecture" in p.parts or p.name.startswith("work_log_"):
                code_count += 1
                continue
            task_count += 1
        elif p.suffix in task_extensions:
            task_count += 1
        else:
            code_count += 1

    return "task" if task_count > code_count else "code"


def generate_log_block(
    project: str, task_desc: str, user: str, time_str: str, changes: list[tuple[str, str]], details: str | None = None
) -> str:
    """
    Sinh khối Markdown cho một bản ghi nhật ký công việc.

    Args:
        project (str): Tên dự án.
        task_desc (str): Mô tả tác vụ.
        user (str): Người thực hiện.
        time_str (str): Thời gian (HH:MM:SS).
        changes (List[Tuple[str, str]]): Danh sách file thay đổi.
        details (Optional[str]): Chi tiết quá trình làm việc.

    Returns:
        str: Chuỗi Markdown hoàn chỉnh.
    """
    files_table = ""
    if changes:
        files_table = "| Đường dẫn file | Trạng thái |\n| :--- | :---: |\n"
        for file_path, status in changes:
            # Chuẩn hóa đường dẫn hiển thị với forward slash
            normalized_path = file_path.replace("\\", "/")
            files_table += f"| `{normalized_path}` | {status} |\n"
    else:
        files_table = "*Không phát hiện thay đổi file nào qua Git.*\n"

    # Tạo khối chi tiết công việc nếu có
    details_section = ""
    if details:
        details_section = f"- **Chi tiết công việc**:\n{details.strip()}\n"

    block = (
        f"## [{project}]_{task_desc} ({time_str})\n"
        f"- **Tác vụ**: {task_desc}\n"
        f"- **Người thực hiện**: {user}\n"
        f"{details_section}"
        f"- **Danh sách file thay đổi**:\n"
        f"{files_table}\n"
        f"---\n"
    )
    return block


def prepend_log_to_file(file_path: Path, log_content: str, date_str: str, project: str, is_task: bool) -> None:
    """
    Ghi đè an toàn bằng cách chèn khối log mới vào sau header ngày của file log cũ.

    Args:
        file_path (Path): Đường dẫn tới file log mục tiêu.
        log_content (str): Nội dung khối log mới.
        date_str (str): Chuỗi ngày YYYY-MM-DD.
        project (str): Tên dự án.
        is_task (bool): True nếu là log task nghiệp vụ, ngược lại là code.
    """
    header_title = "NGHIỆP VỤ" if is_task else "MÃ NGUỒN"
    emoji = "📝" if is_task else "📑"

    default_header = (
        f"# {emoji} NHẬT KÝ CÔNG VIỆC {header_title} - NGÀY {date_str}\n\n"
        f"> **Dự án**: {project}\n"
        f"> **Ngày tạo**: {date_str}\n\n"
        f"---\n\n"
    )

    content = ""
    if file_path.exists():
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️ Lỗi đọc file log cũ: {e}")

    if not content:
        # Tạo mới file hoàn toàn
        new_content = default_header + log_content
    else:
        # Chèn thông minh sau dòng phân cách "---" đầu tiên
        lines = content.splitlines(keepends=True)
        insert_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == "---":
                insert_idx = i + 1
                break

        if insert_idx != -1:
            new_lines = lines[:insert_idx]
            new_lines.append("\n")
            new_lines.append(log_content)
            new_lines.extend(lines[insert_idx:])
            new_content = "".join(new_lines)
        else:
            # Fallback nếu không có dòng "---", chèn thẳng lên đầu
            new_content = log_content + "\n" + content

    # Ghi lại file an toàn
    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ Đã ghi nhận log vào: `{file_path.relative_to(file_path.parents[1])}`")
    except Exception as e:
        print(f"🚨 Không thể ghi file log: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Công cụ tự động hóa cập nhật work_log")
    parser.add_argument(
        "-t", "--task", type=str, help="Mô tả công việc thực hiện (nếu trống sẽ lấy từ commit gần nhất)"
    )
    parser.add_argument("-y", "--type", type=str, choices=["code", "task"], help="Loại nhật ký: 'code' hoặc 'task'")
    parser.add_argument("-p", "--project", type=str, default="AI_ASSISTANT", help="Tên dự án (mặc định: AI_ASSISTANT)")
    parser.add_argument("-u", "--user", type=str, default="Antigravity / Anh Lưu", help="Người thực hiện")
    parser.add_argument("-d", "--date", type=str, help="Ngày ghi nhận định dạng YYYY_MM_DD (mặc định: hôm nay)")
    parser.add_argument(
        "-f", "--files", type=str, help="Danh sách các file thay đổi, phân tách bằng dấu phẩy (bỏ qua Git)"
    )
    parser.add_argument("-s", "--staged", action="store_true", help="Chỉ lấy các thay đổi đã được staged (git add)")
    parser.add_argument("-desc", "--details", type=str, help="Mô tả chi tiết quá trình làm việc")
    parser.add_argument("-df", "--details-file", type=str, help="Đường dẫn đến file chứa mô tả chi tiết công việc")
    parser.add_argument("--log-dir", type=str, help="Thư mục lưu file log (mặc định: docs/work_logs/)")

    args = parser.parse_args()

    # Thư mục gốc dự án (đi lên 1 cấp từ thư mục scripts/)
    project_root = Path(__file__).resolve().parents[1]

    # Lấy ngày và giờ hiện tại
    now = datetime.now()
    date_suffix = args.date if args.date else now.strftime("%Y_%m_%d")
    date_dash = date_suffix.replace("_", "-")
    time_str = now.strftime("%H:%M:%S")

    # Xác định mô tả chi tiết công việc
    details_content = None
    if args.details:
        details_content = args.details
    elif args.details_file:
        details_file_path = Path(args.details_file)
        if details_file_path.exists():
            try:
                details_content = details_file_path.read_text(encoding="utf-8")
            except Exception as e:
                print(f"⚠️ Không thể đọc file chi tiết công việc: {e}")
        else:
            # Thử tìm kiếm tương đối từ project_root nếu đường dẫn tuyệt đối không tồn tại
            rel_path = project_root / details_file_path
            if rel_path.exists():
                try:
                    details_content = rel_path.read_text(encoding="utf-8")
                except Exception as e:
                    print(f"⚠️ Không thể đọc file chi tiết công việc: {e}")
            else:
                print(f"⚠️ File chi tiết công việc không tồn tại: {args.details_file}")

    print("🔍 Đang thu thập dữ liệu từ Git...")
    changes = get_git_changes(project_root, files=args.files, staged_only=args.staged)

    # Xác định mô tả tác vụ
    task_desc = args.task
    if not task_desc:
        task_desc = get_last_commit_message(project_root)
        print(f"ℹ️ Sử dụng mô tả từ commit gần nhất: '{task_desc}'")

    # Xác định loại log
    log_type = args.type
    if not log_type:
        log_type = auto_detect_type(changes)
        print(f"ℹ️ Tự động phát hiện loại log: '{log_type}'")

    # Xác định đường dẫn file log
    is_task = log_type == "task"
    log_filename = f"work_log_{log_type}_{date_suffix}.md"
    if args.log_dir:
        log_dir_path = Path(args.log_dir)
        if not log_dir_path.is_absolute():
            log_dir_path = project_root / log_dir_path
        log_file_path = log_dir_path / log_filename
    else:
        log_file_path = project_root / "docs" / "work_logs" / log_filename

    # Sinh nội dung log
    log_block = generate_log_block(args.project, task_desc, args.user, time_str, changes, details=details_content)

    # Ghi nhận log
    prepend_log_to_file(log_file_path, log_block, date_dash, args.project, is_task)


if __name__ == "__main__":
    main()
