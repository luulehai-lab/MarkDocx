<!--
File: docs/work_log_code_2026_04_18.md
Description: Nhật ký thay đổi mã nguồn dự án Markdown Viewer.
CHANGELOG:
- 15:13:00 18/04/2026: [NEW] Khởi tạo nhật ký công việc. (Antigravity)
-->

# 📝 NHẬT KÝ THAY ĐỔI MÃ NGUỒN (CODE WORK LOG) - 2026-04-18

## [MARKDOWN_VIEWER] Tích hợp hỗ trợ Mermaid Diagrams Offline (15:13:00 18/04/2026)

- **Mô tả**: Nâng cấp ứng dụng để có thể xem được biểu đồ Mermaid trực tiếp trong trình xem Markdown ở chế độ Offline và tự động đồng bộ Theme (Sáng/Tối).
- **Các file đã thay đổi**:
    - `config.py`: Thêm đường dẫn file Mermaid JS local.
    - `backend/md_parser.py`: Tích hợp extension `pymdownx.superfences`, cấu hình render mermaid div, và cập nhật template HTML để nạp JS local.
    - `frontend/styles.py`: Bổ sung CSS làm đẹp cho biểu đồ Mermaid.
    - `test_sample.md`: Thêm ví dụ biểu đồ Mermaid để kiểm tra.
- **Thành quả**: 
    - Render biểu đồ Mermaid mượt bà không cần internet.
    - Đồng bộ màu sắc biểu đồ theo giao diện App.
    - Trải nghiệm người dùng được nâng cấp đáng kể (Premium Aesthetics).

## [MARKDOWN_VIEWER] Hoàn thiện xuất biểu đồ Mermaid sang Word (DOCX) (15:52:00 18/04/2026)

- **Mô tả**: Fix lỗi file Word chỉ hiện code Mermaid và lỗi ảnh trắng.
- **Giải pháp**: 
    - Dùng Regex `re.sub` để thay thế khối Mermaid chuẩn xác trên Windows (newline fix).
    - MermaidRenderer dùng `show()` off-screen để buộc WebEngine vẽ hình vào buffer.
    - Ép màu nền trắng cho ảnh PNG để tương thích Word.
    - Dùng đường dẫn tương đối và `--resource-path` cho Pandoc.
- **Các file đã thay đổi**:
    - `backend/mermaid_renderer.py`: [UPDATE] Refactor toàn diện cơ chế render off-screen và nạp JS.
    - `backend/md_parser.py`: [UPDATE] Chuyển sang dùng Regex và quản lý thư mục ảnh tạm tại chỗ.
- **Thành quả**: Biểu đồ Mermaid trong file Word hiển thị hoàn hảo dưới dạng hình ảnh.

## [MARKDOWN_VIEWER] Fix lỗi KeyError 'toc' (15:54:00 18/04/2026)

- **Mô tả**: Sửa lỗi crash khi mở file do thiếu dữ liệu Mục lục trong kết quả trả về của bộ render.
- **Các file đã thay đổi**:
    - `backend/md_parser.py`: [FIX] Bổ sung trường `toc` vào dictionary kết quả.

---
