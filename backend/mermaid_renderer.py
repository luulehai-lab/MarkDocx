# Tên file: backend/mermaid_renderer.py
# CHỨC NĂNG: Cung cấp bộ renderer thầm lặng (headless) để chuyển đổi mã Mermaid sang ảnh PNG.
# CHANGELOG:
# - 15:05:00 02/07/2026: [REFACTOR] Rút ngắn render_to_image bằng cách tách template HTML, sửa lỗi Silent Exception trong cleanup và thay print bằng logging (Lê Thanh Vân/Antigravity)
# - 17:18:00 28/05/2026: [UPDATE] Cập nhật cấu hình maxTextSize: 10000000 cho Mermaid renderer thầm lặng và thêm Google Docstring. (Antigravity)
# - 16:08:00 18/04/2026: [UPDATE] Sửa Base URL để nạp JS thành công và render biểu đồ thật. (Antigravity)

import os
import uuid
import logging
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl, QEventLoop, QTimer
from config import MERMAID_JS_PATH, BASE_DIR

logger = logging.getLogger(__name__)

def _get_mermaid_html_template(rel_js_path: str, mermaid_code: str) -> str:
    """Trả về HTML template để render sơ đồ Mermaid thầm lặng."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="{rel_js_path}"></script>
        <style>
            html, body {{ 
                margin: 0; padding: 0; 
                background-color: white !important; 
                overflow: hidden !important; /* Xóa thanh cuộn */
            }}
            body {{ 
                padding: 20px; 
                display: inline-block;
            }}
            .mermaid {{ background-color: white !important; }}
        </style>
    </head>
    <body>
        <div id="container" class="mermaid">{mermaid_code}</div>
        <script>
            window.mermaid_done = false;
            window.onload = function() {{
                if (typeof mermaid !== 'undefined') {{
                    mermaid.initialize({{ 
                        startOnLoad: false, 
                        theme: 'default',
                        securityLevel: 'loose',
                        useMaxWidth: false, // Rất quan trọng: cho phép render kích thước thật
                        maxTextSize: 10000000
                    }});
                    const container = document.getElementById('container');
                    mermaid.init(undefined, container).then(function() {{
                        window.mermaid_done = true;
                    }}).catch(function(err) {{
                        window.mermaid_done = true;
                    }});
                }} else {{
                    window.mermaid_done = true;
                }}
            }};
        </script>
    </body>
    </html>
    """

class MermaidRenderer:
    def __init__(self):
        self.view = QWebEngineView()
        self.view.setWindowFlags(self.view.windowFlags() | (1 << 11)) 
        
        settings = self.view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        
        # Đặt kích thước mặc định và Zoom cao để ảnh siêu nét
        self.view.resize(1200, 1200)
        self.view.setZoomFactor(3.0) # Ultra HD Zoom
        self.temp_dir = os.path.join(BASE_DIR, "temp_render")
        os.makedirs(self.temp_dir, exist_ok=True)

    def render_to_image(self, mermaid_code: str, is_dark: bool = False) -> str:
        """Chuyển đổi mã Mermaid sang ảnh PNG thầm lặng (headless).

        Args:
            mermaid_code: Chuỗi chứa mã nguồn Mermaid.
            is_dark: Cờ sử dụng giao diện tối.

        Returns:
            str: Đường dẫn tuyệt đối đến file ảnh PNG tạm đã render.
        """
        rel_js_path = os.path.relpath(MERMAID_JS_PATH, BASE_DIR).replace('\\', '/')
        html = _get_mermaid_html_template(rel_js_path, mermaid_code)
        
        self.view.show()
        self.view.move(-5000, -5000)
        
        loop = QEventLoop()
        self.view.loadFinished.connect(loop.quit)
        # QUAN TRỌNG: Phải có Base URL thì trình duyệt ảo mới được phép nạp JS từ file local
        self.view.setHtml(html, QUrl.fromLocalFile(BASE_DIR + os.sep))
        loop.exec()

        # Đợi render thực sự
        rendered_loop = QEventLoop()
        is_success = False
        def check_status(result):
            nonlocal is_success
            if result:
                is_success = True
                rendered_loop.quit()

        timer = QTimer()
        timer.timeout.connect(lambda: self.view.page().runJavaScript("window.mermaid_done", check_status))
        timer.start(200) 
        QTimer.singleShot(8000, rendered_loop.quit)
        rendered_loop.exec()
        timer.stop()

        # Lấy kích thước thực tế sau khi đã render và zoom
        size_loop = QEventLoop()
        rect = {'width': 800, 'height': 600}
        def get_size(result):
            nonlocal rect
            if result: rect = result
            size_loop.quit()

        # Dùng getBBox() trên SVG để lấy kích thước thật của nội dung (giúp ảnh to và nét)
        size_js = """
            var el = document.querySelector('.mermaid svg'); 
            if(el) { 
                var b = el.getBBox(); 
                ({width: b.width + 50, height: b.height + 80}); 
            } else { 
                null; 
            }
        """
        self.view.page().runJavaScript(size_js, get_size)
        size_loop.exec()

        # Resize view sát với kích thước nội dung (WebEngine tự tính toán theo Zoom)
        self.view.resize(int(rect['width']), int(rect['height']))
        
        final_loop = QEventLoop()
        QTimer.singleShot(1000, final_loop.quit)
        final_loop.exec()
        
        # Lưu ảnh
        image_path = os.path.join(self.temp_dir, f"mermaid_{uuid.uuid4().hex}.png")
        pixmap = self.view.grab()
        if not pixmap.isNull():
            pixmap.save(image_path, "PNG")
            size = os.path.getsize(image_path)
            logger.info(f"Đã render và lưu ảnh Mermaid: {size} bytes")
        
        self.view.hide()
        return image_path

    def cleanup(self):
        """Xóa các file tạm."""
        if os.path.exists(self.temp_dir):
            for f in os.listdir(self.temp_dir):
                try:
                    os.remove(os.path.join(self.temp_dir, f))
                except OSError as e:
                    logger.debug(f"Không thể xóa file tạm {f}: {e}")
