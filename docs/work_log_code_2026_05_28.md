<!--
File: docs/work_log_code_2026_05_28.md
Description: Nhật ký thay đổi mã nguồn dự án Markdown Viewer.
CHANGELOG:
- 17:23:00 28/05/2026: [UPDATE] Tích hợp tính năng Click-to-Zoom và Pan Premium tương tác cực đỉnh cho sơ đồ Mermaid. (Antigravity)
- 17:19:00 28/05/2026: [NEW] Khởi tạo nhật ký sửa lỗi hiển thị sơ đồ Mermaid kích thước lớn. (Antigravity)
-->

# 📝 NHẬT KÝ THAY ĐỔI MÃ NGUỒN (CODE WORK LOG) - 2026-05-28

## [MARKDOWN_VIEWER] Tích hợp tính năng Click-to-Zoom và Kéo thả (Pan) cho sơ đồ Mermaid (17:23:00 28/05/2026)

- **Mô tả**: Tích hợp cơ chế xem tương tác cho phép click vào bất kỳ sơ đồ Mermaid nào để phóng to, thu nhỏ và kéo thả di chuyển giúp người dùng dễ dàng xem các sơ đồ kích thước lớn và chi tiết.
- **Giải pháp**:
    - Thiết kế một Modal Overlay với hiệu ứng Glassmorphism mờ nền (`backdrop-filter: blur(12px)`) cực kỳ hiện đại và sang trọng.
    - Phát triển thuật toán kéo thả (Pan) mượt mà và thuật toán phóng to thu nhỏ cuộn chuột lấy tâm con trỏ chuột làm tiêu điểm (Mouse-centered Zoom) tương tự Figma, CAD.
    - Thêm các nút điều khiển trực quan (➕, ➖, 🔄, ✕) trên Toolbar trong suốt và hỗ trợ phím tắt `Esc` để đóng nhanh.
    - Cải thiện CSS hover cho `.mermaid`: tăng tương tác với hiệu ứng dịch chuyển nhẹ `translateY(-2px)`, đổ bóng mịn màng và đổi màu viền sang màu nhấn (accent-color) của giao diện đang chọn.
- **Các file đã thay đổi**:
    - `backend/md_parser.py`: [NEW] Tích hợp cấu trúc HTML của modal và mã Javascript xử lý các sự kiện Drag/Wheel/Esc vào luồng render HTML của tài liệu.
    - `frontend/styles.py`: [UPDATE] Bổ sung các hiệu ứng chuyển động mượt mà và CSS hover Premium cho `.mermaid`.
- **Thành quả**: Trải nghiệm xem biểu đồ nâng lên một tầm cao mới (Wow effect), cực kỳ trực quan và tiện dụng khi phân tích cấu trúc codebase phức tạp của Anh Lưu.

## [MARKDOWN_VIEWER] Nâng cấp cấu hình Mermaid hiển thị biểu đồ kích thước lớn (17:19:00 28/05/2026)

- **Mô tả**: Sửa lỗi "Maximum text size in diagram exceeded" khi render các file markdown chứa sơ đồ/đồ thị Mermaid quá lớn (như đồ thị liên kết của codebase sinh ra tự động).
- **Giải pháp**: 
    - Nâng cấu hình `maxTextSize` của `mermaid.initialize` lên `10000000` (10 triệu ký tự) cho cả trình xem trực tiếp (WebView) và bộ xuất ảnh DOCX (MermaidRenderer).
    - Chuẩn hóa Type Hints và bổ sung Google-style Docstrings cho các phương thức được sửa đổi để loại bỏ nợ kỹ thuật (Technical Debt).
- **Các file đã thay đổi**:
    - `backend/md_parser.py`: [UPDATE] Bổ sung cấu hình `maxTextSize: 10000000` trong phần init script, cập nhật docstring dạng Google-style cho hàm `render_markdown_to_html`.
    - `backend/mermaid_renderer.py`: [UPDATE] Bổ sung cấu hình `maxTextSize: 10000000` trong init script thầm lặng, cập nhật docstring dạng Google-style cho hàm `render_to_image`.
- **Thành quả**: 
    - Hiển thị hoàn hảo mọi biểu đồ Mermaid kích thước lớn mà không còn bị giới hạn bởi giới hạn mặc định (50,000 ký tự) của Mermaid.js.
    - Duy trì sự chuyên nghiệp, sạch sẽ trong mã nguồn với chuẩn Type Hints và Docstrings đầy đủ.

---
