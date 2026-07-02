# Tên file: main.py
# CHANGELOG:
# - 2026-04-02: [KHỞI TẠO] Tạo entry point khởi chạy ứng dụng. (Lê Hải Lưu)

import sys
from PyQt6.QtWidgets import QApplication
from frontend.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()