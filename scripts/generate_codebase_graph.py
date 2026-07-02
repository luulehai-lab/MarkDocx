# Tên file: scripts/generate_codebase_graph.py
# CHỨC NĂNG: Quét codebase bằng AST, xây dựng đồ thị tri thức (JSON/Mermaid) hỗ trợ Incremental Cache siêu tốc và phân tích tác động.
# CHANGELOG:
# - 14:55:00 02/07/2026: [UPDATE] Cập nhật đồ thị và Mermaid export sang backend/frontend của dự án Markdown Viewer (Lê Thanh Vân/Antigravity)
# - 11:49:13 02/07/2026: [NEW] Cập nhật mã nguồn (Antigravity)
# - 17:03:17 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 17:00:33 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 18:00:00 28/05/2026: [UPDATE] Tích hợp cơ chế Incremental Cache tối ưu tốc độ quét dưới 0.3s (Lê Thanh Vân/Antigravity)
# - 17:45:00 28/05/2026: [NEW] Tích hợp công cụ Đồ thị Codebase cho AI Assistant (Lê Thanh Vân/Antigravity)

import argparse
import ast
import json
from pathlib import Path
from typing import Any


class CodebaseParser(ast.NodeVisitor):
    """
    Bộ phân tích cú pháp AST của từng file Python để trích xuất các thực thể và mối quan hệ.
    """

    def __init__(self, file_path: Path, project_root: Path) -> None:
        self.file_path = file_path
        self.project_root = project_root
        relative_path = file_path.relative_to(project_root)
        self.module_name = ".".join(relative_path.with_suffix("").parts)

        self.current_class: str | None = None
        self.current_function: str | None = None

        # Dữ liệu trích xuất
        self.imports: list[dict[str, Any]] = []
        self.classes: list[dict[str, Any]] = []
        self.functions: list[dict[str, Any]] = []
        self.calls: list[dict[str, Any]] = []

    def visit_Import(self, node: ast.Import) -> None:
        """Trích xuất import trực tiếp dạng 'import x'."""
        for alias in node.names:
            self.imports.append({"type": "direct", "name": alias.name, "asname": alias.asname, "line": node.lineno})
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Trích xuất import dạng 'from x import y'."""
        if node.module:
            module_name = node.module
            if node.level > 0:
                parts = self.file_path.parent.relative_to(self.project_root).parts
                if node.level <= len(parts):
                    base = ".".join(parts[: len(parts) - node.level + 1])
                    module_name = f"{base}.{module_name}" if base else module_name

            for alias in node.names:
                self.imports.append(
                    {
                        "type": "from",
                        "module": module_name,
                        "name": alias.name,
                        "asname": alias.asname,
                        "line": node.lineno,
                    }
                )
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Ghi nhận định nghĩa Class và các Class cha kế thừa."""
        class_id = f"{self.module_name}.{node.name}"
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(f"{self.visit_Attribute_name(base)}")

        self.classes.append(
            {
                "id": class_id,
                "name": node.name,
                "bases": bases,
                "line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno),
            }
        )

        old_class = self.current_class
        self.current_class = class_id
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Ghi nhận định nghĩa Function/Method."""
        func_name = node.name
        if self.current_class:
            func_id = f"{self.current_class}.{func_name}"
            parent_type = "class"
            parent_id = self.current_class
        else:
            func_id = f"{self.module_name}.{func_name}"
            parent_type = "module"
            parent_id = self.module_name

        args_hints = {}
        for arg in node.args.args:
            if arg.annotation:
                args_hints[arg.arg] = self.get_annotation_str(arg.annotation)

        return_hint = None
        if node.returns:
            return_hint = self.get_annotation_str(node.returns)

        self.functions.append(
            {
                "id": func_id,
                "name": func_name,
                "parent_id": parent_id,
                "parent_type": parent_type,
                "args": list(args_hints.keys()),
                "args_hints": args_hints,
                "return_hint": return_hint,
                "line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno),
            }
        )

        old_func = self.current_function
        self.current_function = func_id
        self.generic_visit(node)
        self.current_function = old_func

    def visit_Call(self, node: ast.Call) -> None:
        """Ghi nhận cuộc gọi hàm."""
        call_name = ""
        caller_obj = None

        if isinstance(node.func, ast.Name):
            call_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            call_name = node.func.attr
            caller_obj = self.visit_Attribute_name(node.func.value)

        if self.current_function:
            self.calls.append(
                {"caller": self.current_function, "call_name": call_name, "caller_obj": caller_obj, "line": node.lineno}
            )
        self.generic_visit(node)

    def visit_Attribute_name(self, node: ast.AST) -> str:
        """Đệ quy lấy tên đầy đủ của Attribute (e.g. self.takeoff_repo)."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self.visit_Attribute_name(node.value)}.{node.attr}"
        return ""

    def get_annotation_str(self, node: ast.AST) -> str:
        """Chuyển đổi node Type Hint thành chuỗi trực quan."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self.visit_Attribute_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            value = self.get_annotation_str(node.value)
            slice_val = self.get_annotation_str(node.slice)
            return f"{value}[{slice_val}]"
        elif isinstance(node, ast.Tuple):
            return f"Tuple[{', '.join(self.get_annotation_str(e) for e in node.elts)}]"
        elif isinstance(node, ast.Constant):
            return str(node.value)
        return "Any"


class CodebaseGraph:
    """
    Quản lý Đồ thị Tri thức (Nodes & Edges), kết nối các thực thể và phân tích tác động.
    """

    def __init__(self) -> None:
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: list[dict[str, str]] = []
        self.adjacency_list: dict[str, set[str]] = {}  # Đồ thị xuôi
        self.reverse_adjacency_list: dict[str, set[str]] = {}  # Đồ thị ngược để tìm Impact

    def add_node(self, node_id: str, label: str, node_type: str, **kwargs: Any) -> None:
        self.nodes[node_id] = {"id": node_id, "label": label, "type": node_type, **kwargs}

    def add_edge(self, source: str, target: str, edge_type: str) -> None:
        edge = {"source": source, "target": target, "type": edge_type}
        if edge not in self.edges:
            self.edges.append(edge)

            if source not in self.adjacency_list:
                self.adjacency_list[source] = set()
            self.adjacency_list[source].add(target)

            if target not in self.reverse_adjacency_list:
                self.reverse_adjacency_list[target] = set()
            self.reverse_adjacency_list[target].add(source)

    def resolve_relationships(self, parsers_data: list[dict[str, Any]]) -> None:
        """
        Kết hợp dữ liệu từ tất cả file đã parse (hoặc load từ cache) để tạo liên kết đồ thị logic.
        """
        # Bước 1: Tạo các node File, Class và Function định nghĩa sẵn
        for pdata in parsers_data:
            module_name = pdata["module_name"]
            file_path = pdata["file_path"]
            self.add_node(module_name, Path(file_path).name, "file", file_path=file_path)

            for cls in pdata["classes"]:
                self.add_node(cls["id"], cls["name"], "class", file_path=file_path, line=cls["line"])
                self.add_edge(module_name, cls["id"], "contains")

                # Liên kết kế thừa (Inheritance)
                for base in cls["bases"]:
                    resolved_base = self._resolve_class_by_name_from_data(base, pdata)
                    if resolved_base:
                        self.add_edge(cls["id"], resolved_base, "inherits_from")

            for func in pdata["functions"]:
                self.add_node(func["id"], func["name"], "function", file_path=file_path, line=func["line"])
                self.add_edge(func["parent_id"], func["id"], "contains")

        # Bước 2: Phân tích các lệnh gọi hàm (Calls) để tạo các cạnh CALLS
        for pdata in parsers_data:
            for call in pdata["calls"]:
                caller_id = call["caller"]
                call_name = call["call_name"]
                caller_obj = call["caller_obj"]

                target_id = self._resolve_call_target_from_data(call_name, caller_obj, pdata)
                if target_id:
                    self.add_edge(caller_id, target_id, "calls")

    def _resolve_class_by_name_from_data(self, class_name: str, pdata: dict[str, Any]) -> str | None:
        """Tìm ID đầy đủ của Class dựa trên tên gọi và danh sách imports của file tương ứng."""
        # 1. Tìm trong chính file hiện tại
        local_id = f"{pdata['module_name']}.{class_name}"
        if local_id in self.nodes:
            return local_id

        # 2. Tìm qua các imports
        for imp in pdata["imports"]:
            if imp["type"] == "from" and imp["name"] == class_name:
                target_module = imp["module"]
                return f"{target_module}.{class_name}"
            elif imp["type"] == "direct" and imp["asname"] == class_name:
                return imp["name"]
            elif imp["type"] == "direct" and imp["name"].endswith(f".{class_name}"):
                return imp["name"]

        # 3. Quét toàn bộ đồ thị xem có Class nào trùng tên độc nhất không
        matches = [nid for nid, node in self.nodes.items() if node["type"] == "class" and node["label"] == class_name]
        if len(matches) == 1:
            return matches[0]

        return None

    def _resolve_call_target_from_data(
        self, call_name: str, caller_obj: str | None, pdata: dict[str, Any]
    ) -> str | None:
        """Dựa trên Type Hints hoặc quy tắc cấu trúc để suy luận phương thức đích từ data trích xuất."""
        # caller_id là hàm chứa cuộc gọi hiện tại
        caller_func = next((f for f in pdata["functions"] if f["id"] == pdata.get("current_function")), None)
        caller_id = caller_func["id"] if caller_func else pdata["module_name"]

        # Trường hợp 1: self.method()
        if caller_obj == "self":
            # Tìm class hiện tại chứa caller
            current_class = None
            for cls in pdata["classes"]:
                if caller_id.startswith(f"{cls['id']}."):
                    current_class = cls["id"]
                    break

            if current_class:
                target_id = f"{current_class}.{call_name}"
                if target_id in self.nodes:
                    return target_id

                # Kiểm tra xem có kế thừa từ class cha nào không
                cls_node = next((c for c in pdata["classes"] if c["id"] == current_class), None)
                if cls_node:
                    for base in cls_node["bases"]:
                        base_id = self._resolve_class_by_name_from_data(base, pdata)
                        if base_id:
                            parent_target = f"{base_id}.{call_name}"
                            if parent_target in self.nodes:
                                return parent_target

        # Trường hợp 2: Biến nội bộ có Type Hint rõ ràng trong hàm gọi
        if caller_obj:
            caller_func = next((f for f in pdata["functions"] if f["id"] == caller_id), None)
            if caller_func and caller_obj in caller_func.get("args_hints", {}):
                hint = caller_func["args_hints"][caller_obj]
                class_id = self._resolve_class_by_name_from_data(hint, pdata)
                if class_id:
                    target_id = f"{class_id}.{call_name}"
                    if target_id in self.nodes:
                        return target_id

        # Trường hợp 3: Gọi hàm tự do được import trực tiếp
        resolved_func = self._resolve_class_by_name_from_data(call_name, pdata)
        if resolved_func and resolved_func in self.nodes:
            return resolved_func

        # Trường hợp 4: Quét toàn bộ đồ thị tìm Method trùng tên độc nhất
        matches = [nid for nid, node in self.nodes.items() if node["type"] == "function" and node["label"] == call_name]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1 and caller_obj:
            for match in matches:
                if caller_obj.lower() in match.lower():
                    return match

        return None

    def find_impact(self, target_node_id: str) -> list[dict[str, Any]]:
        """
        Tìm kiếm ngược (BFS) trên đồ thị để tìm tất cả thực thể bị ảnh hưởng trực tiếp/gián tiếp.
        """
        if target_node_id not in self.nodes:
            return []

        visited: set[str] = set()
        queue: list[str] = [target_node_id]
        impact_chain: list[dict[str, Any]] = []

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            callers = self.reverse_adjacency_list.get(current, set())
            for caller in callers:
                if caller not in visited and caller not in queue:
                    queue.append(caller)
                    edge_type = "calls"
                    for edge in self.edges:
                        if edge["source"] == caller and edge["target"] == current:
                            edge_type = edge["type"]
                            break

                    impact_chain.append(
                        {"node": self.nodes[caller], "impact_on": self.nodes[current]["id"], "relation": edge_type}
                    )

        return impact_chain


class GraphExporter:
    """
    Xuất dữ liệu đồ thị sang JSON hoặc Markdown Mermaid.
    """

    def __init__(self, graph: CodebaseGraph) -> None:
        self.graph = graph

    def to_json(self, output_path: Path, files_cache: dict[str, Any]) -> None:
        """Xuất toàn bộ đồ thị và tệp cache vào JSON."""
        data = {"nodes": list(self.graph.nodes.values()), "edges": self.graph.edges, "_files_cache": files_cache}
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def to_mermaid(self, focus_modules: list[str] | None = None) -> str:
        """Tạo mã Mermaid TD. Có thể lọc theo các module để giữ sơ đồ gọn gàng."""
        lines = ["graph TD"]
        lines.append("    classDef file fill:#f9f,stroke:#333,stroke-width:1px;")
        lines.append("    classDef cls fill:#bbf,stroke:#333,stroke-width:1px;")
        lines.append("    classDef func fill:#bfb,stroke:#333,stroke-width:1px;")

        filtered_nodes = {}
        for nid, node in self.graph.nodes.items():
            if focus_modules:
                match = False
                for mod in focus_modules:
                    if nid.startswith(mod):
                        match = True
                        break
                if not match:
                    continue
            filtered_nodes[nid] = node

        for nid, node in filtered_nodes.items():
            label = node["label"]
            ntype = node["type"]
            safe_id = nid.replace(".", "_").replace("/", "_").replace("-", "_")

            if ntype == "file":
                lines.append(f'    {safe_id}["📄 {label}"]:::file')
            elif ntype == "class":
                lines.append(f'    {safe_id}["🧩 {label}"]:::cls')
            elif ntype == "function":
                lines.append(f'    {safe_id}["⚙️ {label}()"]:::func')

        for edge in self.graph.edges:
            src, tgt, etype = edge["source"], edge["target"], edge["type"]
            if src in filtered_nodes and tgt in filtered_nodes:
                src_safe = src.replace(".", "_").replace("/", "_").replace("-", "_")
                tgt_safe = tgt.replace(".", "_").replace("/", "_").replace("-", "_")

                if etype == "contains":
                    lines.append(f"    {src_safe} -->|contains| {tgt_safe}")
                elif etype == "calls":
                    lines.append(f"    {src_safe} ==>|calls| {tgt_safe}")
                elif etype == "inherits_from":
                    lines.append(f"    {src_safe} -.->|inherits| {tgt_safe}")

        return "\n".join(lines)


def scan_codebase_incremental(project_root: Path, cache_path: Path) -> tuple[CodebaseGraph, dict[str, Any]]:
    """
    Quét codebase hỗ trợ Incremental Cache:
    Chỉ parse AST những file đã bị chỉnh sửa mới, giữ lại dữ liệu cũ cho các file không đổi.
    """
    files_cache = {}

    # 1. Đọc cache cũ nếu tồn tại
    if cache_path.exists():
        try:
            with open(cache_path, encoding="utf-8") as f:
                old_data = json.load(f)
                files_cache = old_data.get("_files_cache", {})
                print(f"📦 Đã tìm thấy cache đồ thị hiện tại ({len(files_cache)} files).")
        except Exception as e:
            print(f"⚠️ Không thể load cache đồ thị cũ: {e}. Quét lại từ đầu.")

    exclude_dirs = {
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
    }

    parsers_data = []
    scanned_count = 0
    cached_count = 0

    # 2. Duyệt codebase và cập nhật động
    for py_file in project_root.glob("**/*.py"):
        if any(ex in py_file.parts for ex in exclude_dirs):
            continue
        if py_file.name.startswith("test_"):
            continue

        relative_path = py_file.relative_to(project_root)
        module_name = ".".join(relative_path.with_suffix("").parts)

        try:
            file_mtime = py_file.stat().st_mtime

            # Kiểm tra xem có cache hợp lệ không
            if module_name in files_cache and files_cache[module_name].get("mtime") == file_mtime:
                # Đọc trực tiếp từ cache cũ!
                parsers_data.append(files_cache[module_name])
                cached_count += 1
            else:
                # Parse AST file mới
                with open(py_file, encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=str(py_file))

                parser = CodebaseParser(py_file, project_root)
                parser.visit(tree)

                # Đóng gói dữ liệu trích xuất dạng JSON dict
                pdata = {
                    "module_name": parser.module_name,
                    "file_path": str(relative_path).replace("\\", "/"),
                    "mtime": file_mtime,
                    "imports": parser.imports,
                    "classes": parser.classes,
                    "functions": parser.functions,
                    "calls": parser.calls,
                }

                # Cập nhật cache
                files_cache[module_name] = pdata
                parsers_data.append(pdata)
                scanned_count += 1
        except Exception as e:
            print(f"⚠️ Không thể parse file {py_file}: {e}")

    print(f"⚡ Tối ưu hóa: Phân tích AST {scanned_count} files thay đổi. Đọc nhanh từ Cache {cached_count} files.")

    # 3. Dựng đồ thị
    graph = CodebaseGraph()
    graph.resolve_relationships(parsers_data)
    return graph, files_cache


def main() -> None:
    parser = argparse.ArgumentParser(description="Công cụ quét Codebase dạng Graph siêu tốc cho AI Assistant.")
    parser.add_argument("--scan", action="store_true", help="Quét codebase cập nhật đồ thị bằng Incremental Cache.")
    parser.add_argument("--impact", type=str, help="Truy vết tác động sửa đổi của thực thể.")
    parser.add_argument("--mermaid", type=str, help="Lọc module xuất sơ đồ Mermaid.")

    args = parser.parse_args()
    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "docs" / "architecture"
    json_path = output_dir / "codebase_graph.json"

    if args.scan:
        print("🔄 Đang quét codebase AI Assistant...")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Gọi quét Incremental Cache!
        graph, files_cache = scan_codebase_incremental(project_root, json_path)

        # 1. Lưu file JSON đồ thị kèm Cache
        exporter = GraphExporter(graph)
        exporter.to_json(json_path, files_cache)
        print(f"💾 Đã lưu đồ thị và cache: {json_path}")

        # 2. Tạo sơ đồ Mermaid cho các module chính của Markdown Viewer
        core_mermaid = exporter.to_mermaid(["backend", "main", "config"])
        ui_mermaid = exporter.to_mermaid(["frontend"])

        # 3. Ghi vào file MAP_GRAPH.md
        map_graph_path = output_dir / "MAP_GRAPH.md"
        with open(map_graph_path, "w", encoding="utf-8") as f:
            f.write(f"""<!--
File: docs/architecture/MAP_GRAPH.md
Description: 🌐 ĐỒ THỊ LIÊN KẾT CODEBASE MARKDOWN VIEWER
CHANGELOG:
- 14:55:00 02/07/2026: [UPDATE] Cập nhật đồ thị sang backend/frontend của dự án Markdown Viewer (Lê Thanh Vân/Antigravity)
-->

# 🌐 ĐỒ THỊ LIÊN KẾT CODEBASE MARKDOWN VIEWER

> [!TIP]
> Tài liệu này được tự động cập nhật bằng cơ chế **Incremental Cache** siêu tốc.
> Giúp hình dung rõ ràng mối liên kết gọi hàm và kế thừa trong toàn bộ hệ thống Markdown Viewer.

---

## 💾 1. Đồ thị liên kết Backend & Core (Phân tích cú pháp Markdown, Latex, Mermaid)
```mermaid
{core_mermaid}
```

---

## 🎨 2. Đồ thị liên kết Frontend PyQt6 (Giao diện Markdown Viewer)
```mermaid
{ui_mermaid}
```
""")
        print(f"📝 Đã tạo/cập nhật tài liệu đồ thị: {map_graph_path}")
        print("✅ Hoàn thành quét codebase thành công!")

    elif args.impact:
        # Load đồ thị từ cache JSON để chạy lập tức (tốc độ dưới 0.1s!)
        if not json_path.exists():
            print("⚠️ File đồ thị chưa tồn tại. Vui lòng chạy quét `--scan` trước.")
            return

        try:
            with open(json_path, encoding="utf-8") as f:
                graph_data = json.load(f)
                files_cache = graph_data.get("_files_cache", {})
                parsers_data = list(files_cache.values())
        except Exception as e:
            print(f"⚠️ Lỗi đọc cache: {e}. Đang quét trực tiếp...")
            graph, files_cache = scan_codebase_incremental(project_root, json_path)
            parsers_data = list(files_cache.values())

        graph = CodebaseGraph()
        graph.resolve_relationships(parsers_data)

        target = args.impact
        if target not in graph.nodes:
            matches = [nid for nid in graph.nodes if target in nid]
            if not matches:
                print(f"❌ Không tìm thấy thực thể nào khớp với: {target}")
                return
            elif len(matches) == 1:
                target = matches[0]
            else:
                print("❓ Tìm thấy nhiều thực thể khớp, vui lòng nhập chính xác:")
                for m in matches[:10]:
                    print(f"  - {m}")
                return

        print(f"🔍 Đang truy vết tác động khi thay đổi: {target} ({graph.nodes[target]['type']})")
        impacts = graph.find_impact(target)
        if not impacts:
            print("🟢 Tuyệt vời! Không phát hiện ảnh hưởng trực tiếp nào đến các module khác.")
        else:
            print(f"⚠️ Phát hiện {len(impacts)} điểm bị ảnh hưởng trực tiếp/gián tiếp:")
            print(f"{'Thực thể bị ảnh hưởng':<70} | {'Mối quan hệ':<12} | {'Chi tiết file'}")
            print("-" * 120)
            for imp in impacts:
                node = imp["node"]
                rel = imp["relation"].upper()
                file_info = f"{node.get('file_path', 'unknown')}:{node.get('line', '')}"
                print(f"{node['id']:<70} | {rel:<12} | {file_info}")

    elif args.mermaid:
        if not json_path.exists():
            print("⚠️ File đồ thị chưa tồn tại. Vui lòng chạy quét `--scan` trước.")
            return
        with open(json_path, encoding="utf-8") as f:
            graph_data = json.load(f)
            files_cache = graph_data.get("_files_cache", {})
            parsers_data = list(files_cache.values())

        graph = CodebaseGraph()
        graph.resolve_relationships(parsers_data)

        exporter = GraphExporter(graph)
        modules = args.mermaid.split(",")
        print(exporter.to_mermaid(modules))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
