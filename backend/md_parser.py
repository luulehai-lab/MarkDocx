# Tên file: backend/md_parser.py
# CHỨC NĂNG: Logic xử lý Markdown và xuất DOCX.
# CHANGELOG:
# - 15:16:00 02/07/2026: [REFACTOR] Di chuyển export_to_docx sang backend/exporters.py để giảm kích thước file và nợ kỹ thuật (Lê Thanh Vân/Antigravity)
# - 15:02:00 02/07/2026: [REFACTOR] Giải phóng render_markdown_to_html bằng cách tách các helpers render JavaScript/HTML và sửa 02 lỗi Silent Exception trong dọn dẹp DOCX (Lê Thanh Vân/Antigravity)
# - 10:33:00 06/06/2026: [UPDATE] Cập nhật cấu hình MathJax mở rộng hỗ trợ delimiters $, $$ và quét toàn bộ markdown-body. (Antigravity)
# - 10:00:00 30/05/2026: [UPDATE] Tích hợp MathJax offline (tex-svg) và bộ dịch LaTeX-to-Unicode khi xuất DOCX. (Antigravity)
# - 17:21:00 28/05/2026: [NEW] Tích hợp tính năng Click-to-Zoom / Pan cho sơ đồ Mermaid bằng chuột/cuộn chuột cực đỉnh. (Antigravity)
# - 17:17:00 28/05/2026: [UPDATE] Cập nhật maxTextSize: 10000000 cho Mermaid nhằm hỗ trợ sơ đồ lớn và chuẩn hóa Google Docstrings. (Antigravity)
# - 15:52:00 18/04/2026: [UPDATE] Cải thiện regex thay thế Mermaid để tương thích newline Windows. (Antigravity)

import markdown
import os
import re
import subprocess
import logging
import pymdownx.superfences
from frontend.styles import get_full_css
from config import MATHJAX_JS_PATH, MERMAID_JS_PATH

logger = logging.getLogger(__name__)

def find_matching_brace(s: str, start_idx: int) -> int:
    """Tìm chỉ số của dấu ngoặc nhọn đóng khớp với dấu ngoặc mở tại start_idx."""
    count = 0
    for i in range(start_idx, len(s)):
        if s[i] == '{':
            count += 1
        elif s[i] == '}':
            count -= 1
            if count == 0:
                return i
    return -1

def parse_braces_content(s: str, command: str) -> list:
    """Trích xuất chính xác các tham số ngoặc nhọn lồng nhau của một lệnh LaTeX."""
    results = []
    idx = 0
    cmd_len = len(command)
    while True:
        idx = s.find(command, idx)
        if idx == -1:
            break
            
        arg_start = idx + cmd_len
        while arg_start < len(s) and s[arg_start].isspace():
            arg_start += 1
            
        if arg_start >= len(s) or s[arg_start] != '{':
            idx += 1
            continue
            
        arg1_end = find_matching_brace(s, arg_start)
        if arg1_end == -1:
            idx += 1
            continue
            
        arg1 = s[arg_start+1:arg1_end]
        
        if command == '\\frac':
            arg2_start = arg1_end + 1
            while arg2_start < len(s) and s[arg2_start].isspace():
                arg2_start += 1
                
            if arg2_start < len(s) and s[arg2_start] == '{':
                arg2_end = find_matching_brace(s, arg2_start)
                if arg2_end != -1:
                    arg2 = s[arg2_start+1:arg2_end]
                    results.append((idx, arg2_end + 1, [arg1, arg2]))
                    idx = arg2_end
                    continue
        else:  # \\sqrt
            results.append((idx, arg1_end + 1, [arg1]))
            idx = arg1_end
            continue
            
        idx += 1
    return results

def latex_to_unicode(latex_str: str) -> str:
    """Chuyển đổi biểu thức LaTeX sang ký tự Unicode phẳng."""
    if not latex_str:
        return ""

    replacements = [
        (r'\^\{\\circ\}', '°'),
        (r'\^\\circ', '°'),
        (r'\\dots', '...'),
        (r'\\Delta', 'Δ'),
        (r'\\delta', 'δ'),
        (r'\\pi', 'π'),
        (r'\\pm', '±'),
        (r'\\ge', '≥'),
        (r'\\le', '≤'),
        (r'\\cdot', '·'),
        (r'\\infty', '∞'),
        (r'\\approx', '≈'),
        (r'\\ne', '≠'),
        (r'\\alpha', 'α'),
        (r'\\beta', 'β'),
        (r'\\gamma', 'γ'),
        (r'\\theta', 'θ'),
        (r'\\circ', '°'),
        (r'\\mu', 'μ'),
        (r'\\sigma', 'σ'),
        (r'\\phi', 'φ'),
        (r'\\rho', 'ρ'),
        (r'\\eta', 'η'),
        (r'\\tau', 'τ'),
        (r'\\lambda', 'λ'),
        (r'\\omega', 'ω'),
        (r'\\times', 'x'),
        (r'\\div', '/'),
        (r'\\pm', '±'),
        (r'\\mp', '∓'),
        (r'\\neq', '≠'),
        (r'\\equiv', '≡'),
        (r'\\propto', '∝'),
        (r'\\sin', 'sin'),
        (r'\\cos', 'cos'),
        (r'\\tan', 'tan'),
        (r'\\cot', 'cot'),
        (r'\\sec', 'sec'),
        (r'\\csc', 'csc'),
        (r'\\ln', 'ln'),
        (r'\\log', 'log'),
        (r'\\exp', 'exp'),
        (r'\\sinh', 'sinh'),
        (r'\\cosh', 'cosh'),
        (r'\\tanh', 'tanh'),
        (r'\\coth', 'coth'),
    ]

    for lat, uni in replacements:
        latex_str = re.sub(lat, uni, latex_str)

    latex_str = re.sub(r'\^([0-9a-zA-Z])', r'^\1', latex_str)
    latex_str = re.sub(r'\^\{([^{}]+)\}', r'^\1', latex_str)
    latex_str = re.sub(r'\_([0-9a-zA-Z])', r'_\1', latex_str)
    latex_str = re.sub(r'\_\{([^{}]+)\}', r'_\1', latex_str)
    latex_str = process_recursive_commands(latex_str)

    return latex_str

def process_recursive_commands(s: str) -> str:
    """Xử lý đệ quy các cấu trúc LaTeX phức tạp như \\frac và \\sqrt từ trong ra ngoài."""
    while True:
        fracs = parse_braces_content(s, '\\frac')
        sqrts = parse_braces_content(s, '\\sqrt')
        
        candidates = fracs + sqrts
        if not candidates:
            break
            
        candidates.sort(key=lambda x: x[1] - x[0])
        start, end, args = candidates[0]
        
        is_frac = len(args) == 2
        processed_args = [process_recursive_commands(arg) for arg in args]
        
        if is_frac:
            replacement = f"({processed_args[0]})/({processed_args[1]})"
        else:
            replacement = f"√({processed_args[0]})"
            
        s = s[:start] + replacement + s[end:]
        
    return s

def replace_sub(match) -> str:
    val = match.group(1)
    subscript_map = {'0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉', 
                     'a': 'ₐ', 'e': 'ₑ', 'h': 'ₕ', 'i': 'ᵢ', 'j': 'ⱼ', 'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ', 
                     'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ', 'v': 'ᵥ', 'x': 'ₓ'}
    return "".join(subscript_map.get(c, c) for c in val)

def replace_super(match) -> str:
    val = match.group(1)
    superscript_map = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', 
                       '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾', 'n': 'ⁿ', 'i': 'ⁱ'}
    return "".join(superscript_map.get(c, c) for c in val)

def replace_block_math(match) -> str:
    latex = match.group(1)
    return f'<div class="math-block" style="text-align: center; margin: 15px 0; font-size: 1.15em;">{latex_to_unicode(latex)}</div>'

def replace_inline_math(match) -> str:
    latex = match.group(1)
    return f'<span class="math-inline" style="font-family: serif; font-style: italic;">{latex_to_unicode(latex)}</span>'

def clean_latex_in_markdown(text: str) -> str:
    """Lọc và chuyển đổi LaTeX trong markdown sang ký tự Unicode phẳng."""
    text = re.sub(r'\$\$([^\$]+)\$\$', replace_block_math, text)
    text = re.sub(r'\$([^\$]+)\$', replace_inline_math, text)
    text = re.sub(r'\_\{([a-zA-Z0-9]+)\}', replace_sub, text)
    text = re.sub(r'\^\{([a-zA-Z0-9\+\-\=\(\)]+)\}', replace_super, text)
    text = re.sub(r'\_([a-zA-Z0-9])', replace_sub, text)
    text = re.sub(r'\^([a-zA-Z0-9])', replace_super, text)
    return text

def open_file_with_default_app(filepath: str) -> None:
    """Mở file bằng ứng dụng mặc định của hệ thống."""
    try:
        if os.name == 'nt':
            os.startfile(filepath)
        else:
            subprocess.run(['xdg-open', filepath])
    except Exception as e:
        logger.error(f"Lỗi mở file: {e}", exc_info=True)

def open_folder_and_select_file(filepath: str) -> None:
    """Mở thư mục và chọn file bằng File Explorer."""
    try:
        if os.name == 'nt':
            subprocess.run(['explorer', '/select,', os.path.abspath(filepath)])
    except Exception as e:
        logger.error(f"Lỗi mở thư mục chứa file: {e}", exc_info=True)

def _get_mathjax_mermaid_header(is_dark: bool) -> str:
    """Trả về header cấu hình MathJax và Mermaid."""
    mathjax_uri = f"file:///{MATHJAX_JS_PATH.replace('\\', '/')}"
    return f"""
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true,
                processEnvironments: true
            }},
            options: {{
                ignoreHtmlClass: 'tex2jax_ignore',
                processHtmlClass: 'markdown-body'
            }}
        }};
    </script>
    <script id="MathJax-script" async src="{mathjax_uri}"></script>
    <script src="file:///{MERMAID_JS_PATH.replace('\\', '/')}"></script>
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            mermaid.initialize({{ 
                startOnLoad: true, 
                theme: "{'dark' if is_dark else 'default'}",
                maxTextSize: 10000000
            }});
        }});
    </script>
    """

def _get_mermaid_zoom_modal_html() -> str:
    """Trả về HTML layout của zoom modal cho Mermaid."""
    return """
    <!-- Mermaid Interactive Zoom Modal -->
    <div id="mermaid-zoom-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(13, 17, 23, 0.95); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); z-index: 99999; justify-content: center; align-items: center; user-select: none;">
        <!-- Glassmorphic Toolbar -->
        <div class="mermaid-zoom-toolbar" style="position: absolute; top: 20px; right: 20px; display: flex; gap: 8px; z-index: 100000; padding: 6px; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; backdrop-filter: blur(8px); box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);">
            <button onclick="zoomIn()" title="Phóng to" style="background: transparent; color: #fff; border: none; width: 36px; height: 36px; border-radius: 6px; cursor: pointer; font-size: 16px; display: flex; justify-content: center; align-items: center; transition: background 0.2s;" onmouseover="this.style.background='rgba(0,0,0,0.1)'" onmouseout="this.style.background='transparent'">➕</button>
            <button onclick="zoomOut()" title="Thu nhỏ" style="background: transparent; color: #fff; border: none; width: 36px; height: 36px; border-radius: 6px; cursor: pointer; font-size: 16px; display: flex; justify-content: center; align-items: center; transition: background 0.2s;" onmouseover="this.style.background='rgba(0,0,0,0.1)'" onmouseout="this.style.background='transparent'">➖</button>
            <button onclick="resetZoom()" title="Đặt lại" style="background: transparent; color: #fff; border: none; width: 36px; height: 36px; border-radius: 6px; cursor: pointer; font-size: 16px; display: flex; justify-content: center; align-items: center; transition: background 0.2s;" onmouseover="this.style.background='rgba(0,0,0,0.1)'" onmouseout="this.style.background='transparent'">🔄</button>
            <div class="divider" style="width: 1px; height: 24px; background: rgba(255,255,255,0.2); align-self: center; margin: 0 4px;"></div>
            <button class="close-btn" onclick="closeZoomModal()" title="Đóng (Esc)" style="background: #e81123; color: #fff; border: none; width: 36px; height: 36px; border-radius: 6px; cursor: pointer; font-size: 16px; display: flex; justify-content: center; align-items: center; transition: background 0.2s; font-weight: bold;" onmouseover="this.style.background='#ff3344'" onmouseout="this.style.background='#e81123'">✕</button>
        </div>
        
        <!-- Modal Content Container -->
        <div id="mermaid-zoom-container" style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; overflow: hidden; cursor: grab;">
            <div id="mermaid-zoom-content" style="transform-origin: 0 0; transition: transform 0.05s ease-out; display: inline-block;"></div>
        </div>
    </div>
    """

def _get_mermaid_zoom_script() -> str:
    """Trả về Javascript xử lý zoom/pan cho sơ đồ Mermaid."""
    return """
    <script>
        let zoomScale = 1;
        let isPanning = false;
        let startX = 0, startY = 0;
        let translateX = 0, translateY = 0;
        let modalContent = null;
        let modalContainer = null;

        function openZoomModal(mermaidDiv) {
            const svg = mermaidDiv.querySelector('svg');
            if (!svg) return;
            
            const modal = document.getElementById('mermaid-zoom-modal');
            modalContent = document.getElementById('mermaid-zoom-content');
            modalContainer = document.getElementById('mermaid-zoom-container');
            const toolbar = modal.querySelector('.mermaid-zoom-toolbar');
            
            // Sao chép SVG sang modal
            const clonedSvg = svg.cloneNode(true);
            
            // Lấy kích thước tự nhiên từ viewBox để tránh bị thu bé về 0
            const viewBox = svg.getAttribute('viewBox');
            let widthVal = '';
            let heightVal = '';
            if (viewBox) {
                const parts = viewBox.split(' ');
                if (parts.length === 4) {
                    widthVal = parts[2] + 'px';
                    heightVal = parts[3] + 'px';
                }
            }
            
            if (!widthVal) {
                const rect = svg.getBoundingClientRect();
                widthVal = rect.width + 'px';
                heightVal = rect.height + 'px';
            }
            
            clonedSvg.removeAttribute('style');
            clonedSvg.setAttribute('width', widthVal);
            clonedSvg.setAttribute('height', heightVal);
            clonedSvg.style.width = widthVal;
            clonedSvg.style.height = heightVal;
            clonedSvg.style.maxWidth = 'none';
            clonedSvg.style.maxHeight = 'none';
            clonedSvg.style.display = 'block';
            
            modalContent.innerHTML = '';
            modalContent.appendChild(clonedSvg);
            
            // Đồng bộ màu nền modal theo theme (Sáng/Tối) để có tương phản tốt nhất
            const isDarkMode = document.body.classList.contains('dark-mode');
            const divider = toolbar.querySelector('.divider');
            
            if (isDarkMode) {
                modal.style.background = 'rgba(13, 17, 23, 0.95)';
                toolbar.style.background = 'rgba(255, 255, 255, 0.08)';
                toolbar.style.borderColor = 'rgba(255, 255, 255, 0.15)';
                if (divider) divider.style.background = 'rgba(255, 255, 255, 0.2)';
                
                toolbar.querySelectorAll('button').forEach(btn => {
                    if (!btn.classList.contains('close-btn')) {
                        btn.style.color = '#ffffff';
                    }
                });
            } else {
                modal.style.background = 'rgba(255, 255, 255, 0.97)';
                toolbar.style.background = 'rgba(0, 0, 0, 0.05)';
                toolbar.style.borderColor = 'rgba(0, 0, 0, 0.1)';
                if (divider) divider.style.background = 'rgba(0, 0, 0, 0.1)';
                
                toolbar.querySelectorAll('button').forEach(btn => {
                    if (!btn.classList.contains('close-btn')) {
                        btn.style.color = '#000000';
                    }
                });
            }
            
            zoomScale = 1;
            translateX = 0;
            translateY = 0;
            
            modal.style.display = 'flex';
            
            setTimeout(() => {
                const containerRect = modalContainer.getBoundingClientRect();
                const contentRect = modalContent.getBoundingClientRect();
                translateX = (containerRect.width - contentRect.width) / 2;
                translateY = (containerRect.height - contentRect.height) / 2;
                updateTransform();
            }, 50);
        }

        function updateTransform() {
            if (modalContent) {
                modalContent.style.transform = `translate(${translateX}px, ${translateY}px) scale(${zoomScale})`;
            }
        }

        function closeZoomModal() {
            document.getElementById('mermaid-zoom-modal').style.display = 'none';
        }

        function zoomIn() {
            zoomScale *= 1.25;
            updateTransform();
        }

        function zoomOut() {
            zoomScale /= 1.25;
            updateTransform();
        }

        function resetZoom() {
            zoomScale = 1;
            if (modalContainer && modalContent) {
                const containerRect = modalContainer.getBoundingClientRect();
                modalContent.style.transform = '';
                const contentRect = modalContent.getBoundingClientRect();
                translateX = (containerRect.width - contentRect.width) / 2;
                translateY = (containerRect.height - contentRect.height) / 2;
                updateTransform();
            }
        }

        // Event delegation cho click vào sơ đồ Mermaid
        document.addEventListener('click', (e) => {
            const mermaidDiv = e.target.closest('.mermaid');
            if (mermaidDiv) {
                openZoomModal(mermaidDiv);
            }
        });

        document.addEventListener('DOMContentLoaded', () => {
            const container = document.getElementById('mermaid-zoom-container');
            
            container.addEventListener('mousedown', (e) => {
                if (e.button !== 0) return;
                isPanning = true;
                container.style.cursor = 'grabbing';
                startX = e.clientX - translateX;
                startY = e.clientY - translateY;
                e.preventDefault();
            });
            
            window.addEventListener('mousemove', (e) => {
                if (!isPanning) return;
                translateX = e.clientX - startX;
                translateY = e.clientY - startY;
                updateTransform();
            });
            
            window.addEventListener('mouseup', () => {
                if (isPanning) {
                    isPanning = false;
                    container.style.cursor = 'grab';
                }
            });
            
            // Phóng to thu nhỏ bằng cuộn chuột (Mouse-centered Zoom giống Figma/CAD)
            container.addEventListener('wheel', (e) => {
                e.preventDefault();
                
                const zoomFactor = 1.15;
                const oldScale = zoomScale;
                
                if (e.deltaY < 0) {
                    zoomScale *= zoomFactor;
                } else {
                    zoomScale /= zoomFactor;
                }
                
                zoomScale = Math.max(0.05, Math.min(zoomScale, 50));
                
                const zoomRatio = zoomScale / oldScale;
                translateX = e.clientX - (e.clientX - translateX) * zoomRatio;
                translateY = e.clientY - (e.clientY - translateY) * zoomRatio;
                
                updateTransform();
            }, { passive: false });
            
            window.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    closeZoomModal();
                }
            });
        });
    </script>
    """

def render_markdown_to_html(filepath: str, is_dark: bool = False) -> dict:
    """Chuyển đổi file Markdown sang HTML.

    Args:
        filepath: Đường dẫn đến file Markdown nguồn.
        is_dark: Cờ sử dụng giao diện tối.

    Returns:
        dict: Dict chứa mã HTML, raw body, và mục lục TOC.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            md_text = f.read()

        html_header = _get_mathjax_mermaid_header(is_dark)

        md = markdown.Markdown(extensions=[
            'extra',
            'nl2br',
            'sane_lists',
            'toc',
            'codehilite',
            'admonition',
            'pymdownx.arithmatex',
            'pymdownx.superfences',
        ], extension_configs={
            'pymdownx.arithmatex': {
                'generic': True,
                'smart_dollar': True
            },
            'pymdownx.superfences': {
                'custom_fences': [
                    {
                        'name': 'mermaid',
                        'class': 'mermaid',
                        'format': pymdownx.superfences.fence_div_format
                    }
                ]
            }
        })

        html_content = md.convert(md_text)
        full_css = get_full_css(is_dark)
        
        zoom_modal_html = _get_mermaid_zoom_modal_html()
        zoom_script = _get_mermaid_zoom_script()

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>{full_css}</style>
            {html_header}
        </head>
        <body class="{'dark-mode' if is_dark else ''}">
            <div class="markdown-body">
                {html_content}
            </div>
            {zoom_modal_html}
            {zoom_script}
        </body>
        </html>
        """
        return {
            "html": html_body,
            "raw_body": html_content,
            "toc": md.toc
        }
    except Exception as e:
        print(f"Lỗi render markdown: {e}")
        return {"html": f"<h1>Lỗi</h1><p>{e}</p>", "raw_body": str(e)}
