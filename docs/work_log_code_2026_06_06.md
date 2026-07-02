<!--
File: docs/work_log_code_2026_06_06.md
Description: Nhật ký thay đổi mã nguồn dự án Markdown Viewer.
CHANGELOG:
- 10:35:00 06/06/2026: [NEW] Khởi tạo nhật ký tích hợp MathJax mở rộng hỗ trợ $, $$ và markdown-body. (Antigravity)
-->

# 📝 NHẬT KÝ THAY ĐỔI MÃ NGUỒN (CODE WORK LOG) - 2026-06-06

## [MARKDOWN_VIEWER] Đồng bộ MathJax mở rộng hỗ trợ mọi định dạng LaTeX (10:35:00 06/06/2026)

- **Mô tả**: Tối ưu hóa MathJax để render mượt mà mọi định dạng công thức LaTeX trực tiếp trên giao diện Viewer mà không bị giới hạn bởi arithmatex parser của Python.
- **Giải pháp**:
    - **Cập nhật delimiters**: Thêm `$` (inline) và `$$` (display) vào các delimiters của đối tượng `window.MathJax` để nhận diện biểu thức toán trực tiếp.
    - **Hỗ trợ LaTeX nâng cao**: Kích hoạt `processEnvironments: true` để tự động render ma trận và các khối phương trình.
    - **Mở rộng phạm vi quét**: Cấu hình `processHtmlClass` trỏ đến `markdown-body` (bao trùm toàn bộ văn bản Markdown render ra) thay vì chỉ thẻ chứa class `arithmatex`.
- **Các file đã thay đổi**:
    - `backend/md_parser.py`: [UPDATE] Cập nhật cấu hình MathJax và thêm changelog header.
- **Thành quả**:
    - Thử nghiệm trên `test_complex_science.md` chạy thành công, MathJax render hoàn hảo mọi công thức toán học cao cấp ngoại tuyến.
