# Tên file: frontend/components/parser_thread.py
# CHỨC NĂNG: Khai báo lớp luồng phụ QThread để biên dịch Markdown bất đồng bộ.
# CHANGELOG:
# - 15:11:00 02/07/2026: [NEW] Khởi tạo module tách từ main_window.py (Lê Thanh Vân/Antigravity)

from PyQt6.QtCore import QThread, pyqtSignal
from backend.md_parser import render_markdown_to_html

class MarkdownParserThread(QThread):
    """Luồng phụ QThread để chạy render markdown bất đồng bộ, tránh đơ UI."""
    parse_done = pyqtSignal(dict)  # Trả về dict chứa HTML và TOC
    error_occurred = pyqtSignal(str)

    def __init__(self, filepath: str, is_dark: bool = False) -> None:
        """Khởi tạo luồng parser.

        Args:
            filepath: Đường dẫn đến file Markdown.
            is_dark: Cờ sử dụng giao diện tối.
        """
        super().__init__()
        self.filepath = filepath
        self.is_dark = is_dark

    def run(self) -> None:
        """Thực thi biên dịch Markdown bất đồng bộ."""
        try:
            data = render_markdown_to_html(self.filepath, self.is_dark)
            self.parse_done.emit(data)
        except Exception as e:
            self.error_occurred.emit(str(e))
