# Tên file: backend/exporters.py
# CHỨC NĂNG: Cung cấp logic xuất văn bản ra định dạng Word (.docx) hỗ trợ xuất biểu đồ và công thức.
# CHANGELOG:
# - 15:15:00 02/07/2026: [NEW] Khởi tạo exporters component chứa hàm export_to_docx tách từ md_parser.py (Lê Thanh Vân/Antigravity)

import os
import re
import logging
import pypandoc
from backend.mermaid_renderer import MermaidRenderer
from backend.md_parser import clean_latex_in_markdown

logger = logging.getLogger(__name__)

def export_to_docx(src_filepath: str, dest_filepath: str, landscape: bool = False, is_dark: bool = False) -> bool:
    """Xuất file Markdown sang định dạng Word (.docx).
    
    Tự động quét các khối Mermaid, dựng thành hình ảnh tạm và nhúng tương đối vào tài liệu 
    trước khi sử dụng Pandoc để chuyển đổi.

    Args:
        src_filepath: Đường dẫn file Markdown nguồn.
        dest_filepath: Đường dẫn lưu file DOCX kết quả.
        landscape: Trạng thái xoay ngang tài liệu.
        is_dark: Trạng thái áp dụng theme tối cho ảnh Mermaid.

    Returns:
        bool: True nếu xuất file thành công, False nếu thất bại.
    """
    try:
        src_dir = os.path.dirname(os.path.abspath(src_filepath))
        with open(src_filepath, 'r', encoding='utf-8') as f:
            md_text = f.read()

        # Thư mục chứa ảnh tạm tại chỗ
        temp_img_dir = os.path.join(src_dir, "_mermaid_temp")
        temp_md_path = src_filepath + ".export_temp.md"
        
        renderer = None
        
        # Regex "Siêu cấp": bắt mọi ký tự kể cả xuống dòng, khoảng trắng thừa
        pattern = re.compile(r'```mermaid\s*[\r\n]+([\s\S]*?)\s*```', re.IGNORECASE)
        matches = pattern.findall(md_text)
        
        if matches:
            logger.info(f"Tìm thấy {len(matches)} khối Mermaid. Bắt đầu Render...")
            os.makedirs(temp_img_dir, exist_ok=True)
            renderer = MermaidRenderer()
            renderer.temp_dir = temp_img_dir
            
            def replace_mermaid(match):
                content = match.group(1).strip()
                try:
                    logger.debug(f"Đang render biểu đồ: {content[:30]}...")
                    # Renderer bây giờ sẽ lưu vào thư mục tại chỗ
                    img_path_abs = renderer.render_to_image(content, is_dark)
                    img_filename = os.path.basename(img_path_abs)
                    
                    if os.path.exists(img_path_abs):
                        size = os.path.getsize(img_path_abs)
                        logger.info(f"Render Mermaid thành công: {img_filename} ({size} bytes)")
                    
                    # Dùng đường dẫn TƯƠNG ĐỐI để Pandoc không bị lỗi dấu cách (%20)
                    return f"![](_mermaid_temp/{img_filename})"
                except Exception as e:
                    logger.error(f"Render block Mermaid thất bại: {e}", exc_info=True)
                    return match.group(0)

            # Thực hiện thay thế tất cả
            md_text = pattern.sub(replace_mermaid, md_text)
        else:
            logger.info("Không tìm thấy khối Mermaid nào trong văn bản.")

        # Làm sạch LaTeX trong Markdown tạm trước khi xuất DOCX
        md_text = clean_latex_in_markdown(md_text)

        with open(temp_md_path, 'w', encoding='utf-8') as f:
            f.write(md_text)

        # 2. Chạy Pandoc
        args = [
            '--resource-path', src_dir,
            '--extract-media', src_dir
        ]
        if landscape:
            if os.path.exists('template_landscape.docx'):
                args.append('--reference-doc=template_landscape.docx')
        
        pypandoc.convert_file(temp_md_path, 'docx', outputfile=dest_filepath, extra_args=args)

        # 3. Dọn dẹp
        if os.path.exists(temp_md_path):
            os.remove(temp_md_path)
        
        if os.path.exists(temp_img_dir):
            for f in os.listdir(temp_img_dir):
                try:
                    os.remove(os.path.join(temp_img_dir, f))
                except OSError as e:
                    logger.debug(f"Không thể xóa file tạm {f}: {e}")
            try:
                os.rmdir(temp_img_dir)
            except OSError as e:
                logger.debug(f"Không thể xóa thư mục tạm {temp_img_dir}: {e}")
            
        return True
    except Exception as e:
        logger.error(f"Lỗi export DOCX: {e}", exc_info=True)
        return False
