<!--
File: docs/work_log_code_2026_05_30.md
Description: Nhật ký thay đổi mã nguồn dự án Markdown Viewer.
CHANGELOG:
- 10:15:00 30/05/2026: [NEW] Khởi tạo nhật ký tích hợp MathJax offline, xuất PDF, sửa lỗi QAction và cấu hình ảnh WebEngine. (Antigravity)
-->

# 📝 NHẬT KÝ THAY ĐỔI MÃ NGUỒN (CODE WORK LOG) - 2026-05-30

## [MARKDOWN_VIEWER] Tích hợp kết xuất PDF/DOCX, sửa lỗi hiển thị ảnh WebEngine và công thức LaTeX (10:15:00 30/05/2026)

- **Mô tả**: Nâng cấp tính năng render LaTeX offline mượt mà, sửa các lỗi hiển thị hình ảnh online trên WebView, sửa lỗi PyQt6 QAction crash khi khởi động, và đồng bộ cơ chế xuất PDF Premium, xuất DOCX làm sạch LaTeX.
- **Giải pháp**:
    - **Sửa lỗi Qt platform plugin & QAction**: Chuyển đổi cách khởi tạo QAction trong `frontend/main_window.py` từ việc truyền keyword arguments (`triggered`, `shortcut`, `checkable` không được hỗ trợ trong PyQt6) sang gán sự kiện `.triggered.connect()` thủ công và thiết lập thuộc tính trực tiếp.
    - **Sửa lỗi hiển thị ảnh (CORS/Security)**: Cấu hình `QWebEngineSettings` cho WebView chính (`self.web_view`) cho phép truy cập remote URLs từ trang local (`LocalContentCanAccessRemoteUrls=True`) và cho phép truy cập file cục bộ, tự động load ảnh.
    - **Sửa lỗi LaTeX hiển thị dấu $ thừa**: Sửa đổi và hướng dẫn định dạng file markdown mẫu `test_sample.md` chèn dòng trống trước và sau biểu thức block math `$$` để markdown parser nhận diện đúng là display math thay vì inline math (tránh sinh ra dấu `$` thừa bao quanh thẻ span).
    - **Premium Export**: Tích hợp các hàm kết xuất PDF và DOCX cùng hộp thoại Premium mở file/thư mục sau khi hoàn thành.
- **Các file đã thay đổi**:
    - `frontend/main_window.py`: [UPDATE] Sửa lỗi khởi tạo QAction và bổ sung cấu hình QWebEngineSettings cho web_view.
    - `test_sample.md`: [UPDATE] Chèn dòng trống xung quanh biểu thức block math `$$` để đảm bảo định dạng chuẩn.
- **Thành quả**: 
    - Ứng dụng chạy mượt mà ổn định, hiển thị hoàn hảo cả công thức toán LaTeX offline, biểu đồ Mermaid tương tác zoom/pan, và các hình ảnh online từ internet.
    - Các nút PDF/DOCX xuất file nhanh chóng, giữ nguyên định dạng hoặc dịch LaTeX sang ký tự Unicode in nghiêng phẳng sạch sẽ.

---
