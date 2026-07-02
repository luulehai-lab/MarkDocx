# Tên file: config.py
# CHANGELOG:
# - 2026-05-30: [UPDATE] Tích hợp cấu hình MathJax offline. (Antigravity)
# - 2026-04-02: [KHỞI TẠO] Thiết lập cấu hình cơ bản cho ứng dụng. (Lê Hải Lưu)

import os

APP_NAME = "Vibe Markdown Reader"
VERSION = "1.1.0"
DEFAULT_WINDOW_SIZE = (1200, 800)

# Xác định đường dẫn gốc của project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cấu hình Markdown
ALLOWED_EXTENSIONS = [".md", ".markdown", ".txt"]
MATHJAX_JS_PATH = os.path.join(BASE_DIR, "frontend", "static", "mathjax.js")
MERMAID_JS_PATH = os.path.join(BASE_DIR, "frontend", "static", "mermaid.min.js")