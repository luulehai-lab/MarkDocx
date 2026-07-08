# Tên file: frontend/components/editor.py
# CHỨC NĂNG: Thành phần trình soạn thảo CodeEditor với cột số dòng LineNumberArea.
# CHANGELOG:
# - 09:53:00 08/07/2026: [FIX] Sửa lỗi click lệch dòng trên LineNumberArea bằng phương pháp tìm block theo tọa độ y vẽ (Antigravity)
# - 09:50:00 08/07/2026: [NEW] Thêm tính năng click/drag chọn dòng và Ctrl+Click chọn nhiều dòng cách quãng kèm copy (Antigravity)
# - 15:21:00 02/07/2026: [DOCS] Phủ Type Hints và hoàn thiện Google-style Docstrings cho toàn bộ các hàm vẽ/sự kiện (Antigravity)
# - 15:12:00 02/07/2026: [NEW] Khởi tạo editor component tách từ main_window.py (Lê Thanh Vân/Antigravity)

from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QApplication
from PyQt6.QtCore import Qt, QSize, QRect, QPoint
from PyQt6.QtGui import (
    QFont,
    QPainter,
    QColor,
    QTextFormat,
    QPaintEvent,
    QResizeEvent,
    QMouseEvent,
    QTextCursor,
    QKeyEvent,
    QTextBlock,
)


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

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Xử lý sự kiện nhấn chuột trái để bắt đầu chọn dòng hoặc chọn cách quãng.

        Args:
            event: Đối tượng sự kiện chuột QMouseEvent.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            ctrl_pressed = bool(event.modifiers() & Qt.KeyboardModifier.ControlModifier)
            self.codeEditor.selectLineAtPos(event.pos(), ctrl_pressed)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Xử lý sự kiện di chuyển chuột khi đang kéo để chọn dải dòng.

        Args:
            event: Đối tượng sự kiện chuột QMouseEvent.
        """
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.codeEditor.selectLinesBetween(event.pos())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Xử lý sự kiện thả chuột để kết thúc thao tác chọn dòng.

        Args:
            event: Đối tượng sự kiện chuột QMouseEvent.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.codeEditor.endLineSelection()
        else:
            super().mouseReleaseEvent(event)


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

        # Trạng thái phục vụ chọn dòng kiểu VS Code
        self.selected_block_numbers: set[int] = set()
        self._drag_start_block_num: int | None = None

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

        # Thiết lập font và thanh trượt
        self.setFont(QFont("Consolas", 11))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setStyleSheet("""
            QPlainTextEdit { border: none; background-color: #ffffff; color: #2c3e50; }
        """)
        self.verticalScrollBar().setStyleSheet(
            "width: 10px; background: #f0f0f0; border-radius: 5px;"
        )

    def set_dark_mode(self, is_dark: bool) -> None:
        """Cập nhật theme sáng/tối cho trình soạn thảo.

        Args:
            is_dark: Cờ sử dụng theme tối.
        """
        self.is_dark = is_dark
        if is_dark:
            self.setStyleSheet(
                "QPlainTextEdit { border: none; background-color: #161b22; color: #c9d1d9; }"
            )
        else:
            self.setStyleSheet(
                "QPlainTextEdit { border: none; background-color: #ffffff; color: #2c3e50; }"
            )
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
        space = 15 + self.fontMetrics().horizontalAdvance("9") * digits
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
            self.lineNumberArea.update(
                0, rect.y(), self.lineNumberArea.width(), rect.height()
            )

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Xử lý sự kiện co giãn trình soạn thảo.

        Args:
            event: Đối tượng sự kiện co giãn QResizeEvent.
        """
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        )

    def lineNumberAreaPaintEvent(self, event: QPaintEvent) -> None:
        """Vẽ số dòng tương ứng với các block hiển thị thực tế.

        Args:
            event: Đối tượng sự kiện vẽ QPaintEvent chứa vùng cần vẽ số dòng.
        """
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#f6f8fa"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = round(
            self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        )
        bottom = top + round(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(QColor("#999"))
                painter.drawText(
                    0,
                    top,
                    self.lineNumberArea.width() - 10,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    number,
                )

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            blockNumber += 1

    def _getBlockAtY(self, y: int) -> QTextBlock:
        """Tìm block văn bản hiển thị tại tọa độ y trên cột số dòng.

        Args:
            y: Tọa độ y trên LineNumberArea.

        Returns:
            QTextBlock: Block tìm thấy hoặc QTextBlock() không hợp lệ nếu không tìm thấy.
        """
        block = self.firstVisibleBlock()
        top = round(
            self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        )
        bottom = top + round(self.blockBoundingRect(block).height())

        while block.isValid() and top <= self.lineNumberArea.rect().bottom():
            if block.isVisible() and top <= y < bottom:
                return block
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
        return block

    def selectLineAtPos(self, pos: QPoint, ctrl_pressed: bool) -> None:
        """Chọn dòng đơn hoặc toggle chọn dòng cách quãng khi click trên cột số dòng.

        Args:
            pos: Tọa độ chuột trong hệ tọa độ của LineNumberArea.
            ctrl_pressed: Cờ trạng thái phím Ctrl đang được giữ.
        """
        block = self._getBlockAtY(pos.y())

        if block.isValid():
            block_num = block.blockNumber()

            if ctrl_pressed:
                if block_num in self.selected_block_numbers:
                    self.selected_block_numbers.remove(block_num)
                else:
                    self.selected_block_numbers.add(block_num)
                self._drag_start_block_num = None
                self.highlightCurrentLine()
            else:
                self.selected_block_numbers.clear()
                self._drag_start_block_num = block_num

                # Bôi đen dòng hiện tại
                new_cursor = self.textCursor()
                new_cursor.setPosition(block.position())
                new_cursor.setPosition(
                    block.position() + block.length() - 1,
                    QTextCursor.MoveMode.KeepAnchor,
                )
                self.setTextCursor(new_cursor)

    def selectLinesBetween(self, current_pos: QPoint) -> None:
        """Chọn dải các dòng liên tiếp khi kéo chuột từ dòng bắt đầu.

        Args:
            current_pos: Tọa độ chuột hiện tại trên LineNumberArea.
        """
        if self._drag_start_block_num is None:
            return

        block = self._getBlockAtY(current_pos.y())

        if block.isValid():
            current_block_num = block.blockNumber()

            start_block = self.document().findBlockByNumber(self._drag_start_block_num)
            if start_block.isValid():
                new_cursor = self.textCursor()

                if self._drag_start_block_num <= current_block_num:
                    new_cursor.setPosition(start_block.position())
                    new_cursor.setPosition(
                        block.position() + block.length() - 1,
                        QTextCursor.MoveMode.KeepAnchor,
                    )
                else:
                    new_cursor.setPosition(
                        start_block.position() + start_block.length() - 1
                    )
                    new_cursor.setPosition(
                        block.position(), QTextCursor.MoveMode.KeepAnchor
                    )

                self.setTextCursor(new_cursor)

    def endLineSelection(self) -> None:
        """Kết thúc quá trình kéo chọn dòng, đặt dòng bắt đầu về None."""
        self._drag_start_block_num = None

    def copySelectedBlocks(self) -> None:
        """Sao chép nội dung tất cả các dòng được chọn cách quãng vào clipboard."""
        if not self.selected_block_numbers:
            return

        texts = []
        for block_num in sorted(self.selected_block_numbers):
            block = self.document().findBlockByNumber(block_num)
            if block.isValid():
                texts.append(block.text())

        clipboard = QApplication.clipboard()
        if clipboard:
            clipboard.setText("\n".join(texts))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Xử lý sự kiện bàn phím, hỗ trợ copy vùng chọn cách quãng và xóa trạng thái chọn.

        Args:
            event: Đối tượng sự kiện bàn phím QKeyEvent.
        """
        # Nếu nhấn Ctrl+C khi đang chọn cách quãng
        if (
            event.key() == Qt.Key.Key_C
            and event.modifiers() == Qt.KeyboardModifier.ControlModifier
        ):
            if self.selected_block_numbers:
                self.copySelectedBlocks()
                return

        # Xóa vùng chọn cách quãng khi di chuyển con trỏ mà không giữ Ctrl/Shift
        if self.selected_block_numbers and not (
            event.modifiers()
            & (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier)
        ):
            if event.key() in (
                Qt.Key.Key_Up,
                Qt.Key.Key_Down,
                Qt.Key.Key_Left,
                Qt.Key.Key_Right,
                Qt.Key.Key_Home,
                Qt.Key.Key_End,
                Qt.Key.Key_PageUp,
                Qt.Key.Key_PageDown,
            ):
                self.selected_block_numbers.clear()
                self.highlightCurrentLine()

        super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Xử lý sự kiện click chuột trên editor để xóa highlight chọn cách quãng.

        Args:
            event: Đối tượng sự kiện chuột QMouseEvent.
        """
        if self.selected_block_numbers and not (
            event.modifiers() & Qt.KeyboardModifier.ControlModifier
        ):
            self.selected_block_numbers.clear()
            self.highlightCurrentLine()
        super().mousePressEvent(event)

    def highlightCurrentLine(self) -> None:
        """Thực hiện vẽ highlight cho dòng hiện tại, dòng được chọn cách quãng và kết quả tìm kiếm."""
        extraSelections = []

        # 1. Highlight dòng hiện tại (chỉ vẽ khi không chọn cách quãng)
        if not self.selected_block_numbers and not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor("#2d333b") if self.is_dark else QColor("#f1f3f4")
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        # 2. Highlight các dòng được chọn cách quãng bằng Ctrl
        if self.selected_block_numbers:
            for block_num in sorted(self.selected_block_numbers):
                block = self.document().findBlockByNumber(block_num)
                if block.isValid():
                    selection = QTextEdit.ExtraSelection()
                    lineColor = QColor("#21262d") if self.is_dark else QColor("#e8f0fe")
                    selection.format.setBackground(lineColor)
                    selection.format.setProperty(
                        QTextFormat.Property.FullWidthSelection, True
                    )

                    cursor = QTextCursor(block)
                    cursor.clearSelection()
                    selection.cursor = cursor
                    extraSelections.append(selection)

        # 3. Highlight tất cả các từ tìm kiếm (Multi-highlight)
        if self.search_term:
            cursor = self.document().find(self.search_term)
            while not cursor.isNull():
                selection = QTextEdit.ExtraSelection()
                highlight_color = (
                    QColor("#ffd33d") if self.is_dark else QColor("#fff200")
                )
                selection.format.setBackground(highlight_color)
                if self.is_dark:
                    selection.format.setForeground(QColor("#000000"))
                selection.cursor = cursor
                extraSelections.append(selection)
                cursor = self.document().find(self.search_term, cursor)

        self.setExtraSelections(extraSelections)
