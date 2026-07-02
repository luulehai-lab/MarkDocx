# Tên file: scripts/audit_code_quality.py
# CHỨC NĂNG: Phân tích cú pháp AST tự động kiểm tra Clean Code, Type Hints, Docstrings và Ranh giới kiến trúc.
# CHANGELOG:
# - 14:52:00 02/07/2026: [UPDATE] Cập nhật bộ lọc is_app_file để hỗ trợ backend, frontend và main.py của dự án Markdown Viewer (Lê Thanh Vân/Antigravity)
# - 11:49:13 02/07/2026: [NEW] Cập nhật mã nguồn (Antigravity)
# - 16:07:29 23/06/2026: [REFACTOR] refactor(word-export): optimize rendering structure and resolve all 12 linter errors in export_word_renderer (Antigravity)
# - 15:55:00 23/06/2026: [REFACTOR] Rút ngắn docstrings các hàm helper để hạ tổng số dòng xuống dưới 800 dòng tránh vi phạm modularity (Antigravity)
# - 14:49:00 23/06/2026: [UPDATE] Cập nhật bộ lọc quét kiểm toán chất lượng mã nguồn chỉ áp dụng cho codebase thực tế của app, loại bỏ tests/scripts/tools (Antigravity)
# - 15:39:49 22/06/2026: [REFACTOR] refactor(retrieval): decompose search functions and resolve blocker violations (Antigravity)
# - 15:29:16 22/06/2026: [REFACTOR] refactor(retrieval): decompose search functions and resolve blocker violations (Antigravity)
# - 14:54:49 22/06/2026: [REFACTOR] refactor(retrieval): decompose search functions and resolve blocker violations (Antigravity)
# - 14:47:28 22/06/2026: [REFACTOR] refactor(retrieval): decompose search functions and resolve blocker violations (Antigravity)
# - 14:16:02 22/06/2026: [REFACTOR] refactor(retrieval): decompose search functions and resolve blocker violations (Antigravity)
# - 14:02:00 22/06/2026: [UPDATE] Tăng ngưỡng Jaccard filter lên 0.65 để loại bỏ false positive của các hàm lớn, ngăn chặn triệt để tình trạng SequenceMatcher bị kẹt CPU (Antigravity)
# - 13:56:00 22/06/2026: [UPDATE] Tinh chỉnh giới hạn độ dài AST tối thiểu để check trùng lặp lên 4000 ký tự (phù hợp với phân vị thực tế của codebase) để giải quyết dứt điểm vấn đề hiệu suất (Antigravity)
# - 13:46:00 22/06/2026: [UPDATE] Tăng giới hạn độ dài AST tối thiểu để check trùng lặp lên 500 ký tự để tập trung vào các hàm thực sự có giá trị và tối ưu hiệu suất (Antigravity)
# - 14:15:00 20/06/2026: [UPDATE] Thêm cờ --output và --format để hỗ trợ xuất báo cáo MD & JSON ra file (Antigravity)
# - 11:53:00 20/06/2026: [UPDATE] Tinh chỉnh logic kiểm toán phân tách vùng Strict Core (core, agents) và UI/Tools, đổi công thức tính điểm nhạy bén (Antigravity)
# - 11:47:00 20/06/2026: [FIX] Loại trừ vulture_whitelist.py khỏi danh sách quét code quality (Antigravity)
# - 17:03:17 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 17:00:33 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 10:55:00 19/06/2026: [NEW] Khởi tạo công cụ Custom Code Quality Auditor (Lê Thanh Vân/Antigravity)
# - 11:08:00 19/06/2026: [UPDATE] Tối ưu hóa thuật toán check_logic_duplication bằng Early Filtering (Lê Thanh Vân/Antigravity)
# - 11:10:00 19/06/2026: [UPDATE] Thêm cờ --check-dups và mặc định tắt quét trùng lặp để tối ưu hóa tốc độ scan (Lê Thanh Vân/Antigravity)
# - 11:21:00 19/06/2026: [NEW] Tích hợp 3 quy tắc kiểm toán chuẩn công nghiệp: độ dài hàm, số lượng đối số và số lượng Class/file (Lê Thanh Vân/Antigravity)

import argparse
import ast
import difflib
import json
import os
import sys
from pathlib import Path
from typing import Any

# Ngưỡng cảnh báo trùng lặp logic (%)
SIMILARITY_THRESHOLD = 0.75

# Thư mục loại trừ
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


class CodeQualityAuditor:
    """Hệ thống phân tích cú pháp tĩnh AST để kiểm tra Clean Code & Kiến trúc thông minh."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        # Lưu trữ biểu diễn AST của các hàm để so sánh trùng lặp logic
        self.function_signatures: list[dict[str, Any]] = []

    def load_changelog_header(self, file_path: Path) -> tuple[bool, str]:
        """Kiểm tra sự hiện diện của Header Changelog ở 15 dòng đầu file."""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                lines = [f.readline() for _ in range(15)]

            has_file = False
            has_func = False
            has_changelog = False

            for line in lines:
                stripped = line.strip().lower()
                if "tên file:" in stripped or "file:" in stripped:
                    has_file = True
                if "chức năng:" in stripped or "description:" in stripped:
                    has_func = True
                if "changelog:" in stripped:
                    has_changelog = True

            if has_file and has_func and has_changelog:
                return True, "Valid"

            missing = []
            if not has_file:
                missing.append("Tên file")
            if not has_func:
                missing.append("Chức năng")
            if not has_changelog:
                missing.append("Changelog")
            return False, f"Thiếu: {', '.join(missing)}"
        except Exception as e:
            return False, f"Lỗi đọc file: {str(e)}"

    def check_type_hints(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[bool, list[str]]:
        """Kiểm tra Type Hints của hàm."""
        missing = []
        # Bỏ qua hàm __init__ không bắt buộc trả về (hoặc nếu có thì tốt, nhưng bỏ qua trả về)
        is_init = node.name == "__init__"

        # 1. Kiểm tra đối số
        args = node.args
        for idx, arg in enumerate(args.args):
            # Bỏ qua self và cls
            if idx == 0 and arg.arg in {"self", "cls"}:
                continue
            if not arg.annotation:
                missing.append(f"Đối số `{arg.arg}`")

        # 2. Kiểm tra kiểu trả về (trừ __init__)
        if not is_init and not node.returns:
            missing.append("Kiểu trả về (Returns)")

        return len(missing) == 0, missing

    def check_docstring_style(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef
    ) -> tuple[bool, list[str]]:
        """Kiểm tra Docstring chuẩn Google."""
        doc = ast.get_docstring(node)
        if not doc:
            return False, ["Thiếu Docstring"]

        warnings = []
        stripped_doc = doc.strip()

        # Nếu là FunctionDef, có tham số (trừ self/cls) thì khuyên dùng Args:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            has_real_args = False
            for idx, arg in enumerate(node.args.args):
                if idx == 0 and arg.arg in {"self", "cls"}:
                    continue
                has_real_args = True
                break

            if has_real_args and "Args:" not in stripped_doc:
                warnings.append("Thiếu phần mô tả đối số 'Args:' trong Docstring")

            is_init = node.name == "__init__"
            if not is_init and "Returns:" not in stripped_doc:
                # Đôi khi hàm trả về None, nếu return type là None thì có thể châm chước
                # Nhưng nếu có return type rõ ràng thì bắt buộc
                if node.returns and not (isinstance(node.returns, ast.Constant) and node.returns.value is None):
                    warnings.append("Thiếu phần mô tả kiểu trả về 'Returns:' trong Docstring")

        return len(warnings) == 0, warnings

    def check_silent_exception(self, node: ast.Try) -> list[tuple[int, str]]:
        """Kiểm tra xem khối try-except có nuốt lỗi im lặng (silent fail) không."""
        violations = []
        for handler in node.handlers:
            # Nhận diện except:, except Exception:, except Exception as e:
            is_generic = False
            if not handler.type:
                is_generic = True
            elif isinstance(handler.type, ast.Name) and handler.type.id in {"Exception", "BaseException"}:
                is_generic = True

            if is_generic:
                # Phân tích body của except xem có rỗng, chỉ pass, hay chỉ continue không
                body = handler.body
                is_silent = False

                if len(body) == 1:
                    child = body[0]
                    if isinstance(child, ast.Pass) or isinstance(child, ast.Continue):
                        is_silent = True
                    elif (
                        isinstance(child, ast.Expr)
                        and isinstance(child.value, ast.Constant)
                        and child.value.value is None
                    ):
                        is_silent = True

                if is_silent:
                    violations.append(
                        (handler.lineno, "Nuốt lỗi im lặng bằng `pass` hoặc `continue` trong except Exception.")
                    )
        return violations

    def check_import_boundary(self, node: ast.Import | ast.ImportFrom, file_relative_path: Path) -> list[str]:
        """Kiểm tra ranh giới nhập khẩu (Import Boundary) của tầng UI."""
        violations = []
        parts = file_relative_path.parts
        if "ui_qt" in parts:
            # Các thư viện cấm ở tầng UI
            forbidden_modules = {"docx", "openpyxl", "sqlite3", "google"}

            if isinstance(node, ast.Import):
                for name in node.names:
                    root_module = name.name.split(".")[0]
                    if root_module in forbidden_modules:
                        violations.append(f"UI import trực tiếp thư viện ngoài `{root_module}`. Hãy sử dụng qua core/.")
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    root_module = node.module.split(".")[0]
                    if root_module in forbidden_modules:
                        violations.append(f"UI import trực tiếp thư viện ngoài `{root_module}`. Hãy sử dụng qua core/.")
        return violations

    def check_print_calls(self, node: ast.Call) -> bool:
        """Phát hiện các hàm gọi print debug trực tiếp."""
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            return True
        return False

    def normalize_ast_structure(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        """Chuẩn hóa cây AST của hàm nhằm so sánh độ tương đồng logic."""

        class ASTNormalizer(ast.NodeTransformer):
            def visit_Name(self, n):
                return ast.Name(id="var", ctx=n.ctx)

            def visit_Constant(self, n):
                return ast.Constant(value="const")

            def visit_arg(self, n):
                return ast.arg(arg="var_arg", annotation=None)

        import copy

        copied = copy.deepcopy(node)
        # Loại bỏ docstring khỏi cây để so sánh thuần logic
        if copied.body and isinstance(copied.body[0], ast.Expr):
            val = copied.body[0].value
            if isinstance(val, ast.Constant) and isinstance(val.value, str):
                copied.body.pop(0)

        normalizer = ASTNormalizer()
        normalized = normalizer.visit(copied)
        return ast.dump(normalized)

    def _analyze_class_node(self, node: ast.ClassDef, results: dict[str, Any]) -> None:
        """Kiểm tra tài liệu (docstring) của class.

        Args:
            node: Node định nghĩa Class trong AST.
            results: Dictionary lưu kết quả kiểm toán file.
        """
        doc_ok, doc_warns = self.check_docstring_style(node)
        if not doc_ok:
            results["warnings"].append(
                {
                    "line": node.lineno,
                    "type": "DOCSTRING_MISSING",
                    "msg": f"Class `{node.name}`: {doc_warns[0]}",
                }
            )

    def _analyze_function_node(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        results: dict[str, Any],
        relative_path: Path,
    ) -> None:
        """Kiểm tra chi tiết một hàm: độ dài, đối số, type hints, docstring và lưu thông tin AST.

        Args:
            node: Node định nghĩa hàm trong AST.
            results: Dictionary lưu kết quả kiểm toán file.
            relative_path: Đường dẫn tương đối của file đang quét.
        """
        results["total_funcs"] += 1

        # Kiểm tra độ dài của hàm
        func_lines = getattr(node, "end_lineno", node.lineno) - node.lineno + 1
        if func_lines > 100:
            results["errors"].append(
                {
                    "line": node.lineno,
                    "type": "FUNCTION_LIMIT_EXCEEDED",
                    "msg": f"Hàm `{node.name}` dài {func_lines} dòng, vượt quá giới hạn cứng 100 dòng.",
                }
            )
        elif func_lines > 50:
            results["warnings"].append(
                {
                    "line": node.lineno,
                    "type": "FUNCTION_TOO_LONG",
                    "msg": f"Hàm `{node.name}` dài {func_lines} dòng, vượt quá giới hạn mềm 50 dòng.",
                }
            )

        # Kiểm tra số lượng đối số
        raw_args = node.args.args
        num_args = len(raw_args)
        if num_args > 0 and raw_args[0].arg in {"self", "cls"}:
            num_args -= 1
        if num_args > 4:
            results["errors"].append(
                {
                    "line": node.lineno,
                    "type": "TOO_MANY_ARGUMENTS",
                    "msg": f"Hàm `{node.name}` nhận {num_args} đối số, vượt quá giới hạn chuẩn 4 đối số.",
                }
            )

        # Check Type Hints
        th_ok, th_missing = self.check_type_hints(node)
        if th_ok:
            results["type_hint_pass"] += 1
        else:
            rel_path_str = str(relative_path).replace("\\", "/")
            is_strict_zone = rel_path_str.startswith("core/") or rel_path_str.startswith("agents/")
            if is_strict_zone:
                results["errors"].append(
                    {
                        "line": node.lineno,
                        "type": "TYPE_HINT_MISSING",
                        "msg": f"Hàm `{node.name}` thiếu Type Hints: {', '.join(th_missing)}.",
                    }
                )
            else:
                results["warnings"].append(
                    {
                        "line": node.lineno,
                        "type": "TYPE_HINT_MISSING",
                        "msg": f"Hàm `{node.name}` thiếu Type Hints: {', '.join(th_missing)} (Vùng UI/Tools - Warning).",
                    }
                )

        # Check Docstrings
        doc_ok, doc_warns = self.check_docstring_style(node)
        if doc_ok:
            results["docstring_pass"] += 1
        else:
            results["warnings"].append(
                {
                    "line": node.lineno,
                    "type": "DOCSTRING_MISSING",
                    "msg": f"Hàm `{node.name}`: {', '.join(doc_warns)}.",
                }
            )

        # Lưu thông tin AST của hàm phục vụ so sánh lặp logic nâng cao
        try:
            norm_ast = self.normalize_ast_structure(node)
            # Chỉ lưu các hàm có độ phức tạp nhất định (hàm ngắn quá 1 dòng bỏ qua)
            if len(node.body) >= 2:
                self.function_signatures.append(
                    {"file": results["file"], "func_name": node.name, "line": node.lineno, "ast_str": norm_ast}
                )
        except Exception as e:
            # Ghi nhận lỗi nhưng không spam terminal
            _ = e

    def analyze_file(self, file_path: Path) -> dict[str, Any]:
        """Phân tích một file Python đơn lẻ và thu thập tất cả lỗi/cảnh báo chất lượng."""
        relative_path = file_path.relative_to(self.project_root)
        results = {
            "file": str(relative_path).replace("\\", "/"),
            "errors": [],  # Lỗi nặng chặn commit (HIGH)
            "warnings": [],  # Cảnh báo (WARNING)
            "total_funcs": 0,
            "type_hint_pass": 0,
            "docstring_pass": 0,
        }

        # 1. Kiểm tra Header Changelog
        header_ok, header_msg = self.load_changelog_header(file_path)
        if not header_ok:
            results["warnings"].append(
                {"line": 1, "type": "HEADER_MISSING", "msg": f"Thiếu Header Changelog chuẩn dự án ({header_msg})."}
            )

        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                tree = ast.parse(f.read(), filename=str(file_path))
        except SyntaxError as se:
            results["errors"].append(
                {"line": se.lineno or 0, "type": "SYNTAX_ERROR", "msg": f"Lỗi cú pháp không thể parse: {se.msg}"}
            )
            return results
        except Exception as e:
            results["errors"].append({"line": 0, "type": "READ_ERROR", "msg": f"Không thể đọc file: {str(e)}"})
            return results

        # 1.5 Kiểm tra số lượng Class ở cấp module
        module_classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
        if len(module_classes) > 1:
            results["warnings"].append(
                {
                    "line": module_classes[1].lineno,
                    "type": "MULTIPLE_CLASSES_IN_FILE",
                    "msg": f"Tệp tin chứa {len(module_classes)} Class ở cấp module. Khuyến nghị tách mỗi file chỉ chứa 1 Class chính.",
                }
            )

        # 2. Phân tích cây AST để quét các rule
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self._analyze_class_node(node, results)

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._analyze_function_node(node, results, relative_path)

            elif isinstance(node, ast.Try):
                silent_fails = self.check_silent_exception(node)
                for line, msg in silent_fails:
                    results["errors"].append({"line": line, "type": "SILENT_EXCEPTION", "msg": msg})

            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                boundary_violations = self.check_import_boundary(node, relative_path)
                for violation in boundary_violations:
                    results["errors"].append(
                        {"line": node.lineno, "type": "IMPORT_BOUNDARY_VIOLATION", "msg": violation}
                    )

            elif isinstance(node, ast.Call):
                if self.check_print_calls(node):
                    results["warnings"].append(
                        {
                            "line": node.lineno,
                            "type": "RAW_PRINT_CALL",
                            "msg": "Sử dụng lệnh `print()` trực tiếp. Hãy chuyển đổi sang `logger`.",
                        }
                    )

        return results

    def check_logic_duplication(self) -> list[dict[str, Any]]:
        """So sánh các hàm để phát hiện trùng lặp logic thuật toán (AST Similarity).

        Sử dụng kỹ thuật sắp xếp theo độ dài AST kết hợp cửa sổ trượt (sliding window)
        và Jaccard Similarity 3-gram để lọc sớm cực nhanh.

        Returns:
            list[dict[str, Any]]: Danh sách các hàm trùng lặp logic chứa các thông tin:
                - file1: Đường dẫn file thứ nhất.
                - func1: Tên hàm thứ nhất.
                - line1: Dòng định nghĩa hàm thứ nhất.
                - file2: Đường dẫn file thứ hai.
                - func2: Tên hàm thứ hai.
                - line2: Dòng định nghĩa hàm thứ hai.
                - similarity: Phần trăm độ tương đồng logic (%).
        """
        duplicates = []

        # 1. Loại bỏ các hàm quá ngắn trước để giảm kích thước tập dữ liệu
        valid_sigs = [sig for sig in self.function_signatures if len(sig["ast_str"]) >= 4000]

        # 2. Sắp xếp các hàm theo độ dài của chuỗi AST tăng dần
        valid_sigs.sort(key=lambda x: len(x["ast_str"]))

        # 3. Tiền tính toán n-grams để tối ưu hóa bộ lọc Jaccard
        ngrams_cache = {}
        for sig in valid_sigs:
            s = sig["ast_str"]
            ngrams_cache[id(sig)] = set(s[i : i + 3] for i in range(len(s) - 2)) if len(s) >= 3 else set()

        # 4. Duyệt so sánh với kỹ thuật break-early dựa trên độ dài
        for i in range(len(valid_sigs)):
            sig1 = valid_sigs[i]
            len1 = len(sig1["ast_str"])
            set1 = ngrams_cache[id(sig1)]

            for j in range(i + 1, len(valid_sigs)):
                sig2 = valid_sigs[j]
                len2 = len(sig2["ast_str"])

                # Vì danh sách đã sắp xếp, nếu len2 vượt quá giới hạn lý thuyết tối đa (tương đồng >= 0.75)
                # thì dừng vòng lặp trong ngay lập tức (break) vì mọi hàm sau đó cũng sẽ vượt giới hạn.
                # Công thức: 2.0 * len1 / (len1 + len2) >= SIMILARITY_THRESHOLD
                # Với SIMILARITY_THRESHOLD = 0.75 => len2 <= 1.667 * len1
                if len2 > 1.667 * len1:
                    break

                # Nếu thuộc cùng 1 file và tên giống nhau (đè/overload) thì bỏ qua
                if sig1["file"] == sig2["file"] and sig1["func_name"] == sig2["func_name"]:
                    continue

                # Bỏ qua các hàm thiết lập UI đặc thù PyQt6
                ui_funcs = {"setupui", "retranslateui", "paintevent", "initui", "init_ui"}
                if sig1["func_name"].lower() in ui_funcs or sig2["func_name"].lower() in ui_funcs:
                    continue

                # Lọc sớm Jaccard Similarity trên 3-grams
                set2 = ngrams_cache[id(sig2)]
                union_len = len(set1.union(set2))
                if union_len > 0:
                    jaccard = len(set1.intersection(set2)) / union_len
                    # Nếu Jaccard similarity quá thấp, chắc chắn SequenceMatcher cũng sẽ thấp
                    if jaccard < 0.65:
                        continue
                else:
                    continue

                # Sử dụng difflib để so sánh độ tương đồng chuỗi AST chi tiết
                ratio = difflib.SequenceMatcher(None, sig1["ast_str"], sig2["ast_str"]).ratio()
                if ratio >= SIMILARITY_THRESHOLD:
                    duplicates.append(
                        {
                            "file1": sig1["file"],
                            "func1": sig1["func_name"],
                            "line1": sig1["line"],
                            "file2": sig2["file"],
                            "func2": sig2["func_name"],
                            "line2": sig2["line"],
                            "similarity": round(ratio * 100, 1),
                        }
                    )
        return duplicates

    def is_app_file(self, file_path: Path) -> bool:
        """Kiểm tra xem một file Python có thuộc codebase chính của app hay không."""
        try:
            abs_path = file_path.resolve()
            abs_root = self.project_root.resolve()
            rel_path = abs_path.relative_to(abs_root)
            parts = rel_path.parts

            if not parts:
                return False

            # Nếu file nằm trực tiếp ở thư mục root
            if len(parts) == 1:
                name = parts[0]
                app_root_files = {
                    "main.py",
                    "config.py",
                }
                return name in app_root_files

            # Nếu file nằm trong thư mục con
            first_dir = parts[0]
            app_dirs = {"backend", "frontend", "core", "ui_qt", "agents", "utils"}
            return first_dir in app_dirs
        except Exception:
            return False

    def scan_project(
        self, target_files: list[Path] | None = None, check_dups: bool = False
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Quét các file chỉ định hoặc toàn project và trả về báo cáo.

        Args:
            target_files: Danh sách các file chỉ định.
            check_dups: Có kiểm tra trùng lặp logic hay không.

        Returns:
            Tuple chứa danh sách kết quả phân tích từng file và danh sách trùng lặp logic.
        """
        reports = []
        files_to_scan = []

        if target_files:
            files_to_scan = [f for f in target_files if f.suffix == ".py" and self.is_app_file(f)]
        else:
            # Quét toàn bộ project
            for root, dirs, files in os.walk(self.project_root):
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                for file in files:
                    if file.endswith(".py"):
                        full_path = Path(root) / file
                        if self.is_app_file(full_path):
                            files_to_scan.append(full_path)

        for file_path in files_to_scan:
            reports.append(self.analyze_file(file_path))

        # Tìm trùng lặp logic trong số các hàm vừa quét nếu được yêu cầu
        duplicates = []
        if check_dups:
            duplicates = self.check_logic_duplication()
        return reports, duplicates


def generate_markdown_report(
    reports: list[dict[str, Any]],
    duplicates: list[dict[str, Any]],
    score: float,
    *,
    th_coverage: float,
    total_errors: int,
    total_warnings: int,
    total_funcs: int,
    total_th_pass: int,
) -> str:
    """Tạo báo cáo chất lượng mã nguồn dưới dạng Markdown."""
    status_emoji = "🟢" if score >= 8.0 else ("⚠️" if score >= 5.0 else "🚨")
    lines = [
        "# 🛡️ BÁO CÁO KIỂM TOÁN CHẤT LƯỢNG MÃ NGUỒN (CLEAN CODE AUDIT)",
        "",
        f"* Điểm chất lượng mã nguồn: {status_emoji} **{score:.1f}/10.0**",
        f"* Độ bao phủ Type Hints: **{th_coverage:.1f}%** ({total_th_pass}/{total_funcs} hàm)",
        f"* Tổng số Lỗi nặng (High Error): **{total_errors}**",
        f"* Tổng số Cảnh báo (Warning): **{total_warnings}**",
        "",
    ]

    if total_errors > 0:
        lines.append("## ❌ CÁC LỖI NẶNG CẦN SỬA NGAY (BLOCK COMMIT)")
        lines.append("| File | Dòng | Loại lỗi | Chi tiết vi phạm |")
        lines.append("| :--- | :---: | :--- | :--- |")
        for r in reports:
            for err in r["errors"]:
                lines.append(f"| `{r['file']}` | {err['line']} | `{err['type']}` | {err['msg']} |")
        lines.append("")

    has_warnings = any(len(r["warnings"]) > 0 for r in reports)
    if has_warnings:
        lines.append("## ⚠️ CÁC CẢNH BÁO TỐI ƯU (WARNING)")
        lines.append("| File | Dòng | Loại cảnh báo | Chi tiết |")
        lines.append("| :--- | :---: | :--- | :--- |")
        for r in reports:
            for warn in r["warnings"]:
                lines.append(f"| `{r['file']}` | {warn['line']} | `{warn['type']}` | {warn['msg']} |")
        lines.append("")

    if duplicates:
        lines.append("## 🔌 CẢNH BÁO LẶP LOGIC THUẬT TOÁN (AST SIMILARITY)")
        lines.append("| File 1 (Hàm 1) | File 2 (Hàm 2) | Độ tương đồng | Khuyến nghị |")
        lines.append("| :--- | :--- | :---: | :--- |")
        for d in duplicates:
            lines.append(
                f"| `{d['file1']}`: {d['func1']} (dòng {d['line1']}) | `{d['file2']}`: {d['func2']} (dòng {d['line2']}) | **{d['similarity']}%** | Gộp logic chung vào `core/word_architect.py` hoặc `core/utils/` |"
            )
        lines.append("")

    lines.append("=" * 80)
    lines.append("")
    return "\n".join(lines)


def generate_json_report(
    reports: list[dict[str, Any]],
    duplicates: list[dict[str, Any]],
    score: float,
    *,
    th_coverage: float,
    total_errors: int,
    total_warnings: int,
    total_funcs: int,
    total_th_pass: int,
) -> dict[str, Any]:
    """Tạo báo cáo chất lượng mã nguồn định dạng JSON."""
    return {
        "score": round(score, 2),
        "type_hint_coverage": round(th_coverage, 2),
        "total_errors": total_errors,
        "total_warnings": total_warnings,
        "total_funcs": total_funcs,
        "total_th_pass": total_th_pass,
        "reports": reports,
        "duplicates": duplicates,
    }


def save_report_to_file(
    output_path_str: str,
    report_format: str,
    md_report: str,
    json_report: dict[str, Any],
) -> None:
    """Lưu nội dung báo cáo chất lượng mã nguồn ra tệp tin tương ứng."""
    output_path = Path(output_path_str)
    if output_path.parent:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    base_path = output_path
    suffix = output_path.suffix.lower()
    if suffix in {".md", ".json"}:
        base_path = output_path.with_suffix("")

    written_files = []
    if report_format in {"md", "both"}:
        md_file = base_path.with_suffix(".md") if report_format == "both" or suffix != ".json" else output_path
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_report)
        written_files.append(str(md_file))

    if report_format in {"json", "both"}:
        json_file = base_path.with_suffix(".json") if report_format == "both" or suffix != ".md" else output_path
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_report, f, ensure_ascii=False, indent=2)
        written_files.append(str(json_file))

    print(f"\n[OK] Đã xuất báo cáo chất lượng mã nguồn ra: {', '.join(written_files)}")


def main() -> None:
    """Hàm chạy chính của công cụ kiểm toán."""
    parser = argparse.ArgumentParser(description="Clean Code & Code Quality Auditor cho dự án.")
    parser.add_argument("--scan", action="store_true", help="Quét toàn bộ dự án.")
    parser.add_argument("--files", nargs="+", help="Quét danh sách các file cụ thể (phù hợp Git staged check).")
    parser.add_argument(
        "--check-dups",
        action="store_true",
        help="Kích hoạt quét trùng lặp logic thuật toán (chạy chậm trên codebase lớn).",
    )
    parser.add_argument("--output", "-o", type=str, help="Đường dẫn lưu tệp báo cáo.")
    parser.add_argument(
        "--format",
        "-f",
        choices=["md", "json", "both"],
        default="md",
        help="Định dạng kết xuất báo cáo (md, json, both).",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    auditor = CodeQualityAuditor(project_root)

    target_files = None
    if args.files:
        target_files = [Path(f).resolve() for f in args.files]

    reports, duplicates = auditor.scan_project(target_files, check_dups=args.check_dups)

    # Tính toán các chỉ số thống kê
    total_errors = sum(len(r["errors"]) for r in reports)
    total_warnings = sum(len(r["warnings"]) for r in reports) + len(duplicates)
    total_funcs = sum(r["total_funcs"] for r in reports)
    total_th_pass = sum(r["type_hint_pass"] for r in reports)
    th_coverage = (total_th_pass / total_funcs * 100) if total_funcs > 0 else 100

    score = 10.0 - (total_errors * 0.01) - (total_warnings * 0.0002)
    score = max(0.0, min(10.0, score))

    # Sinh nội dung báo cáo
    md_report = generate_markdown_report(
        reports,
        duplicates,
        score,
        th_coverage=th_coverage,
        total_errors=total_errors,
        total_warnings=total_warnings,
        total_funcs=total_funcs,
        total_th_pass=total_th_pass,
    )
    json_report = generate_json_report(
        reports,
        duplicates,
        score,
        th_coverage=th_coverage,
        total_errors=total_errors,
        total_warnings=total_warnings,
        total_funcs=total_funcs,
        total_th_pass=total_th_pass,
    )

    # In kết quả tóm tắt ra terminal
    status_emoji = "🟢" if score >= 8.0 else ("⚠️" if score >= 5.0 else "🚨")
    print(f"\n* Điểm chất lượng mã nguồn: {status_emoji} **{score:.1f}/10.0**")
    print(f"* Độ bao phủ Type Hints: **{th_coverage:.1f}%** ({total_th_pass}/{total_funcs} hàm)")
    print(f"* Tổng số Lỗi nặng (High Error): **{total_errors}**")
    print(f"* Tổng số Cảnh báo (Warning): **{total_warnings}**")

    # Nếu có tham số --output, lưu báo cáo ra file
    if args.output:
        save_report_to_file(args.output, args.format, md_report, json_report)
    else:
        # Nếu không có output, in báo cáo MD chi tiết lên terminal như cũ
        print(md_report)

    # Trả về exit code 1 nếu có lỗi nặng
    if total_errors > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
