# Tên file: frontend/components/search_panel.py
# CHỨC NĂNG: Thành quan hiển thị kết quả tìm kiếm Notepad++ style (SearchResultPanel).
# CHANGELOG:
# - 15:22:00 02/07/2026: [DOCS] Phủ đầy đủ Google Docstring cho on_item_clicked (Antigravity)
# - 15:13:00 02/07/2026: [NEW] Khởi tạo search_panel component tách từ main_window.py (Lê Thanh Vân/Antigravity)

import re
import html
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QLabel, QWidget
from PyQt6.QtCore import Qt, pyqtSignal

class SearchResultPanel(QListWidget):
    """Panel hiển thị kết quả tìm kiếm Notepad++ Style với Rich Text highlight."""
    # Tín hiệu gửi sang MainWindow: (số dòng, vị trí cursor)
    item_selected = pyqtSignal(int, int)

    def __init__(self, parent: QWidget | None = None) -> None:
        """Khởi tạo panel kết quả tìm kiếm.

        Args:
            parent: Widget cha.
        """
        super().__init__(parent)
        self.itemClicked.connect(self.on_item_clicked)
        self.setAlternatingRowColors(True)
        self.is_dark = False
        self.setStyleSheet("""
            QListWidget { font-family: 'Consolas', 'Courier New'; font-size: 10pt; border: none; }
        """)

    def add_result(self, line_num: int, text_snippet: str, pos: int, search_term: str) -> None:
        """Thêm một dòng kết quả tìm kiếm vào danh sách.

        Args:
            line_num: Số dòng trong văn bản.
            text_snippet: Đoạn văn bản chứa từ khóa.
            pos: Vị trí của con trỏ.
            search_term: Từ khóa tìm kiếm để highlight.
        """
        # 1. Tạo item ảo để giữ chỗ trong list
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, (line_num, pos))
        self.addItem(item)
        
        # 2. Xử lý HTML highlight (Case-insensitive)
        escaped_snippet = html.escape(text_snippet.strip())
        # Tạo màu highlight: Vàng tươi cho Sáng, Cam đậm cho Tối để dễ nhìn
        hl_bg = "#fff200" if not self.is_dark else "#d4a017"
        hl_fg = "#000000"
        
        pattern = re.compile(re.escape(search_term), re.IGNORECASE)
        highlighted = pattern.sub(
            f"<span style='background-color: {hl_bg}; color: {hl_fg}; font-weight: bold;'>\\g<0></span>", 
            escaped_snippet
        )
        
        # 3. Tạo Label chứa Rich Text
        lbl = QLabel()
        line_color = "#0078d4" if not self.is_dark else "#58a6ff"
        display_text = f"<b style='color: {line_color};'>Dòng {line_num:<5}</b> | {highlighted}"
        lbl.setText(display_text)
        lbl.setContentsMargins(10, 5, 10, 5)
        
        # 4. Gắn widget vào item
        self.setItemWidget(item, lbl)

    def set_dark_mode(self, is_dark: bool) -> None:
        """Cập nhật giao diện theme tối/sáng cho list kết quả.

        Args:
            is_dark: Cờ sử dụng theme tối.
        """
        self.is_dark = is_dark
        if is_dark:
            self.setStyleSheet("""
                QListWidget { background: #0d1117; color: #c9d1d9; border: none; }
                QListWidget::item:selected { background: #1f3a5f; color: #58a6ff; }
                QListWidget::item:hover { background: #161b22; }
            """)
        else:
            self.setStyleSheet("""
                QListWidget { background: #ffffff; color: #2c3e50; border: none; }
                QListWidget::item:selected { background: #e8f0fe; color: #1a73e8; }
                QListWidget::item:hover { background: #f8f9fa; }
            """)

    def on_item_clicked(self, item: QListWidgetItem) -> None:
        """Xử lý sự kiện click chuột vào một dòng kết quả tìm kiếm.

        Args:
            item: Item kết quả tìm kiếm QListWidgetItem được click.
        """
        res = item.data(Qt.ItemDataRole.UserRole)
        if res:
            self.item_selected.emit(res[0], res[1])
