<!--
File: docs/work_log_code_2026_07_02.md
CHỨC NĂNG: Nhật ký công việc mã nguồn dự án ERP TK-KH
CHANGELOG:
- 10:45:00 02/07/2026: [NEW] Khởi tạo nhật ký công việc (Lê Thanh Vân/Antigravity)
-->

# 📝 NHẬT KÝ CÔNG VIỆC MÃ NGUỒN - 02/07/2026

## [55_ERP_TK_KH_01726] Hoàn thành core services và khung giao diện PyQt6 (11:15)

- **Người thực hiện**: Lê Thanh Vân (Antigravity)
- **Danh sách file đã tạo/sửa đổi**:
  - `[NEW]` [scripts/init_db.py](file:///D:/CloudStation/CODE/PYTHON_APP/55_ERP_TK_KH_01726/scripts/init_db.py) - Script khởi tạo cơ sở dữ liệu.
  - `[NEW]` [core/services/project_service.py](file:///D:/CloudStation/CODE/PYTHON_APP/55_ERP_TK_KH_01726/core/services/project_service.py) - Service quản lý Dự án (CRUD).
  - `[NEW]` [core/services/drawing_service.py](file:///D:/CloudStation/CODE/PYTHON_APP/55_ERP_TK_KH_01726/core/services/drawing_service.py) - Service quản lý Bản vẽ & Logs trạng thái.
  - `[NEW]` [scratch/test_services.py](file:///D:/CloudStation/CODE/PYTHON_APP/55_ERP_TK_KH_01726/scratch/test_services.py) - Unit test cho các service.
  - `[NEW]` [ui/main_window.py](file:///D:/CloudStation/CODE/PYTHON_APP/55_ERP_TK_KH_01726/ui/main_window.py) - Giao diện chính PyQt6 (Sidebar, QStackedWidget).
  - `[NEW]` [ui/views/thiet_ke_view.py](file:///D:/CloudStation/CODE/PYTHON_APP/55_ERP_TK_KH_01726/ui/views/thiet_ke_view.py) - Màn hình ban hành bản vẽ của Thiết kế.
  - `[NEW]` [ui/views/ke_hoach_view.py](file:///D:/CloudStation/CODE/PYTHON_APP/55_ERP_TK_KH_01726/ui/views/ke_hoach_view.py) - Màn hình tiếp nhận và chuyển xưởng của Kế hoạch.
  - `[NEW]` [main.py](file:///D:/CloudStation/CODE/PYTHON_APP/55_ERP_TK_KH_01726/main.py) - File khởi động chính của ứng dụng.

- **Mô tả chi tiết**:
  - Viết script khởi tạo cơ sở dữ liệu trên Cloud Supabase DB PostgreSQL và đã chạy thành công.
  - Hoàn thành viết logic nghiệp vụ cho Project và Drawing theo các quy chuẩn Clean Code nghiêm ngặt (Type Hints 100%, Google-Style Docstring, giới hạn soft/hard dòng và đối số).
  - Hoàn thành viết bộ kiểm thử tự động `test_services.py` chạy trên SQLite bộ nhớ và kết quả pass 100%.
  - Thiết kế và hoàn thiện toàn bộ giao diện PyQt6 đẹp mắt (Premium Slate theme) kết nối an toàn với tầng logic nghiệp vụ, đáp ứng đầy đủ tính năng ban hành bản vẽ (Thiết kế) và tiếp nhận, mở Drive, xác nhận sản xuất (Kế hoạch).
  - **[UPDATE - 11:20]**: Tối ưu hóa trải nghiệm người dùng bằng cách di chuyển bộ chọn Dự án sang thanh Sidebar bên trái (Left Panel) làm bộ chọn dùng chung. Đồng thời cải tiến layout theo yêu cầu của Anh Lưu:
    - Sidebar bên trái hiển thị danh sách dự án trải rộng (`QListWidget`), người dùng click chọn trực tiếp không cần click qua ComboBox.
    - Hai nút chuyển view ("Ban hành bản vẽ" và "Tiếp nhận sản xuất") được chuyển lên thanh HeaderBar nằm ngang trên cùng bên phải dưới dạng tab bar phẳng hiện đại.
    - Khi tạo dự án mới ở màn hình Thiết kế, danh sách dự án ở Sidebar sẽ tự động làm mới và tự động chọn (highlight) dự án mới tạo đó ngay lập tức.
    - **[PERF - 11:25]**: Giải quyết triệt để hiện tượng đơ giật giao diện (chậm 10s) bằng cơ chế Lazy Loading và State Caching. Dữ liệu bản vẽ chỉ được load cho active view. Khi chuyển đổi tab qua lại, nếu mã dự án không thay đổi, hệ thống sẽ bỏ qua truy vấn database giúp việc chuyển tab phản hồi tức thời (0s).
    - **[PERF - 11:30]**: Khắc phục triệt để hiện tượng đơ giật (chậm 10s) khi click chọn dự án ở Sidebar. Tạo module luồng phụ `ui/common/workers.py` chứa class `DrawingLoaderThread(QThread)` để truy vấn cơ sở dữ liệu ngầm và phát tín hiệu. Bảng danh sách bản vẽ hiển thị trạng thái `"⏳ Đang tải bản vẽ..."` và cập nhật bất đồng bộ mà không bao giờ block UI Thread của PyQt6. Giao diện mượt mà 100% khi bấm chọn dự án liên tục.

## [55_ERP_TK_KH_01726] Khởi tạo dự án và thiết lập kiến trúc chuẩn (10:45)

- **Người thực hiện**: Lê Thanh Vân (Antigravity)
- **Danh sách file đã tạo/sửa đổi**:
  - `[NEW]` Sao chép `.agents/` (rules, workflows, skills) sang thư mục dự án mới.
  - `[NEW]` Sao chép `scripts/` (audit_code_quality, git_guard, check_modularity...) sang thư mục dự án mới.
  - `[NEW]` [ARCHITECTURE_MAP.md](file:///D:/CloudStation/CODE/PYTHON_APP/55_ERP_TK_KH_01726/docs/architecture/ARCHITECTURE_MAP.md) - Bản đồ Master kiến trúc.
  - `[NEW]` [MAP_GRAPH.md](file:///D:/CloudStation/CODE/PYTHON_APP/55_ERP_TK_KH_01726/docs/architecture/MAP_GRAPH.md) - Sơ đồ codebase.
  - `[NEW]` `.gitignore` - Bỏ qua file rác.
  - `[NEW]` `docs/work_log_code_2026_07_02.md` - Nhật ký công việc đầu tiên.

- **Mô tả chi tiết**:
  - Thống nhất giải pháp kỹ thuật: Sử dụng giao diện Desktop App **PyQt6** kết nối với **Cloud Database Supabase (PostgreSQL)** miễn phí, kết hợp quản lý file bản vẽ nặng thông qua shareable link **Google Drive**.
  - Thiết lập rào chắn kiến trúc phân tách trách nhiệm (Separation of Concerns): Tách biệt tầng UI PyQt6 với Core Logic / DB Service.
  - Tạo cấu trúc thư mục sạch chuẩn bị cho việc viết code.
