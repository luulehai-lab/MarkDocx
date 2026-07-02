# Tên file: scripts/dxf_to_excel_boq.py
# CHỨC NĂNG: CLI Script chính thức hỗ trợ truyền tham số để chạy pipeline số hóa bản vẽ DXF sang Excel BOQ Premium.
# CHANGELOG:
# - 11:49:13 02/07/2026: [NEW] Cập nhật mã nguồn (Antigravity)
# - 17:03:17 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 17:00:33 19/06/2026: [UPDATE] feat(audit): integrate clean code AST auditor and sync workspace updates (Antigravity)
# - 11:20:00 23/05/2026: [UPDATE] Tích hợp bước Parser sinh JSON trung gian và Renderer vẽ Excel riêng biệt (Antigravity/Anh Lưu)
# - 10:25:00 23/05/2026: [NEW] Khởi tạo tệp chạy CLI chính thức cho pipeline DXF-Excel với argparse và type hints (Antigravity/Anh Lưu)

import argparse
import os
import sys

# Thiết lập đường dẫn thư mục gốc để import được gói core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.dxf_boq import create_premium_excel_multisheet, parse_dxf_to_json


def main() -> None:
    """Hàm chạy chính điều phối nhận đối số dòng lệnh và kích hoạt pipeline số hóa DXF."""
    parser = argparse.ArgumentParser(description="Pipeline số hóa bản vẽ CAD DXF sang Excel BOQ Premium của TLS.")

    # Định nghĩa các tham số đầu vào
    parser.add_argument(
        "--dxf",
        type=str,
        default=r"D:\CloudStation\TL DRIVE\2026\02_S31-60\044_CET_MDF_DA_NANG_190526\A\01_BV_185\NX3.dxf",
        help="Đường dẫn đến tệp DXF nguồn.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=r"D:\CloudStation\TL DRIVE\2026\02_S31-60\044_CET_MDF_DA_NANG_190526\A\01_BV_185\044_CET_MDF_DA_NANG_NX3_Thong_Ke_Ket_Cau.xlsx",
        help="Đường dẫn lưu tệp Excel BOQ đầu ra.",
    )

    args = parser.parse_args()

    if not os.path.exists(args.dxf):
        print(f"[ERROR] Không tìm thấy tệp DXF nguồn tại: {args.dxf}")
        sys.exit(1)

    print("==================================================================================")
    print("=== KÍCH HOẠT PIPELINE SỐ HÓA CAD DXF SANG EXCEL BOQ (PARSER & RENDERER) ===")
    print("==================================================================================")
    print(f"  - Tệp DXF nguồn: {args.dxf}")
    print(f"  - Tệp Excel đích: {args.output}")

    # Định nghĩa tệp dữ liệu trung gian sạch JSON nằm cạnh Excel đầu ra
    output_json = os.path.splitext(args.output)[0] + "_data.json"
    print(f"  - Tệp JSON dữ liệu trung gian: {output_json}")
    print("----------------------------------------------------------------------------------")

    try:
        # Bước 1: Quét DXF thô và dimension, trích xuất dữ liệu thực chứng ra JSON trung gian
        print("[STEP 1/2] Đang quét DXF và sinh tệp JSON dữ liệu thực chứng trung gian...")
        parse_dxf_to_json(dxf_path=args.dxf, output_json_path=output_json)

        # Bước 2: Đọc dữ liệu JSON trung gian và render vẽ báo cáo Excel Premium của TLS
        print("[STEP 2/2] Đang đọc tệp JSON trung gian và vẽ báo cáo Excel BOQ Premium...")
        create_premium_excel_multisheet(output_path=args.output, dxf_path=args.dxf, json_data_path=output_json)

        print("==================================================================================")
        print("=== [SUCCESS] PIPELINE SỐ HÓA CAD DXF SANG EXCEL HOÀN THÀNH RỰC RỠ! ===")
        print("==================================================================================")
    except Exception as e:
        print(f"[FATAL ERROR] Lỗi nghiêm trọng khi thực thi pipeline: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
