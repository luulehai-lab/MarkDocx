# Tên file: scripts/check_modularity.py
# CHỨC NĂNG: Kiểm tra và giám sát tuân thủ kỷ luật Modularity (chống phình code, giới hạn 500/800 dòng)
# CHANGELOG:
# - 11:49:13 02/07/2026: [NEW] Cập nhật mã nguồn (Antigravity)
# - 17:03:17 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 17:00:33 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 10:38:36 19/06/2026: [REFACTOR] refactor(modularity): split main_window, export_utils, ocr_reconstructor, and bridge_util into submodules and mixins (Antigravity)
# - 14:45:00 11/06/2026: [NEW] Khởi tạo công cụ giám sát Modularity tự động cho dự án AI Assistant (Lê Thanh Vân/Antigravity)
# - 10:25:00 19/06/2026: [UPDATE] Bổ sung "_backups" vào danh sách thư mục loại trừ khi quét (Lê Thanh Vân/Antigravity)

import argparse
import ast
import os
from pathlib import Path
from typing import Any

# Cấu hình giới hạn dòng
SOFT_LIMIT = 500
HARD_LIMIT = 800

EXCLUDE_DIRS = {
    ".git",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "archives",
    "backups",
    "_backups",
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


class ModularityChecker:
    """
    Lớp chịu trách nhiệm kiểm tra số lượng dòng và cấu trúc module để đảm bảo tính Modularity.
    """

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def count_lines(self, file_path: Path) -> tuple[int, int, int]:
        """
        Đếm tổng số dòng, dòng trống và dòng comment trong file.

        Args:
            file_path (Path): Đường dẫn tới file cần đếm.

        Returns:
            Tuple[int, int, int]: (Tổng số dòng, Số dòng comment, Số dòng trống)
        """
        total = 0
        comments = 0
        blanks = 0
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                for line in f:
                    total += 1
                    stripped = line.strip()
                    if not stripped:
                        blanks += 1
                    elif stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
                        comments += 1
        except Exception as e:
            # Ghi nhận lỗi đọc file nhưng không làm gián đoạn chương trình
            _ = e
        return total, comments, blanks

    def analyze_structure(self, file_path: Path) -> dict[str, Any]:
        """
        Phân tích cấu trúc của file Python bằng AST để đếm class, function và import.

        Args:
            file_path (Path): Đường dẫn file Python.

        Returns:
            Dict[str, Any]: Kết quả phân tích cấu trúc.
        """
        result = {"classes": [], "functions": [], "imports_count": 0, "syntax_valid": True}
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                tree = ast.parse(f.read(), filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    result["classes"].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    # Chỉ lấy hàm ở cấp module
                    result["functions"].append(node.name)
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    result["imports_count"] += len(node.names) if hasattr(node, "names") else 1
        except Exception:
            result["syntax_valid"] = False
        return result

    def scan_project(self) -> list[dict[str, Any]]:
        """
        Quét toàn bộ dự án và thu thập số liệu modularity & coupling.

        Returns:
            List[Dict[str, Any]]: Danh sách kết quả kiểm tra từng file.
        """
        reports = []
        for root, dirs, files in os.walk(self.project_root):
            # Loại bỏ thư mục loại trừ
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                if not file.endswith(".py"):
                    continue
                # Skip test files
                if file.startswith("test_"):
                    continue

                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_root)

                total_lines, comments, blanks = self.count_lines(file_path)
                structure = self.analyze_structure(file_path)

                # Tính toán điểm khớp nối (Coupling Score)
                # Điểm số phản ánh mức độ phức tạp: số class có trọng số cao, rồi tới hàm và imports
                classes_c = len(structure["classes"])
                funcs_c = len(structure["functions"])
                imports_c = structure["imports_count"]
                coupling_score = classes_c * 3 + funcs_c * 1.5 + imports_c

                reports.append(
                    {
                        "file": str(relative_path).replace("\\", "/"),
                        "total_lines": total_lines,
                        "comments": comments,
                        "blanks": blanks,
                        "classes_count": classes_c,
                        "funcs_count": funcs_c,
                        "imports_count": imports_c,
                        "coupling_score": round(coupling_score, 1),
                        "syntax_valid": structure["syntax_valid"],
                    }
                )

        # Sắp xếp theo số dòng giảm dần
        reports.sort(key=lambda x: x["total_lines"], reverse=True)
        return reports

    def check_file_impact(self, target_file: str, estimated_add_lines: int) -> dict[str, Any]:
        """
        Đánh giá tác động về mặt dòng code và cấu trúc trước khi sửa file.

        Args:
            target_file (str): Đường dẫn tương đối hoặc tuyệt đối tới file.
            estimated_add_lines (int): Số dòng ước tính sẽ thêm vào.

        Returns:
            Dict[str, Any]: Báo cáo tác động và khuyến nghị.
        """
        file_path = Path(target_file)
        if not file_path.is_absolute():
            file_path = self.project_root / file_path

        if not file_path.exists():
            return {"exists": False, "file": target_file, "msg": f"File {target_file} không tồn tại (sẽ tạo mới)."}

        total_lines, _, _ = self.count_lines(file_path)
        structure = self.analyze_structure(file_path)
        new_total = total_lines + estimated_add_lines

        classes_c = len(structure["classes"])
        funcs_c = len(structure["functions"])
        imports_c = structure["imports_count"]
        coupling_score = classes_c * 3 + funcs_c * 1.5 + imports_c

        violation = "NONE"
        if new_total >= HARD_LIMIT:
            violation = "HARD_LIMIT_VIOLATION"
        elif new_total >= SOFT_LIMIT:
            violation = "SOFT_LIMIT_WARNING"
        elif coupling_score > 25:
            violation = "HIGH_COUPLING_WARNING"

        recommendation = ""
        if violation == "HARD_LIMIT_VIOLATION":
            recommendation = (
                f"🚨 CẤM APPEND CODE! File {file_path.name} hiện tại có {total_lines} dòng. "
                f"Nếu thêm {estimated_add_lines} dòng sẽ vượt quá giới hạn cứng {HARD_LIMIT} dòng (Tổng: {new_total}). "
                f"BẮT BUỘC phải tách logic mới thành một module riêng biệt. File cũ chỉ import và route logic."
            )
        elif violation == "SOFT_LIMIT_WARNING":
            recommendation = (
                f"⚠️ CẢNH BÁO PHÌNH CODE! File {file_path.name} hiện có {total_lines} dòng. "
                f"Thêm {estimated_add_lines} dòng sẽ vượt qua ngưỡng cảnh báo {SOFT_LIMIT} dòng (Tổng: {new_total}). "
                f"Khuyến nghị tách module mới ngay để bảo trì tốt hơn."
            )
        elif violation == "HIGH_COUPLING_WARNING":
            recommendation = (
                f"🔌 CẢNH BÁO KHỚP NỐI CAO (Coupling Score: {coupling_score})! "
                f"File này hiện chứa nhiều Class ({classes_c}), Hàm ({funcs_c}) hoặc Imports ({imports_c}). "
                f"Dù tổng số dòng ({new_total}) chưa vượt giới hạn, cấu trúc hiện tại đã quá phức tạp. "
                f"Yêu cầu TƯ DUY CẤU TRÚC: Thiết kế tách biệt module logic mới ngay từ đầu thay vì sửa trực tiếp."
            )
        else:
            if classes_c >= 2 or funcs_c >= 8:
                recommendation = (
                    f"💡 Khuyên dùng: File có cấu trúc vừa phải ({classes_c} classes, {funcs_c} functions). "
                    f"Nếu logic mới có tính chất độc lập, hãy ưu tiên viết file mới và import vào đây."
                )
            else:
                recommendation = "✅ An toàn. Cho phép sửa trực tiếp (surgical modification)."

        return {
            "exists": True,
            "file": target_file,
            "current_lines": total_lines,
            "estimated_added": estimated_add_lines,
            "projected_lines": new_total,
            "classes_count": classes_c,
            "funcs_count": funcs_c,
            "imports_count": imports_c,
            "coupling_score": round(coupling_score, 1),
            "violation": violation,
            "recommendation": recommendation,
        }


def print_markdown_report(reports: list[dict[str, Any]]) -> None:
    """In báo cáo quét dự án dưới dạng Markdown đẹp mắt."""
    print("# 📊 BÁO CÁO GIÁM SÁT KỶ LUẬT MODULARITY & COUPLING")
    print(f"\n- **Ngưỡng cảnh báo mềm (Soft Limit)**: {SOFT_LIMIT} dòng")
    print(f"- **Ngưỡng giới hạn cứng (Hard Limit)**: {HARD_LIMIT} dòng")
    print(
        "- **Ngưỡng cảnh báo khớp nối (Coupling Warning)**: Điểm số > 25 (Tính toán dựa trên Số Class * 3 + Số Hàm * 1.5 + Số Imports)"
    )

    print("\n## 🚨 Danh sách các file vi phạm hoặc có nguy cơ vi phạm")
    violated = [r for r in reports if r["total_lines"] >= SOFT_LIMIT or r["coupling_score"] > 25]
    if not violated:
        print("🟢 Tuyệt vời! Hiện tại không có file nào vi phạm số dòng hoặc có mức độ khớp nối quá cao.")
    else:
        print("| File | Tổng dòng | Lớp | Hàm | Imports | Khớp nối (Coupling) | Trạng thái |")
        print("| :--- | :---: | :---: | :---: | :---: | :---: | :--- |")
        for r in violated:
            status = (
                "🚨 CẤM SỬA TRỰC TIẾP"
                if r["total_lines"] >= HARD_LIMIT
                else (
                    "⚠️ Khớp nối cao"
                    if r["coupling_score"] > 25 and r["total_lines"] < SOFT_LIMIT
                    else "⚠️ Nguy cơ phình"
                )
            )
            line_str = f"**{r['total_lines']}**" if r["total_lines"] >= SOFT_LIMIT else str(r["total_lines"])
            coupling_str = f"**{r['coupling_score']}**" if r["coupling_score"] > 25 else str(r["coupling_score"])
            print(
                f"| `{r['file']}` | {line_str} | {r['classes_count']} | {r['funcs_count']} | {r['imports_count']} | {coupling_str} | {status} |"
            )

    print("\n## 📁 Thống kê chi tiết toàn bộ file Python (Top 30 file phức tạp nhất)")
    print("| File | Tổng dòng | Lớp | Hàm | Imports | Điểm Khớp Nối |")
    print("| :--- | :---: | :---: | :---: | :---: | :---: |")
    # Sắp xếp top 30 theo coupling_score giảm dần để hiển thị file có độ phức tạp cao nhất trước
    sorted_by_coupling = sorted(reports, key=lambda x: x["coupling_score"], reverse=True)
    for r in sorted_by_coupling[:30]:
        line_str = f"**{r['total_lines']}**" if r["total_lines"] >= SOFT_LIMIT else str(r["total_lines"])
        coupling_str = f"**{r['coupling_score']}**" if r["coupling_score"] > 25 else str(r["coupling_score"])
        print(
            f"| `{r['file']}` | {line_str} | {r['classes_count']} | {r['funcs_count']} | {r['imports_count']} | {coupling_str} |"
        )

    if len(reports) > 30:
        print(f"\n*(Còn {len(reports) - 30} file khác không hiển thị)*")


def main() -> None:
    parser = argparse.ArgumentParser(description="Giám sát kỷ luật Modularity của dự án.")
    parser.add_argument("--scan", action="store_true", help="Quét toàn bộ dự án để kiểm tra số dòng các file.")
    parser.add_argument("--check-file", type=str, help="Kiểm tra tác động cụ thể lên một file.")
    parser.add_argument("--add-lines", type=int, default=50, help="Số dòng dự kiến thêm khi check file (mặc định: 50).")

    args = parser.parse_args()
    project_root = Path(__file__).resolve().parent.parent
    checker = ModularityChecker(project_root)

    if args.scan:
        reports = checker.scan_project()
        print_markdown_report(reports)

    elif args.check_file:
        impact = checker.check_file_impact(args.check_file, args.add_lines)
        print("\n## 🔍 KẾT QUẢ ĐỐI SOÁT TÁC ĐỘNG SỬA CODE")
        print(f"- **Tệp mục tiêu**: `{impact['file']}`")
        if impact["exists"]:
            print(f"- **Số dòng hiện tại**: {impact['current_lines']} dòng")
            print(f"- **Số dòng dự kiến thêm**: +{impact['estimated_added']} dòng")
            print(f"- **Tổng số dòng dự kiến**: **{impact['projected_lines']}** dòng")
            print(f"- **Cấu trúc hiện tại**: {impact['classes_count']} Classes, {impact['funcs_count']} Functions")
            print(f"- **Mức độ vi phạm**: `{impact['violation']}`")
            print(f"\n> [!IMPORTANT]\n> **Khuyến nghị**: {impact['recommendation']}")
        else:
            print(f"- **Trạng thái**: {impact['msg']}")
            print("\n> [!TIP]\n> Tạo file mới: Vui lòng viết code dạng module gọn gàng và tuân thủ giới hạn.")

    else:
        # Mặc định quét dự án
        reports = checker.scan_project()
        print_markdown_report(reports)


if __name__ == "__main__":
    main()
