# Tên file: backend/logger.py
# CHỨC NĂNG: Cấu hình hệ thống logging toàn cục và bắt ngoại lệ unhandled crash cho ứng dụng
# CHANGELOG:
# - 15:35:00 08/07/2026: [NEW] Khởi tạo module logger để thiết lập RotatingFileHandler và sys.excepthook (Antigravity)

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from typing import Any


def handle_exception(
    exc_type: type[BaseException], exc_value: BaseException, exc_traceback: Any
) -> None:
    """Xử lý các ngoại lệ chưa được bắt (Unhandled Exception) và ghi vào log.

    Args:
        exc_type: Kiểu ngoại lệ.
        exc_value: Giá trị ngoại lệ.
        exc_traceback: Traceback đối tượng chứa thông tin dòng lỗi.
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger = logging.getLogger("root")
    logger.critical(
        "Unhandled exception detected:", exc_info=(exc_type, exc_value, exc_traceback)
    )


def setup_logging(log_dir: str) -> None:
    """Thiết lập cấu hình logging cho ứng dụng bao gồm console và file rotating.

    Args:
        log_dir: Thư mục chứa tệp tin log.
    """
    log_file = os.path.join(log_dir, "markdown_viewer.log")

    # Định dạng log
    log_format = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    formatter = logging.Formatter(log_format)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Xóa các handler mặc định nếu có để tránh lặp log
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # File handler (Rotating: 5MB mỗi file, tối đa 3 file backup)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)

    # Gắn móc unhandled exception
    sys.excepthook = handle_exception

    root_logger.info("--- HỆ THỐNG LOGGING ĐÃ ĐƯỢC KHỞI TẠO THÀNH CÔNG ---")
