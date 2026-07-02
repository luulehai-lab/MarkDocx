# Tên file: frontend/components/editor.py
# CHỨC NĂNG: Thành phần trình soạn thảo CodeEditor với cột số dòng LineNumberArea.
# CHANGELOG:
# - 15:21:00 02/07/2026: [DOCS] Phủ Type Hints và hoàn thiện Google-style Docstrings cho toàn bộ các hàm vẽ/sự kiện (Antigravity)
# - 15:12:00 02/07/2026: [NEW] Khởi tạo editor component tách từ main_window.py (Lê Thanh Vân/Antigravity)

from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QFont, QPainter, QColor, QTextFormat, QPaintEvent, QResizeEvent

class LineNumberArea(QWidget):
    """Widget vẽ khu vực số dòng bên cạnh trình soạn thảo."""

    def __init__(self, editor: QPlainTextEdit) -> None:
        """Khởi tạo vùng hiển thị số dòng.

        Args:
            editor: Trình soạn thảo CodeEditor sở hữu.
        """
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self) -> QSize:
        """Trả về kích thước gợi ý.

        Returns:
            QSize: Kích thước gợi ý của khu vực số dòng.
        """
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event: QPaintEvent) -> None:
        """Xử lý sự kiện vẽ widget.

        Args:
            event: Đối tượng sự kiện vẽ QPaintEvent chứa vùng cần vẽ lại.
        """
        self.codeEditor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    """Trình soạn thảo văn bản với số dòng và chức năng highlight từ khóa tìm kiếm."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Khởi tạo trình soạn thảo.

        Args:
            parent: Widget cha.
        """
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.search_term = ""
        self.is_dark = False
        
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()
        
        # Thiết lập font và thanh trượt
        self.setFont(QFont("Consolas", 11))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setStyleSheet("""
            QPlainTextEdit { border: none; background-color: #ffffff; color: #2c3e50; }
        """)
        self.verticalScrollBar().setStyleSheet("width: 10px; background: #f0f0f0; border-radius: 5px;")

    def set_dark_mode(self, is_dark: bool) -> None:
        """Cập nhật theme sáng/tối cho trình soạn thảo.

        Args:
            is_dark: Cờ sử dụng theme tối.
        """
        self.is_dark = is_dark
        if is_dark:
            self.setStyleSheet("QPlainTextEdit { border: none; background-color: #161b22; color: #c9d1d9; }")
        else:
            self.setStyleSheet("QPlainTextEdit { border: none; background-color: #ffffff; color: #2c3e50; }")
        self.highlightCurrentLine()

    def set_search_term(self, term: str) -> None:
        """Đặt từ khóa tìm kiếm hiện tại để thực hiện highlight.

        Args:
            term: Từ khóa tìm kiếm.
        """
        self.search_term = term
        self.highlightCurrentLine()

    def lineNumberAreaWidth(self) -> int:
        """Tính toán chiều rộng cần thiết để hiển thị số dòng.

        Returns:
            int: Chiều rộng khu vực số dòng tính theo pixel.
        """
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 15 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _: int) -> None:
        """Cập nhật lề cho khu vực hiển thị số dòng.

        Args:
            _: Biến giữ chỗ nhận block count thay đổi (không dùng trực tiếp).
        """
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect: QRect, dy: int) -> None:
        """Cập nhật vùng hiển thị số dòng khi văn bản cuộn hoặc thay đổi.

        Args:
            rect: Vùng cập nhật hình chữ nhật.
            dy: Khoảng cách dịch chuyển.
        """
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Xử lý sự kiện co giãn trình soạn thảo.

        Args:
            event: Đối tượng sự kiện co giãn QResizeEvent.
        """
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event: QPaintEvent) -> None:
        """Vẽ số dòng tương ứng với các block hiển thị thực tế.

        Args:
            event: Đối tượng sự kiện vẽ QPaintEvent chứa vùng cần vẽ số dòng.
        """
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#f6f8fa"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(QColor("#999"))
                painter.drawText(0, top, self.lineNumberArea.width() - 10, self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            blockNumber += 1

    def highlightCurrentLine(self) -> None:
        """Thực hiện vẽ highlight cho dòng hiện tại và các kết quả tìm kiếm trùng khớp."""
        extraSelections = []
        
        # 1. Highlight dòng hiện tại
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor("#2d333b") if self.is_dark else QColor("#f1f3f4")
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        # 2. Highlight tất cả các từ tìm kiếm (Multi-highlight)
        if self.search_term:
            cursor = self.document().find(self.search_term)
            while not cursor.isNull():
                selection = QTextEdit.ExtraSelection()
                # Màu vàng cho light, cam/xanh cho dark
                highlight_color = QColor("#ffd33d") if self.is_dark else QColor("#fff200")
                selection.format.setBackground(highlight_color)
                if self.is_dark: 
                    selection.format.setForeground(QColor("#000000"))
                selection.cursor = cursor
                extraSelections.append(selection)
                cursor = self.document().find(self.search_term, cursor)
        
        self.setExtraSelections(extraSelections)
