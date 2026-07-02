E701 Multiple statements on one line (colon)
   --> backend\md_parser.py:574:20
    |
572 |         if os.path.exists(temp_img_dir):
573 |             for f in os.listdir(temp_img_dir):
574 |                 try: os.remove(os.path.join(temp_img_dir, f))
    |                    ^
575 |                 except: pass
576 |             try: os.rmdir(temp_img_dir)
    |

E722 Do not use bare `except`
   --> backend\md_parser.py:575:17
    |
573 |             for f in os.listdir(temp_img_dir):
574 |                 try: os.remove(os.path.join(temp_img_dir, f))
575 |                 except: pass
    |                 ^^^^^^
576 |             try: os.rmdir(temp_img_dir)
577 |             except: pass
    |

E701 Multiple statements on one line (colon)
   --> backend\md_parser.py:575:23
    |
573 |             for f in os.listdir(temp_img_dir):
574 |                 try: os.remove(os.path.join(temp_img_dir, f))
575 |                 except: pass
    |                       ^
576 |             try: os.rmdir(temp_img_dir)
577 |             except: pass
    |

E701 Multiple statements on one line (colon)
   --> backend\md_parser.py:576:16
    |
574 |                 try: os.remove(os.path.join(temp_img_dir, f))
575 |                 except: pass
576 |             try: os.rmdir(temp_img_dir)
    |                ^
577 |             except: pass
    |

E722 Do not use bare `except`
   --> backend\md_parser.py:577:13
    |
575 |                 except: pass
576 |             try: os.rmdir(temp_img_dir)
577 |             except: pass
    |             ^^^^^^
578 |             
579 |         return True
    |

E701 Multiple statements on one line (colon)
   --> backend\md_parser.py:577:19
    |
575 |                 except: pass
576 |             try: os.rmdir(temp_img_dir)
577 |             except: pass
    |                   ^
578 |             
579 |         return True
    |

F401 [*] `time` imported but unused
  --> backend\mermaid_renderer.py:8:8
   |
 7 | import os
 8 | import time
   |        ^^^^
 9 | import uuid
10 | from PyQt6.QtWidgets import QApplication
   |
help: Remove unused import: `time`

F401 [*] `PyQt6.QtWidgets.QApplication` imported but unused
  --> backend\mermaid_renderer.py:10:29
   |
 8 | import time
 9 | import uuid
10 | from PyQt6.QtWidgets import QApplication
   |                             ^^^^^^^^^^^^
11 | from PyQt6.QtWebEngineWidgets import QWebEngineView
12 | from PyQt6.QtWebEngineCore import QWebEngineSettings
   |
help: Remove unused import: `PyQt6.QtWidgets.QApplication`

F401 [*] `PyQt6.QtCore.QSize` imported but unused
  --> backend\mermaid_renderer.py:13:52
   |
11 | from PyQt6.QtWebEngineWidgets import QWebEngineView
12 | from PyQt6.QtWebEngineCore import QWebEngineSettings
13 | from PyQt6.QtCore import QUrl, QEventLoop, QTimer, QSize
   |                                                    ^^^^^
14 | from config import MERMAID_JS_PATH, BASE_DIR
   |
help: Remove unused import: `PyQt6.QtCore.QSize`

E701 Multiple statements on one line (colon)
   --> backend\mermaid_renderer.py:122:22
    |
120 |         def get_size(result):
121 |             nonlocal rect
122 |             if result: rect = result
    |                      ^
123 |             size_loop.quit()
    |

E701 Multiple statements on one line (colon)
   --> backend\mermaid_renderer.py:160:20
    |
158 |         if os.path.exists(self.temp_dir):
159 |             for f in os.listdir(self.temp_dir):
160 |                 try: os.remove(os.path.join(self.temp_dir, f))
    |                    ^
161 |                 except: pass
    |

E722 Do not use bare `except`
   --> backend\mermaid_renderer.py:161:17
    |
159 |             for f in os.listdir(self.temp_dir):
160 |                 try: os.remove(os.path.join(self.temp_dir, f))
161 |                 except: pass
    |                 ^^^^^^
    |

E701 Multiple statements on one line (colon)
   --> backend\mermaid_renderer.py:161:23
    |
159 |             for f in os.listdir(self.temp_dir):
160 |                 try: os.remove(os.path.join(self.temp_dir, f))
161 |                 except: pass
    |                       ^
    |

F401 [*] `PyQt6.QtGui.QIcon` imported but unused
  --> frontend\main_window.py:15:34
   |
13 |     QDockWidget, QListWidgetItem
14 | )
15 | from PyQt6.QtGui import QAction, QIcon, QFont, QTextCursor, QPainter, QColor, QTextFormat, QShortcut, QKeySequence, QTextDocument
   |                                  ^^^^^
16 | from PyQt6.QtCore import QThread, pyqtSignal, QFileSystemWatcher, QUrl, Qt, QSize, QRect, QByteArray
17 | from PyQt6.QtWebEngineWidgets import QWebEngineView
   |
help: Remove unused import

F401 [*] `PyQt6.QtGui.QTextCursor` imported but unused
  --> frontend\main_window.py:15:48
   |
13 |     QDockWidget, QListWidgetItem
14 | )
15 | from PyQt6.QtGui import QAction, QIcon, QFont, QTextCursor, QPainter, QColor, QTextFormat, QShortcut, QKeySequence, QTextDocument
   |                                                ^^^^^^^^^^^
16 | from PyQt6.QtCore import QThread, pyqtSignal, QFileSystemWatcher, QUrl, Qt, QSize, QRect, QByteArray
17 | from PyQt6.QtWebEngineWidgets import QWebEngineView
   |
help: Remove unused import

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:162:32
    |
160 |                 highlight_color = QColor("#ffd33d") if self.is_dark else QColor("#fff200")
161 |                 selection.format.setBackground(highlight_color)
162 |                 if self.is_dark: selection.format.setForeground(QColor("#000000"))
    |                                ^
163 |                 selection.cursor = cursor
164 |                 extraSelections.append(selection)
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:446:53
    |
445 |                     last = settings.get("last_file")
446 |                     if last and os.path.exists(last): self.load_markdown(last)
    |                                                     ^
447 |             except: pass
    |

E722 Do not use bare `except`
   --> frontend\main_window.py:447:13
    |
445 |                     last = settings.get("last_file")
446 |                     if last and os.path.exists(last): self.load_markdown(last)
447 |             except: pass
    |             ^^^^^^
448 |
449 |     def save_settings(self):
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:447:19
    |
445 |                     last = settings.get("last_file")
446 |                     if last and os.path.exists(last): self.load_markdown(last)
447 |             except: pass
    |                   ^
448 |
449 |     def save_settings(self):
    |

E722 Do not use bare `except`
   --> frontend\main_window.py:458:9
    |
456 |                     "splitter_state": self.main_splitter.saveState().toHex().data().decode()
457 |                 }, f, ensure_ascii=False, indent=4)
458 |         except: pass
    |         ^^^^^^
459 |
460 |     def open_file_dialog(self):
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:458:15
    |
456 |                     "splitter_state": self.main_splitter.saveState().toHex().data().decode()
457 |                 }, f, ensure_ascii=False, indent=4)
458 |         except: pass
    |               ^
459 |
460 |     def open_file_dialog(self):
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:462:16
    |
460 |     def open_file_dialog(self):
461 |         path, _ = QFileDialog.getOpenFileName(self, "Mß╗ƒ file", "", "Markdown (*.md)")
462 |         if path: self.load_markdown(path)
    |                ^
463 |
464 |     def load_markdown(self, path):
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:465:48
    |
464 |     def load_markdown(self, path):
465 |         if not path or not os.path.exists(path): return
    |                                                ^
466 |         if self.current_file: self.watcher.removePath(self.current_file)
467 |         self.current_file = path
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:466:29
    |
464 |     def load_markdown(self, path):
465 |         if not path or not os.path.exists(path): return
466 |         if self.current_file: self.watcher.removePath(self.current_file)
    |                             ^
467 |         self.current_file = path
468 |         self.watcher.addPath(path)
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:470:38
    |
468 |         self.watcher.addPath(path)
469 |         
470 |         if path in self.history_files: self.history_files.remove(path)
    |                                      ^
471 |         self.history_files.insert(0, path)
472 |         self.history_files = self.history_files[:20]
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:486:36
    |
484 |     def refresh_file_list_ui(self):
485 |         self.sidebar.clear()
486 |         for f in self.history_files: self.sidebar.addItem(os.path.basename(f))
    |                                    ^
487 |         if self.current_file in self.history_files:
488 |             self.sidebar.setCurrentRow(self.history_files.index(self.current_file))
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:492:20
    |
490 |     def show_sidebar_context_menu(self, pos):
491 |         item = self.sidebar.itemAt(pos)
492 |         if not item: return
    |                    ^
493 |         
494 |         row = self.sidebar.row(item)
    |

F841 Local variable `f_path` is assigned to but never used
   --> frontend\main_window.py:503:13
    |
501 |     def remove_selected_from_history(self, row):
502 |         if 0 <= row < len(self.history_files):
503 |             f_path = self.history_files.pop(row)
    |             ^^^^^^
504 |             # Nß║┐u x├│a ch├¡nh file ─æang mß╗ƒ -> clear hoß║╖c giß╗» nguy├¬n? 
505 |             # Giß╗» nguy├¬n viewer nh╞░ng file kh├┤ng c├▓n trong history nß╗»a
    |
help: Remove assignment to unused variable `f_path`

F541 [*] f-string without any placeholders
   --> frontend\main_window.py:508:41
    |
506 |             self.refresh_file_list_ui()
507 |             self.save_settings()
508 |             self.status_bar.showMessage(f"─É├ú gß╗í khß╗Åi lß╗ïch sß╗¡.", 2000)
    |                                         ^^^^^^^^^^^^^^^^^^^^^^
509 |
510 |     def on_file_item_clicked(self, item):
    |
help: Remove extraneous `f` prefix

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:516:33
    |
515 |     def render_viewer(self):
516 |         if not self.current_file: return
    |                                 ^
517 |         self.parser_thread = MarkdownParserThread(self.current_file, self.is_dark)
518 |         self.parser_thread.parse_done.connect(self.on_parse_done)
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:556:20
    |
554 |         """Qu├⌐t to├án bß╗Ö v├á hiß╗çn bß║úng kß║┐t quß║ú giß╗æng Notepad++."""
555 |         text = self.search_input.text()
556 |         if not text: return
    |                    ^
557 |         
558 |         self.results_panel.clear()
    |

F841 Local variable `found` is assigned to but never used
   --> frontend\main_window.py:603:13
    |
601 |         if self.tabs.currentIndex() == 0: # T├¼m trong Editor
602 |             options = QTextDocument.FindFlag.FindBackward if backward else QTextDocument.FindFlag(0)
603 |             found = self.editor.find(text, options)
    |             ^^^^^
604 |             # ─Éß║┐m sß╗æ l╞░ß╗úng kß║┐t quß║ú (b├ío c├ío)
605 |             count = 0
    |
help: Remove assignment to unused variable `found`

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:627:37
    |
626 |     def on_file_changed_externally(self, path):
627 |         if path == self.current_file: self.load_markdown(path)
    |                                     ^
628 |
629 |     def save_current_file(self):
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:630:33
    |
629 |     def save_current_file(self):
630 |         if not self.current_file: return
    |                                 ^
631 |         try:
632 |             self.watcher.removePath(self.current_file)
    |

E722 Do not use bare `except`
   --> frontend\main_window.py:637:9
    |
635 |             self.watcher.addPath(self.current_file)
636 |             self.render_viewer()
637 |         except: pass
    |         ^^^^^^
638 |
639 |     def on_tab_changed(self, i):
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:637:15
    |
635 |             self.watcher.addPath(self.current_file)
636 |             self.render_viewer()
637 |         except: pass
    |               ^
638 |
639 |     def on_tab_changed(self, i):
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:640:18
    |
639 |     def on_tab_changed(self, i):
640 |         if i == 1: self.render_viewer()
    |                  ^
641 |         
642 |         # ─Éß╗ông bß╗Ö t├¼m kiß║┐m khi chuyß╗ân tab
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:648:33
    |
647 |     def export_pdf(self):
648 |         if not self.current_file: return
    |                                 ^
649 |         path, _ = QFileDialog.getSaveFileName(self, "L╞░u PDF", "", "PDF (*.pdf)")
650 |         if path:
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:668:33
    |
667 |     def export_docx(self):
668 |         if not self.current_file: return
    |                                 ^
669 |         path, _ = QFileDialog.getSaveFileName(self, "L╞░u DOCX", "", "Word (*.docx)")
670 |         if path:
    |

E402 Module level import not at top of file
  --> temp_render\test_viewer_latex.py:20:1
   |
18 |     sys.exit(1)
19 |
20 | from PyQt6.QtWidgets import QApplication
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
21 | # Khß╗ƒi tß║ío QApplication cho QWebEngineView trong MermaidRenderer
22 | app = QApplication([])
   |

Found 40 errors.
[*] 6 fixable with the `--fix` option (2 hidden fixes can be enabled with the `--unsafe-fixes` option).
