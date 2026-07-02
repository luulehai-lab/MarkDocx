---
description: Tự động đồng bộ và xuất các cuộc hội thoại mới của Antigravity IDE ra định dạng Markdown sạch sẽ (.md) để lưu trữ và tra cứu vĩnh viễn.
---

# 🚀 ĐỒNG BỘ & XUẤT LỊCH SỬ HỘI THOẠI (EXPORT CONVERSATIONS)

> **Mục đích:** Workflow này quét toàn bộ các cuộc hội thoại cũ và mới trên máy của Anh Lưu, tự động phát hiện các cuộc trò chuyện mới hoặc cuộc trò chuyện vừa phát sinh thêm tin nhắn mới, và xuất chúng ra định dạng Markdown cực kỳ sạch sẽ và chỉn chu (lọc bỏ metadata XML rác của IDE).

---

## 🛠️ Quy trình thực hiện tự động

Hệ thống sẽ chạy một script Python thông minh (`tools/maintenance/export_conversations.py`) để thực hiện các công việc sau:
1. Quét song song cả 2 thư mục lịch sử cục bộ: `antigravity` (cũ) và `antigravity-ide` (mới).
2. So khớp kích thước và thời gian sửa đổi cuối cùng (Last Modified Time) của từng file log với tệp tin `docs/history_conversations/.export_registry.json`.
3. Chỉ trích xuất và ghi đè những file có sự thay đổi (Incremental Sync) giúp tiết kiệm tài nguyên ổ cứng.
4. Trích xuất chính xác yêu cầu cốt lõi của Anh Lưu, loại bỏ 100% metadata XML rác của IDE.
5. Tạo tệp tin Markdown (.md) chất lượng cao tại thư mục: `docs/history_conversations/`.

---

## 💻 Thực thi lệnh đồng bộ

// turbo
```powershell
python "tools/maintenance/export_conversations.py"
```

---

## 💡 Lưu ý sử dụng
* Khi Anh Lưu muốn em đọc lại cuộc trò chuyện cũ để làm tiếp việc, anh chỉ cần chỉ định tên file Markdown tương ứng trong thư mục `docs/history_conversations/` (ví dụ: *"Đọc file [2026-05-19_..._da09febb.md](file:///d:/CloudStation/CODE/AI_ASSISTANT/ZZZ.DANG%20TEST/docs/history_conversations/2026-05-19_195312_DCloudStationCODEPYTHON_APP33_family_photo_ai_2412_da09febb.md) rồi tiếp tục giúp anh..."*).
* Điều này giúp em nắm bắt 100% bối cảnh một cách nhanh nhất, sạch nhất và chính xác nhất!
