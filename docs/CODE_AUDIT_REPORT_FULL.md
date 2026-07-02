
* ─Éiß╗âm chß║Ñt l╞░ß╗úng m├ú nguß╗ôn: ≡ƒƒó **9.9/10.0**
* ─Éß╗Ö bao phß╗º Type Hints: **20.0%** (14/70 h├ám)
* Tß╗òng sß╗æ Lß╗ùi nß║╖ng (High Error): **11**
* Tß╗òng sß╗æ Cß║únh b├ío (Warning): **142**
# ≡ƒ¢í∩╕Å B├üO C├üO KIß╗éM TO├üN CHß║ñT L╞»ß╗óNG M├â NGUß╗ÆN (CLEAN CODE AUDIT)

* ─Éiß╗âm chß║Ñt l╞░ß╗úng m├ú nguß╗ôn: ≡ƒƒó **9.9/10.0**
* ─Éß╗Ö bao phß╗º Type Hints: **20.0%** (14/70 h├ám)
* Tß╗òng sß╗æ Lß╗ùi nß║╖ng (High Error): **11**
* Tß╗òng sß╗æ Cß║únh b├ío (Warning): **142**

## Γ¥î C├üC Lß╗ûI Nß║╢NG Cß║ªN Sß╗¼A NGAY (BLOCK COMMIT)
| File | D├▓ng | Loß║íi lß╗ùi | Chi tiß║┐t vi phß║ím |
| :--- | :---: | :--- | :--- |
| `backend/md_parser.py` | 201 | `FUNCTION_LIMIT_EXCEEDED` | H├ám `render_markdown_to_html` d├ái 301 d├▓ng, v╞░ß╗út qu├í giß╗¢i hß║ín cß╗⌐ng 100 d├▓ng. |
| `backend/md_parser.py` | 577 | `SILENT_EXCEPTION` | Nuß╗æt lß╗ùi im lß║╖ng bß║▒ng `pass` hoß║╖c `continue` trong except Exception. |
| `backend/md_parser.py` | 575 | `SILENT_EXCEPTION` | Nuß╗æt lß╗ùi im lß║╖ng bß║▒ng `pass` hoß║╖c `continue` trong except Exception. |
| `backend/mermaid_renderer.py` | 30 | `FUNCTION_LIMIT_EXCEEDED` | H├ám `render_to_image` d├ái 125 d├▓ng, v╞░ß╗út qu├í giß╗¢i hß║ín cß╗⌐ng 100 d├▓ng. |
| `backend/mermaid_renderer.py` | 161 | `SILENT_EXCEPTION` | Nuß╗æt lß╗ùi im lß║╖ng bß║▒ng `pass` hoß║╖c `continue` trong except Exception. |
| `frontend/main_window.py` | 251 | `FUNCTION_LIMIT_EXCEEDED` | H├ám `_init_ui` d├ái 106 d├▓ng, v╞░ß╗út qu├í giß╗¢i hß║ín cß╗⌐ng 100 d├▓ng. |
| `frontend/main_window.py` | 458 | `SILENT_EXCEPTION` | Nuß╗æt lß╗ùi im lß║╖ng bß║▒ng `pass` hoß║╖c `continue` trong except Exception. |
| `frontend/main_window.py` | 637 | `SILENT_EXCEPTION` | Nuß╗æt lß╗ùi im lß║╖ng bß║▒ng `pass` hoß║╖c `continue` trong except Exception. |
| `frontend/main_window.py` | 447 | `SILENT_EXCEPTION` | Nuß╗æt lß╗ùi im lß║╖ng bß║▒ng `pass` hoß║╖c `continue` trong except Exception. |
| `frontend/main_window.py` | 656 | `SILENT_EXCEPTION` | Nuß╗æt lß╗ùi im lß║╖ng bß║▒ng `pass` hoß║╖c `continue` trong except Exception. |
| `frontend/styles.py` | 32 | `FUNCTION_LIMIT_EXCEEDED` | H├ám `get_full_css` d├ái 148 d├▓ng, v╞░ß╗út qu├í giß╗¢i hß║ín cß╗⌐ng 100 d├▓ng. |

## ΓÜá∩╕Å C├üC Cß║óNH B├üO Tß╗ÉI ╞»U (WARNING)
| File | D├▓ng | Loß║íi cß║únh b├ío | Chi tiß║┐t |
| :--- | :---: | :--- | :--- |
| `config.py` | 1 | `HEADER_MISSING` | Thiß║┐u Header Changelog chuß║⌐n dß╗▒ ├ín (Thiß║┐u: Chß╗⌐c n─âng). |
| `main.py` | 1 | `HEADER_MISSING` | Thiß║┐u Header Changelog chuß║⌐n dß╗▒ ├ín (Thiß║┐u: Chß╗⌐c n─âng). |
| `main.py` | 9 | `TYPE_HINT_MISSING` | H├ám `main` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `main.py` | 9 | `DOCSTRING_MISSING` | H├ám `main`: Thiß║┐u Docstring. |
| `backend/md_parser.py` | 20 | `DOCSTRING_MISSING` | H├ám `find_matching_brace`: Thiß║┐u phß║ºn m├┤ tß║ú ─æß╗æi sß╗æ 'Args:' trong Docstring, Thiß║┐u phß║ºn m├┤ tß║ú kiß╗âu trß║ú vß╗ü 'Returns:' trong Docstring. |
| `backend/md_parser.py` | 32 | `DOCSTRING_MISSING` | H├ám `parse_braces_content`: Thiß║┐u phß║ºn m├┤ tß║ú ─æß╗æi sß╗æ 'Args:' trong Docstring, Thiß║┐u phß║ºn m├┤ tß║ú kiß╗âu trß║ú vß╗ü 'Returns:' trong Docstring. |
| `backend/md_parser.py` | 77 | `FUNCTION_TOO_LONG` | H├ám `latex_to_unicode` d├ái 85 d├▓ng, v╞░ß╗út qu├í giß╗¢i hß║ín mß╗üm 50 d├▓ng. |
| `backend/md_parser.py` | 77 | `DOCSTRING_MISSING` | H├ám `latex_to_unicode`: Thiß║┐u phß║ºn m├┤ tß║ú ─æß╗æi sß╗æ 'Args:' trong Docstring, Thiß║┐u phß║ºn m├┤ tß║ú kiß╗âu trß║ú vß╗ü 'Returns:' trong Docstring. |
| `backend/md_parser.py` | 163 | `DOCSTRING_MISSING` | H├ám `clean_latex_in_markdown`: Thiß║┐u phß║ºn m├┤ tß║ú ─æß╗æi sß╗æ 'Args:' trong Docstring, Thiß║┐u phß║ºn m├┤ tß║ú kiß╗âu trß║ú vß╗ü 'Returns:' trong Docstring. |
| `backend/md_parser.py` | 185 | `DOCSTRING_MISSING` | H├ám `open_file_with_default_app`: Thiß║┐u phß║ºn m├┤ tß║ú ─æß╗æi sß╗æ 'Args:' trong Docstring, Thiß║┐u phß║ºn m├┤ tß║ú kiß╗âu trß║ú vß╗ü 'Returns:' trong Docstring. |
| `backend/md_parser.py` | 193 | `DOCSTRING_MISSING` | H├ám `open_folder_and_select_file`: Thiß║┐u phß║ºn m├┤ tß║ú ─æß╗æi sß╗æ 'Args:' trong Docstring, Thiß║┐u phß║ºn m├┤ tß║ú kiß╗âu trß║ú vß╗ü 'Returns:' trong Docstring. |
| `backend/md_parser.py` | 503 | `FUNCTION_TOO_LONG` | H├ám `export_to_docx` d├ái 80 d├▓ng, v╞░ß╗út qu├í giß╗¢i hß║ín mß╗üm 50 d├▓ng. |
| `backend/md_parser.py` | 503 | `TYPE_HINT_MISSING` | H├ám `export_to_docx` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `backend/md_parser.py` | 503 | `DOCSTRING_MISSING` | H├ám `export_to_docx`: Thiß║┐u phß║ºn m├┤ tß║ú ─æß╗æi sß╗æ 'Args:' trong Docstring. |
| `backend/md_parser.py` | 105 | `DOCSTRING_MISSING` | H├ám `process_recursive_commands`: Thiß║┐u Docstring. |
| `backend/md_parser.py` | 148 | `TYPE_HINT_MISSING` | H├ám `replace_sub` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `match`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `backend/md_parser.py` | 148 | `DOCSTRING_MISSING` | H├ám `replace_sub`: Thiß║┐u Docstring. |
| `backend/md_parser.py` | 154 | `TYPE_HINT_MISSING` | H├ám `replace_super` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `match`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `backend/md_parser.py` | 154 | `DOCSTRING_MISSING` | H├ám `replace_super`: Thiß║┐u Docstring. |
| `backend/md_parser.py` | 165 | `TYPE_HINT_MISSING` | H├ám `replace_block_math` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `match`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `backend/md_parser.py` | 165 | `DOCSTRING_MISSING` | H├ám `replace_block_math`: Thiß║┐u Docstring. |
| `backend/md_parser.py` | 170 | `TYPE_HINT_MISSING` | H├ám `replace_inline_math` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `match`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `backend/md_parser.py` | 170 | `DOCSTRING_MISSING` | H├ám `replace_inline_math`: Thiß║┐u Docstring. |
| `backend/md_parser.py` | 527 | `TYPE_HINT_MISSING` | H├ám `replace_mermaid` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `match`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `backend/md_parser.py` | 527 | `DOCSTRING_MISSING` | H├ám `replace_mermaid`: Thiß║┐u Docstring. |
| `backend/md_parser.py` | 500 | `RAW_PRINT_CALL` | Sß╗¡ dß╗Ñng lß╗çnh `print()` trß╗▒c tiß║┐p. H├úy chuyß╗ân ─æß╗òi sang `logger`. |
| `backend/md_parser.py` | 522 | `RAW_PRINT_CALL` | Sß╗¡ dß╗Ñng lß╗çnh `print()` trß╗▒c tiß║┐p. H├úy chuyß╗ân ─æß╗òi sang `logger`. |
| `backend/md_parser.py` | 549 | `RAW_PRINT_CALL` | Sß╗¡ dß╗Ñng lß╗çnh `print()` trß╗▒c tiß║┐p. H├úy chuyß╗ân ─æß╗òi sang `logger`. |
| `backend/md_parser.py` | 581 | `RAW_PRINT_CALL` | Sß╗¡ dß╗Ñng lß╗çnh `print()` trß╗▒c tiß║┐p. H├úy chuyß╗ân ─æß╗òi sang `logger`. |
| `backend/md_parser.py` | 530 | `RAW_PRINT_CALL` | Sß╗¡ dß╗Ñng lß╗çnh `print()` trß╗▒c tiß║┐p. H├úy chuyß╗ân ─æß╗òi sang `logger`. |
| `backend/md_parser.py` | 537 | `RAW_PRINT_CALL` | Sß╗¡ dß╗Ñng lß╗çnh `print()` trß╗▒c tiß║┐p. H├úy chuyß╗ân ─æß╗òi sang `logger`. |
| `backend/md_parser.py` | 542 | `RAW_PRINT_CALL` | Sß╗¡ dß╗Ñng lß╗çnh `print()` trß╗▒c tiß║┐p. H├úy chuyß╗ân ─æß╗òi sang `logger`. |
| `backend/mermaid_renderer.py` | 16 | `DOCSTRING_MISSING` | Class `MermaidRenderer`: Thiß║┐u Docstring |
| `backend/mermaid_renderer.py` | 17 | `DOCSTRING_MISSING` | H├ám `__init__`: Thiß║┐u Docstring. |
| `backend/mermaid_renderer.py` | 156 | `TYPE_HINT_MISSING` | H├ám `cleanup` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `backend/mermaid_renderer.py` | 104 | `TYPE_HINT_MISSING` | H├ám `check_status` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `result`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `backend/mermaid_renderer.py` | 104 | `DOCSTRING_MISSING` | H├ám `check_status`: Thiß║┐u Docstring. |
| `backend/mermaid_renderer.py` | 120 | `TYPE_HINT_MISSING` | H├ám `get_size` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `result`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `backend/mermaid_renderer.py` | 120 | `DOCSTRING_MISSING` | H├ám `get_size`: Thiß║┐u Docstring. |
| `backend/mermaid_renderer.py` | 151 | `RAW_PRINT_CALL` | Sß╗¡ dß╗Ñng lß╗çnh `print()` trß╗▒c tiß║┐p. H├úy chuyß╗ân ─æß╗òi sang `logger`. |
| `backend/__init__.py` | 1 | `HEADER_MISSING` | Thiß║┐u Header Changelog chuß║⌐n dß╗▒ ├ín (Thiß║┐u: T├¬n file, Chß╗⌐c n─âng, Changelog). |
| `frontend/main_window.py` | 1 | `HEADER_MISSING` | Thiß║┐u Header Changelog chuß║⌐n dß╗▒ ├ín (Thiß║┐u: Chß╗⌐c n─âng). |
| `frontend/main_window.py` | 47 | `MULTIPLE_CLASSES_IN_FILE` | Tß╗çp tin chß╗⌐a 5 Class ß╗ƒ cß║Ñp module. Khuyß║┐n nghß╗ï t├ích mß╗ùi file chß╗ë chß╗⌐a 1 Class ch├¡nh. |
| `frontend/main_window.py` | 31 | `DOCSTRING_MISSING` | Class `MarkdownParserThread`: Thiß║┐u Docstring |
| `frontend/main_window.py` | 47 | `DOCSTRING_MISSING` | Class `LineNumberArea`: Thiß║┐u Docstring |
| `frontend/main_window.py` | 59 | `DOCSTRING_MISSING` | Class `CodeEditor`: Thiß║┐u Docstring |
| `frontend/main_window.py` | 170 | `DOCSTRING_MISSING` | Class `SearchResultPanel`: Thiß║┐u Docstring |
| `frontend/main_window.py` | 233 | `DOCSTRING_MISSING` | Class `MainWindow`: Thiß║┐u Docstring |
| `frontend/main_window.py` | 35 | `DOCSTRING_MISSING` | H├ám `__init__`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 40 | `TYPE_HINT_MISSING` | H├ám `run` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 40 | `DOCSTRING_MISSING` | H├ám `run`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 48 | `TYPE_HINT_MISSING` | H├ám `__init__` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `editor` (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 48 | `DOCSTRING_MISSING` | H├ám `__init__`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 52 | `TYPE_HINT_MISSING` | H├ám `sizeHint` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 52 | `DOCSTRING_MISSING` | H├ám `sizeHint`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 55 | `TYPE_HINT_MISSING` | H├ám `paintEvent` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `event`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 55 | `DOCSTRING_MISSING` | H├ám `paintEvent`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 60 | `TYPE_HINT_MISSING` | H├ám `__init__` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `parent` (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 60 | `DOCSTRING_MISSING` | H├ám `__init__`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 82 | `TYPE_HINT_MISSING` | H├ám `set_dark_mode` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 82 | `DOCSTRING_MISSING` | H├ám `set_dark_mode`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 90 | `TYPE_HINT_MISSING` | H├ám `set_search_term` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 90 | `DOCSTRING_MISSING` | H├ám `set_search_term`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 94 | `TYPE_HINT_MISSING` | H├ám `lineNumberAreaWidth` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 94 | `DOCSTRING_MISSING` | H├ám `lineNumberAreaWidth`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 103 | `TYPE_HINT_MISSING` | H├ám `updateLineNumberAreaWidth` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `_`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 103 | `DOCSTRING_MISSING` | H├ám `updateLineNumberAreaWidth`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 106 | `TYPE_HINT_MISSING` | H├ám `updateLineNumberArea` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `rect`, ─Éß╗æi sß╗æ `dy`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 106 | `DOCSTRING_MISSING` | H├ám `updateLineNumberArea`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 115 | `TYPE_HINT_MISSING` | H├ám `resizeEvent` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `event`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 115 | `DOCSTRING_MISSING` | H├ám `resizeEvent`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 120 | `TYPE_HINT_MISSING` | H├ám `lineNumberAreaPaintEvent` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `event`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 120 | `DOCSTRING_MISSING` | H├ám `lineNumberAreaPaintEvent`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 141 | `TYPE_HINT_MISSING` | H├ám `highlightCurrentLine` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 141 | `DOCSTRING_MISSING` | H├ám `highlightCurrentLine`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 174 | `TYPE_HINT_MISSING` | H├ám `__init__` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `parent` (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 174 | `DOCSTRING_MISSING` | H├ám `__init__`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 183 | `TYPE_HINT_MISSING` | H├ám `add_result` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `line_num`, ─Éß╗æi sß╗æ `text_snippet`, ─Éß╗æi sß╗æ `pos`, ─Éß╗æi sß╗æ `search_term`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 183 | `DOCSTRING_MISSING` | H├ám `add_result`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 210 | `TYPE_HINT_MISSING` | H├ám `set_dark_mode` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 210 | `DOCSTRING_MISSING` | H├ám `set_dark_mode`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 227 | `TYPE_HINT_MISSING` | H├ám `on_item_clicked` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `item`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 227 | `DOCSTRING_MISSING` | H├ám `on_item_clicked`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 234 | `DOCSTRING_MISSING` | H├ám `__init__`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 251 | `TYPE_HINT_MISSING` | H├ám `_init_ui` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 251 | `DOCSTRING_MISSING` | H├ám `_init_ui`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 358 | `TYPE_HINT_MISSING` | H├ám `on_toc_navigation` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `url`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 358 | `DOCSTRING_MISSING` | H├ám `on_toc_navigation`: Thiß║┐u phß║ºn m├┤ tß║ú ─æß╗æi sß╗æ 'Args:' trong Docstring. |
| `frontend/main_window.py` | 366 | `TYPE_HINT_MISSING` | H├ám `_init_toolbar` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 366 | `DOCSTRING_MISSING` | H├ám `_init_toolbar`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 400 | `TYPE_HINT_MISSING` | H├ám `apply_theme` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 400 | `DOCSTRING_MISSING` | H├ám `apply_theme`: Thiß║┐u phß║ºn m├┤ tß║ú ─æß╗æi sß╗æ 'Args:' trong Docstring. |
| `frontend/main_window.py` | 414 | `TYPE_HINT_MISSING` | H├ám `toggle_theme` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 418 | `TYPE_HINT_MISSING` | H├ám `toggle_orientation` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `checked`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 418 | `DOCSTRING_MISSING` | H├ám `toggle_orientation`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 422 | `TYPE_HINT_MISSING` | H├ám `load_settings` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 422 | `DOCSTRING_MISSING` | H├ám `load_settings`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 449 | `TYPE_HINT_MISSING` | H├ám `save_settings` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 449 | `DOCSTRING_MISSING` | H├ám `save_settings`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 460 | `TYPE_HINT_MISSING` | H├ám `open_file_dialog` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 460 | `DOCSTRING_MISSING` | H├ám `open_file_dialog`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 464 | `TYPE_HINT_MISSING` | H├ám `load_markdown` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `path`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 464 | `DOCSTRING_MISSING` | H├ám `load_markdown`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 484 | `TYPE_HINT_MISSING` | H├ám `refresh_file_list_ui` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 484 | `DOCSTRING_MISSING` | H├ám `refresh_file_list_ui`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 490 | `TYPE_HINT_MISSING` | H├ám `show_sidebar_context_menu` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `pos`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 490 | `DOCSTRING_MISSING` | H├ám `show_sidebar_context_menu`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 501 | `TYPE_HINT_MISSING` | H├ám `remove_selected_from_history` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `row`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 501 | `DOCSTRING_MISSING` | H├ám `remove_selected_from_history`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 510 | `TYPE_HINT_MISSING` | H├ám `on_file_item_clicked` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `item`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 510 | `DOCSTRING_MISSING` | H├ám `on_file_item_clicked`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 515 | `TYPE_HINT_MISSING` | H├ám `render_viewer` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 515 | `DOCSTRING_MISSING` | H├ám `render_viewer`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 522 | `TYPE_HINT_MISSING` | H├ám `show_search_panel` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 522 | `DOCSTRING_MISSING` | H├ám `show_search_panel`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 527 | `TYPE_HINT_MISSING` | H├ám `hide_search_panel` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 527 | `DOCSTRING_MISSING` | H├ám `hide_search_panel`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 532 | `TYPE_HINT_MISSING` | H├ám `on_search_text_changed` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `text`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 532 | `DOCSTRING_MISSING` | H├ám `on_search_text_changed`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 553 | `TYPE_HINT_MISSING` | H├ám `find_all_and_show` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 579 | `TYPE_HINT_MISSING` | H├ám `on_search_result_clicked` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `line_num`, ─Éß╗æi sß╗æ `pos`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 579 | `DOCSTRING_MISSING` | H├ám `on_search_result_clicked`: Thiß║┐u phß║ºn m├┤ tß║ú ─æß╗æi sß╗æ 'Args:' trong Docstring. |
| `frontend/main_window.py` | 595 | `TYPE_HINT_MISSING` | H├ám `do_search` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `backward`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 595 | `DOCSTRING_MISSING` | H├ám `do_search`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 619 | `TYPE_HINT_MISSING` | H├ám `on_parse_done` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `data`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 619 | `DOCSTRING_MISSING` | H├ám `on_parse_done`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 626 | `TYPE_HINT_MISSING` | H├ám `on_file_changed_externally` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `path`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 626 | `DOCSTRING_MISSING` | H├ám `on_file_changed_externally`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 629 | `TYPE_HINT_MISSING` | H├ám `save_current_file` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 629 | `DOCSTRING_MISSING` | H├ám `save_current_file`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 639 | `TYPE_HINT_MISSING` | H├ám `on_tab_changed` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `i`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 639 | `DOCSTRING_MISSING` | H├ám `on_tab_changed`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 647 | `TYPE_HINT_MISSING` | H├ám `export_pdf` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 647 | `DOCSTRING_MISSING` | H├ám `export_pdf`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 667 | `TYPE_HINT_MISSING` | H├ám `export_docx` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 667 | `DOCSTRING_MISSING` | H├ám `export_docx`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 674 | `TYPE_HINT_MISSING` | H├ám `_show_export_success_dialog` thiß║┐u Type Hints: Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 674 | `DOCSTRING_MISSING` | H├ám `_show_export_success_dialog`: Thiß║┐u phß║ºn m├┤ tß║ú ─æß╗æi sß╗æ 'Args:' trong Docstring. |
| `frontend/main_window.py` | 693 | `TYPE_HINT_MISSING` | H├ám `on_error` thiß║┐u Type Hints: ─Éß╗æi sß╗æ `e`, Kiß╗âu trß║ú vß╗ü (Returns) (V├╣ng UI/Tools - Warning). |
| `frontend/main_window.py` | 693 | `DOCSTRING_MISSING` | H├ám `on_error`: Thiß║┐u Docstring. |
| `frontend/main_window.py` | 653 | `DOCSTRING_MISSING` | H├ám `on_pdf_finished`: Thiß║┐u Docstring. |
| `frontend/__init__.py` | 1 | `HEADER_MISSING` | Thiß║┐u Header Changelog chuß║⌐n dß╗▒ ├ín (Thiß║┐u: T├¬n file, Chß╗⌐c n─âng, Changelog). |

================================================================================

