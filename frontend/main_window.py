# Tên file: frontend/main_window.py
# CHANGELOG:
# - 15:18:00 02/07/2026: [REFACTOR] Tách các class phụ trợ sang frontend/components/ để giảm khớp nối (Modularity First) (Lê Thanh Vân/Antigravity)
# - 15:08:00 02/07/2026: [REFACTOR] Phân rã _init_ui thành các helpers nhỏ, sửa triệt để 5 lỗi Silent Exceptions và tích hợp logging (Lê Thanh Vân/Antigravity)
# - 2026-05-30: [UPDATE] Tích hợp xuất PDF bất đồng bộ với dialog Premium và xuất DOCX xử lý LaTeX. (Antigravity)
# - 2026-04-03: [NÂNG CẤP] Cập nhật giao diện Splitter: Left Panel (File list) và Right Panel (Tabs: Editor & Viewer). (Lê Hải Lưu)

import os
import json
import logging
from PyQt6.QtWidgets import (
    QMainWindow, QFileDialog, QMessageBox, QToolBar, 
    QStatusBar, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QTabWidget, QSplitter, QMenu, QLineEdit, 
    QPushButton, QLabel, QDockWidget, QListWidgetItem
)
from PyQt6.QtGui import QAction, QShortcut, QKeySequence, QTextDocument
from PyQt6.QtCore import QFileSystemWatcher, QUrl, Qt, QByteArray
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings

from config import APP_NAME, DEFAULT_WINDOW_SIZE, BASE_DIR
from backend.md_parser import (
    open_file_with_default_app, 
    open_folder_and_select_file
)
from backend.exporters import export_to_docx
from frontend.styles import get_full_css
from frontend.components.parser_thread import MarkdownParserThread
from frontend.components.editor import CodeEditor
from frontend.components.search_panel import SearchResultPanel

logger = logging.getLogger(__name__)

SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(*DEFAULT_WINDOW_SIZE)
        
        self.current_file = None
        self.history_files = []
        self.parser_thread = None
        self.is_dark = False
        self.landscape_mode = False 
        
        self.watcher = QFileSystemWatcher()
        self.watcher.fileChanged.connect(self.on_file_changed_externally)

        self._init_ui()
        self.load_settings()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Splitter chính cho cả 3 vùng
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setHandleWidth(2)
        main_layout.addWidget(self.main_splitter)

        self._init_ui_splitters()
        self._init_toolbar()
        self._init_search_panel(main_layout)
        self._init_shortcuts_and_status()

    def _init_ui_splitters(self):
        # 1. Left Sidebar: Lịch sử file
        self.sidebar = QListWidget()
        self.sidebar.itemClicked.connect(self.on_file_item_clicked)
        self.sidebar.setMinimumWidth(100)
        self.sidebar.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.sidebar.customContextMenuRequested.connect(self.show_sidebar_context_menu)
        self.main_splitter.addWidget(self.sidebar)

        # 2. Middle Sidebar: Mục lục (TOC)
        self.toc_view = QWebEngineView()
        self.toc_view.setMinimumWidth(150)
        self.toc_view.page().urlChanged.connect(self.on_toc_navigation)
        self.main_splitter.addWidget(self.toc_view)

        # 3. Content: Tabs
        self.tabs = QTabWidget()
        
        self.editor = CodeEditor()
        self.tabs.addTab(self.editor, "📝 Soạn thảo")
        
        self.web_view = QWebEngineView()
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
        self.tabs.addTab(self.web_view, "👁️ Xem thử")
        
        self.main_splitter.addWidget(self.tabs)
        
        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 2)
        self.main_splitter.setStretchFactor(2, 6)

    def _init_search_panel(self, main_layout):
        self.search_panel = QWidget()
        self.search_panel.setObjectName("searchPanel")
        search_layout = QHBoxLayout(self.search_panel)
        search_layout.setContentsMargins(10, 5, 10, 5)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm nội dung...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        self.search_input.returnPressed.connect(lambda: self.do_search(False))
        search_layout.addWidget(self.search_input)
        
        self.search_count_label = QLabel("0 kết quả")
        self.search_count_label.setStyleSheet("color: gray; margin: 0 10px;")
        search_layout.addWidget(self.search_count_label)
        
        self.btn_prev = QPushButton("◀")
        self.btn_prev.setFixedWidth(40)
        self.btn_prev.clicked.connect(lambda: self.do_search(True))
        search_layout.addWidget(self.btn_prev)
        
        self.btn_next = QPushButton("▶")
        self.btn_next.setFixedWidth(40)
        self.btn_next.clicked.connect(lambda: self.do_search(False))
        search_layout.addWidget(self.btn_next)
        
        self.btn_all = QPushButton("📋 Tìm tất cả")
        self.btn_all.clicked.connect(self.find_all_and_show)
        search_layout.addWidget(self.btn_all)
        
        btn_close = QPushButton("✕")
        btn_close.setFixedWidth(30)
        btn_close.clicked.connect(self.hide_search_panel)
        search_layout.addWidget(btn_close)
        
        self.search_panel.hide()
        main_layout.addWidget(self.search_panel)

        self.results_panel = SearchResultPanel()
        self.results_panel.item_selected.connect(self.on_search_result_clicked)
        
        self.results_dock = QDockWidget("Kết quả tìm kiếm", self)
        self.results_dock.setWidget(self.results_panel)
        self.results_dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea | Qt.DockWidgetArea.TopDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.results_dock)
        self.results_dock.hide()

    def _init_shortcuts_and_status(self):
        self.tabs.currentChanged.connect(self.on_tab_changed)

        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.show_search_panel)
        QShortcut(QKeySequence("Esc"), self).activated.connect(self.hide_search_panel)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Sẵn sàng.")

    def on_toc_navigation(self, url):
        """Xử lý điều hướng khi click mục lục."""
        anchor = url.fragment()
        if anchor:
            js = f"document.getElementById('{anchor}').scrollIntoView({{behavior: 'smooth'}});"
            self.web_view.page().runJavaScript(js)
            self.tabs.setCurrentIndex(1) # Tự động chuyển qua tab Viewer

    def _init_toolbar(self):
        toolbar = QToolBar("Tools")
        toolbar.setIconSize(toolbar.iconSize() * 1.3)
        self.addToolBar(toolbar)

        open_act = QAction("📂 Mở", self)
        open_act.triggered.connect(self.open_file_dialog)
        toolbar.addAction(open_act)

        save_act = QAction("💾 Lưu", self)
        save_act.setShortcut(QKeySequence("Ctrl+S"))
        save_act.triggered.connect(self.save_current_file)
        toolbar.addAction(save_act)
        
        toolbar.addSeparator()
        self.theme_btn = QAction("🌙 Tối", self)
        self.theme_btn.triggered.connect(self.toggle_theme)
        toolbar.addAction(self.theme_btn)
        
        self.orient_btn = QAction("↔ Ngang", self)
        self.orient_btn.setCheckable(True)
        self.orient_btn.triggered.connect(self.toggle_orientation)
        toolbar.addAction(self.orient_btn)

        toolbar.addSeparator()
        
        pdf_act = QAction("📄 PDF", self)
        pdf_act.triggered.connect(self.export_pdf)
        toolbar.addAction(pdf_act)
        
        docx_act = QAction("📝 DOCX", self)
        docx_act.triggered.connect(self.export_docx)
        toolbar.addAction(docx_act)

    def apply_theme(self, is_dark: bool):
        """Áp dụng theme sáng/tối một cách chính xác."""
        self.is_dark = is_dark
        self.theme_btn.setText("☀️ Sáng" if is_dark else "🌙 Tối")
        self.editor.set_dark_mode(is_dark)
        self.results_panel.set_dark_mode(is_dark)
        
        # Style cho search panel
        bg = "#161b22" if is_dark else "#f1f3f4"
        fg = "#c9d1d9" if is_dark else "#000000"
        self.search_panel.setStyleSheet(f"QWidget#searchPanel {{ background: {bg}; border-top: 1px solid #30363d; }} QLineEdit {{ background: {'#0d1117' if is_dark else '#fff'}; color: {fg}; border: 1px solid #30363d; padding: 4px; }}")
        
        self.render_viewer()

    def toggle_theme(self):
        """Hàm trigger từ nút bấm."""
        self.apply_theme(not self.is_dark)

    def toggle_orientation(self, checked):
        self.landscape_mode = checked
        self.status_bar.showMessage(f"Khổ giấy: {'Ngang' if checked else 'Dọc'}", 2000)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.history_files = settings.get("history_files", [])
                    
                    # Áp dụng theme (không dùng toggle để tránh bị ngược)
                    is_dark = settings.get("is_dark", False)
                    self.apply_theme(is_dark)
                    
                    self.refresh_file_list_ui()
                    
                    # Khôi phục trạng thái thanh kéo (chỉ làm khi có đủ 3 vùng)
                    state = settings.get("splitter_state")
                    if state:
                        self.main_splitter.restoreState(QByteArray.fromHex(state.encode()))
                        
                        # Đảm bảo phần nội dung có độ rộng tối thiểu (Kiểm tra an toàn)
                        sizes = self.main_splitter.sizes()
                        if len(sizes) >= 3 and sizes[2] < 50:
                            self.main_splitter.setSizes([180, 200, 600])
                            
                    last = settings.get("last_file")
                    if last and os.path.exists(last): self.load_markdown(last)
            except Exception as e:
                logger.error(f"Lỗi load settings: {e}", exc_info=True)

    def save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    "last_file": self.current_file,
                    "history_files": self.history_files,
                    "is_dark": self.is_dark,
                    "splitter_state": self.main_splitter.saveState().toHex().data().decode()
                }, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Lỗi lưu settings: {e}", exc_info=True)

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Mở file", "", "Markdown (*.md)")
        if path: self.load_markdown(path)

    def load_markdown(self, path):
        if not path or not os.path.exists(path): return
        if self.current_file: self.watcher.removePath(self.current_file)
        self.current_file = path
        self.watcher.addPath(path)
        
        if path in self.history_files: self.history_files.remove(path)
        self.history_files.insert(0, path)
        self.history_files = self.history_files[:20]
        
        self.refresh_file_list_ui()
        self.save_settings()

        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.editor.setPlainText(f.read())
        except Exception as e:
            QMessageBox.critical(self, "Lỗi đọc file", f"Không thể mở file:\n{e}")
        self.render_viewer()

    def refresh_file_list_ui(self):
        self.sidebar.clear()
        for f in self.history_files: self.sidebar.addItem(os.path.basename(f))
        if self.current_file in self.history_files:
            self.sidebar.setCurrentRow(self.history_files.index(self.current_file))

    def show_sidebar_context_menu(self, pos):
        item = self.sidebar.itemAt(pos)
        if not item: return
        
        row = self.sidebar.row(item)
        menu = QMenu()
        remove_action = QAction("❌ Xóa khỏi lịch sử", self)
        remove_action.triggered.connect(lambda: self.remove_selected_from_history(row))
        menu.addAction(remove_action)
        menu.exec(self.sidebar.mapToGlobal(pos))

    def remove_selected_from_history(self, row: int) -> None:
        """Xóa tệp tin đã chọn ra khỏi danh sách lịch sử mở file.

        Args:
            row: Chỉ số hàng của item được chọn trong list widget.
        """
        if 0 <= row < len(self.history_files):
            self.history_files.pop(row)
            self.refresh_file_list_ui()
            self.save_settings()
            self.status_bar.showMessage("Đã gỡ khỏi lịch sử.", 2000)

    def on_file_item_clicked(self, item: QListWidgetItem) -> None:
        """Xử lý sự kiện click vào item file trong sidebar lịch sử.

        Args:
            item: Đối tượng QListWidgetItem đại diện cho file được click.
        """
        idx = self.sidebar.row(item)
        if 0 <= idx < len(self.history_files):
            self.load_markdown(self.history_files[idx])

    def render_viewer(self) -> None:
        """Khởi động luồng biên dịch Markdown và render kết quả hiển thị."""
        if not self.current_file: return
        self.parser_thread = MarkdownParserThread(self.current_file, self.is_dark)
        self.parser_thread.parse_done.connect(self.on_parse_done)
        self.parser_thread.error_occurred.connect(self.on_error)
        self.parser_thread.start()

    def show_search_panel(self) -> None:
        """Hiển thị bảng tìm kiếm phía dưới và lấy focus cho ô nhập liệu."""
        self.search_panel.show()
        self.search_input.setFocus()
        self.search_input.selectAll()

    def hide_search_panel(self) -> None:
        """Ẩn bảng tìm kiếm và làm sạch highlight các kết quả tìm kiếm cũ."""
        self.search_panel.hide()
        self.editor.set_search_term("") # Xóa highlight khi đóng
        self.web_view.findText("") 

    def on_search_text_changed(self, text: str) -> None:
        """Cập nhật highlight và đếm số lượng kết quả khi văn bản tìm kiếm thay đổi.

        Args:
            text: Chuỗi từ khóa cần tìm kiếm.
        """
        # Theo yêu cầu: Chỉ bôi vàng ở Tab đang đứng
        if self.tabs.currentIndex() == 0:
            self.editor.set_search_term(text)
            self.web_view.findText("") # Làm sạch tab kia
        else:
            self.editor.set_search_term("") # Làm sạch tab kia
            self.web_view.findText(text)

        if text:
            # Tự động cập nhật số lượng khi gõ (luôn đếm từ code cho chính xác)
            count = 0
            doc = self.editor.document()
            cursor = doc.find(text)
            while not cursor.isNull():
                count += 1
                cursor = doc.find(text, cursor)
            self.search_count_label.setText(f"{count} kết quả")
        else:
            self.search_count_label.setText("0 kết quả")

    def find_all_and_show(self):
        """Quét toàn bộ và hiện bảng kết quả giống Notepad++."""
        text = self.search_input.text()
        if not text: return
        
        self.results_panel.clear()
        doc = self.editor.document()
        count = 0
        
        cursor = doc.find(text)
        while not cursor.isNull():
            count += 1
            line_num = cursor.blockNumber() + 1
            full_line_text = cursor.block().text()
            # Thêm vào panel
            self.results_panel.add_result(line_num, full_line_text, cursor.position(), text)
            cursor = doc.find(text, cursor)
            
        if count > 0:
            self.results_dock.show()
            self.results_dock.setWindowTitle(f"Kết quả tìm kiếm cho '{text}' - ({count} hits)")
            self.status_bar.showMessage(f"Đã tìm thấy {count} kết quả.", 3000)
        else:
            self.results_dock.hide()
            QMessageBox.information(self, "Thông báo", f"Không tìm thấy '{text}'")

    def on_search_result_clicked(self, line_num: int, pos: int) -> None:
        """Khi click vào một dòng trong bảng kết quả, định vị con trỏ tại đó.

        Args:
            line_num: Số thứ tự dòng trong văn bản.
            pos: Vị trí con trỏ ký tự tuyệt đối trong văn bản.
        """
        # 1. Luôn cập nhật vị trí trong Editor (vì nó là nguồn dữ liệu chuẩn)
        cursor = self.editor.textCursor()
        cursor.setPosition(pos)
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()
        
        # 2. Đồng bộ highlight sang Viewer
        text = self.search_input.text()
        if text:
            self.web_view.findText(text)

    def do_search(self, backward: bool = False) -> None:
        """Thực hiện hành động tìm kiếm từ tiếp theo trong tài liệu.

        Args:
            backward: Cờ tìm kiếm ngược về phía trước.
        """
        text = self.search_input.text()
        if not text:
            self.search_count_label.setText("0 kết quả")
            return

        if self.tabs.currentIndex() == 0: # Tìm trong Editor
            options = QTextDocument.FindFlag.FindBackward if backward else QTextDocument.FindFlag(0)
            self.editor.find(text, options)
            # Đếm số lượng kết quả (báo cáo)
            count = 0
            doc = self.editor.document()
            cursor = doc.find(text)
            while not cursor.isNull():
                count += 1
                cursor = doc.find(text, cursor)
            self.search_count_label.setText(f"{count} kết quả")
            
        else: # Tìm trong Viewer
            # Note: QWebEngineView.findText không trả về số lượng trực tiếp dễ dàng
            options = QWebEnginePage.FindFlag.FindBackward if backward else QWebEnginePage.FindFlag(0)
            self.web_view.findText(text, options)
            self.search_count_label.setText("Đang tìm...")

    def on_parse_done(self, data):
        self.web_view.setHtml(data["html"], QUrl.fromLocalFile(os.path.abspath(self.current_file)))
        
        toc_css = f"<style>{get_full_css(self.is_dark)} .markdown-body {{ padding: 15px; border: none; box-shadow: none; font-size: 0.85em; background: transparent; }}</style>"
        self.toc_view.setHtml(toc_css + f"<div class='markdown-body'>{data['toc']}</div>")
        self.status_bar.showMessage("Đã cập nhật.", 2000)

    def on_file_changed_externally(self, path):
        if path == self.current_file: self.load_markdown(path)

    def save_current_file(self):
        if not self.current_file: return
        try:
            self.watcher.removePath(self.current_file)
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            self.watcher.addPath(self.current_file)
            self.render_viewer()
        except Exception as e:
            logger.error(f"Lỗi lưu file hiện tại: {e}", exc_info=True)

    def on_tab_changed(self, i):
        if i == 1: self.render_viewer()
        
        # Đồng bộ tìm kiếm khi chuyển tab
        if not self.search_panel.isHidden():
            text = self.search_input.text()
            self.on_search_text_changed(text)

    def export_pdf(self):
        if not self.current_file: return
        path, _ = QFileDialog.getSaveFileName(self, "Lưu PDF", "", "PDF (*.pdf)")
        if path:
            page = self.web_view.page()
            
            def on_pdf_finished(file_path: str, success: bool) -> None:
                try:
                    page.pdfPrintingFinished.disconnect(on_pdf_finished)
                except Exception as e:
                    logger.debug(f"Không thể ngắt kết nối tín hiệu in PDF: {e}")
                if success:
                    self._show_export_success_dialog(file_path, "PDF")
                else:
                    QMessageBox.critical(self, "Lỗi", "Không thể xuất file PDF thành công ạ.")

            page.pdfPrintingFinished.connect(on_pdf_finished)
            page.printToPdf(path)
            self.status_bar.showMessage("Đang xuất PDF...", 3000)

    def export_docx(self):
        if not self.current_file: return
        path, _ = QFileDialog.getSaveFileName(self, "Lưu DOCX", "", "Word (*.docx)")
        if path:
            if export_to_docx(self.current_file, path, self.landscape_mode, self.is_dark):
                self._show_export_success_dialog(path, "Word")

    def _show_export_success_dialog(self, file_path: str, file_type: str):
        """Hiện dialog thành công với các nút Xem file và Vào thư mục."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Xuất file thành công')
        msg_box.setText(f'Đã xuất file {file_type} tại:\n{file_path}')
        msg_box.setIcon(QMessageBox.Icon.Information)
        
        view_btn = msg_box.addButton('📄 Xem file', QMessageBox.ButtonRole.AcceptRole)
        folder_btn = msg_box.addButton('📁 Vào thư mục', QMessageBox.ButtonRole.ActionRole)
        msg_box.addButton('Đóng', QMessageBox.ButtonRole.RejectRole)
        
        msg_box.exec()
        
        clicked = msg_box.clickedButton()
        if clicked == view_btn:
            open_file_with_default_app(file_path)
        elif clicked == folder_btn:
            open_folder_and_select_file(file_path)

    def on_error(self, e): QMessageBox.critical(self, "Lỗi", e)
