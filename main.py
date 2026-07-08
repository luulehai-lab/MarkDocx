# Tên file: main.py
# CHỨC NĂNG: Khởi chạy ứng dụng Markdown Viewer và tích hợp hệ thống ghi log toàn cục
# CHANGELOG:
# - 15:40:00 08/07/2026: [UPDATE] Tích hợp cấu hình setup_logging từ backend.logger (Antigravity)
# - 2026-04-02: [KHỞI TẠO] Tạo entry point khởi chạy ứng dụng. (Lê Hải Lưu)

import sys
from PyQt6.QtWidgets import QApplication
from backend.logger import setup_logging
from config import BASE_DIR
from frontend.main_window import MainWindow


def main() -> None:
    """Khởi chạy ứng dụng và cấu hình ghi log toàn cục trước khi hiển thị giao diện."""
    # Khởi tạo logging trước khi load các thành phần UI
    setup_logging(BASE_DIR)

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
