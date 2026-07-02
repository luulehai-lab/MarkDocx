# Tên file: frontend/styles.py
# CHỨC NĂNG: Định nghĩa hệ thống CSS cho Markdown và các thành phần giao diện.
# CHANGELOG:
# - 15:00:00 02/07/2026: [REFACTOR] Tách chuỗi CSS tĩnh ra hằng số module MARKDOWN_CSS_BODY để rút ngắn get_full_css xuống dưới 15 dòng (Lê Thanh Vân/Antigravity)
# - 17:20:00 28/05/2026: [UPDATE] Nâng cấp hiệu ứng hover cho .mermaid mang lại trải nghiệm Premium. (Antigravity)

MARKDOWN_CSS_DARK = """
:root {
    --bg-color: #0d1117;
    --card-bg: #161b22;
    --text-main: #c9d1d9;
    --text-muted: #8b949e;
    --accent-color: #58a6ff;
    --border-color: #30363d;
    --code-bg: #1f242c;
    --quote-border: #30363d;
}
"""

MARKDOWN_CSS_LIGHT = """
:root {
    --bg-color: #f6f8fa;
    --card-bg: #ffffff;
    --text-main: #24292e;
    --text-muted: #57606a;
    --accent-color: #0969da;
    --border-color: #d0d7de;
    --code-bg: #f6f8fa;
    --quote-border: #d0d7de;
}
"""

MARKDOWN_CSS_BODY = """
img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 10px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

body {
    background-color: var(--bg-color);
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: var(--text-main);
    line-height: 1.6;
}

.markdown-body {
    box-sizing: border-box;
    width: 100%;
    max-width: 900px;
    margin: 30px 20px;
    padding: 60px 80px;
    background-color: var(--card-bg);
    border-radius: 4px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    border: 1px solid var(--border-color);
    min-height: calc(100vh - 60px);
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-main);
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    font-weight: 700;
}

h1 { font-size: 2.2rem; border-bottom: 2px solid var(--border-color); padding-bottom: 0.3em; }
h2 { font-size: 1.8rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.3em; }

p { margin-bottom: 1.2em; font-size: 1.05rem; }

a { color: var(--accent-color); text-decoration: none; }
a:hover { text-decoration: underline; }

/* Tables */
table {
    display: block;
    width: 100%;
    overflow-x: auto;
    border-collapse: collapse;
    margin: 2em 0;
    border: 1px solid var(--border-color);
    -webkit-overflow-scrolling: touch;
}

table th {
    background-color: var(--code-bg);
    font-weight: 600;
    padding: 12px 15px;
    border: 1px solid var(--border-color);
}

table td {
    padding: 10px 15px;
    border: 1px solid var(--border-color);
    min-width: 80px;
}

/* Code */
code {
    background-color: var(--code-bg);
    padding: 0.2em 0.4em;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.9em;
}

pre {
    background-color: var(--code-bg);
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    border: 1px solid var(--border-color);
}

/* TOC Styling (Optional if rendered in HTML) */
.toc {
    margin-bottom: 40px;
    padding: 20px;
    background: var(--code-bg);
    border-radius: 8px;
    border: 1px solid var(--border-color);
}
.toc ul { list-style: none; padding-left: 1.5em; }
.toc > ul { padding-left: 0; }
.toc a { color: var(--text-muted); font-size: 0.95rem; }
.toc a:hover { color: var(--accent-color); }

/* Scrollbar */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #555; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #888; }

.mermaid {
    background-color: var(--card-bg);
    display: flex;
    justify-content: center;
    padding: 20px;
    margin: 20px 0;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    cursor: zoom-in;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.2s, box-shadow 0.2s;
}
.mermaid:hover {
    transform: translateY(-2px);
    border-color: var(--accent-color);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

@media print {
    body { background-color: white; padding: 0; }
    .markdown-body { 
        box-shadow: none; 
        border: none; 
        margin: 0; 
        max-width: none;
        width: 100%;
    }
    table { overflow: visible; display: table; }
}
"""


def get_full_css(is_dark: bool = False) -> str:
    """Trả về CSS đầy đủ cho Markdown và giao diện.

    Args:
        is_dark (bool): Cờ bật chế độ tối.

    Returns:
        str: Chuỗi CSS định dạng hoàn chỉnh.
    """
    theme_vars = MARKDOWN_CSS_DARK if is_dark else MARKDOWN_CSS_LIGHT
    return theme_vars + MARKDOWN_CSS_BODY