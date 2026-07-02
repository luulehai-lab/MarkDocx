# Tên file: scripts/init_db.py
# CHỨC NĂNG: Khởi tạo các bảng cơ sở dữ liệu trên Supabase/SQLite từ các model SQLAlchemy
# CHANGELOG:
# - 11:49:13 02/07/2026: [NEW] Cập nhật mã nguồn (Antigravity)
# - 11:09:00 02/07/2026: [NEW] Khởi tạo script cấu hình database (Lê Thanh Vân/Antigravity)

import sys
import os
import logging

# Đảm bảo đường dẫn gốc của dự án được thêm vào PYTHONPATH ở vị trí đầu tiên để tránh xung đột với thư viện config hệ thống
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import engine, Base
from core.models import Project, Drawing, DrawingLog, BOMDetail  # noqa: F401

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("init_db")


def initialize_database() -> bool:
    """Khởi tạo tất cả các bảng trong cơ sở dữ liệu dựa trên SQLAlchemy Models.

    Đọc cấu hình database từ engine đã thiết lập trong core.database,
    sau đó thực hiện tạo tất cả các bảng nếu chúng chưa tồn tại.

    Returns:
        bool: True nếu khởi tạo thành công, False nếu xảy ra lỗi.
    """
    logger.info("Bắt đầu quá trình tạo các bảng cơ sở dữ liệu...")
    try:
        # Chạy lệnh tạo tất cả các bảng
        Base.metadata.create_all(bind=engine)
        logger.info("Khởi tạo tất cả các bảng cơ sở dữ liệu thành công!")
        return True
    except Exception as e:
        logger.error("Đã xảy ra lỗi nghiêm trọng khi khởi tạo cơ sở dữ liệu: %s", str(e), exc_info=True)
        return False


if __name__ == "__main__":
    success = initialize_database()
    sys.exit(0 if success else 1)
