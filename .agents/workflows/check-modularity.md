---
description: Kiểm tra và giám sát tuân thủ kỷ luật Modularity (giới hạn 500/800 dòng) của dự án.
---

<!--
File: .agents/workflows/check-modularity.md
Description: Workflow tự động kiểm tra kích thước các file mã nguồn và cảnh báo nguy cơ phình code.
CHANGELOG:
- 14:50:00 11/06/2026: [NEW] Khởi tạo workflow check-modularity giúp duy trì cấu trúc code tinh gọn (Lê Thanh Vân/Antigravity)
-->

# 📊 WORKFLOW: GIÁM SÁT KỶ LUẬT MODULARITY (CHỐNG PHÌNH CODE)

> [!NOTE]
> Workflow này giúp Anh Lưu và Agent kiểm soát chặt chẽ độ dài và cấu trúc của các file Python trong dự án, đảm bảo tuân thủ kỷ luật **Modularity First** (Không vượt quá 800 dòng, chủ động tách module khi đạt 500 dòng).

---

## 🔄 1. Quét Toàn Bộ Dự Án (Project Modularity Scan)

Sử dụng lệnh này để hiển thị danh sách tất cả các file Python trong dự án kèm số dòng thực tế, số lớp, số hàm, và trạng thái cảnh báo phình code.

// turbo
```powershell
python scripts/check_modularity.py --scan
```

---

## 🔍 2. Đánh Giá Tác Động Trước Khi Sửa Code (Pre-modification Audit)

Trước khi thực hiện bất kỳ chỉnh sửa nào trên một file có sẵn, hãy chạy lệnh này để tính toán xem việc thêm code mới có vi phạm giới hạn dòng hay cấu trúc hiện tại hay không.

> [!IMPORTANT]
> - Thay thế `<duong_dan_file>` bằng đường dẫn tương đối tới file cần sửa (ví dụ: `core/services/dxf_parser.py`).
> - Thay thế `<so_dong_du_kien>` bằng số lượng dòng code ước tính sẽ viết thêm (ví dụ: `80`).

// turbo
```powershell
python scripts/check_modularity.py --check-file <duong_dan_file> --add-lines <so_dong_du_kien>
```
