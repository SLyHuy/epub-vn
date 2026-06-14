# EPUB Fixer - Công cụ sửa lỗi khoảng cách dấu câu tiếng Việt

Đây là công cụ dòng lệnh (CLI) bằng Python giúp tự động sửa lỗi thiếu khoảng trắng sau các dấu câu (như `. , : ; ! ? " ) } ]`) trong file EPUB tiếng Việt. 

Công cụ đã được thiết kế tối ưu để không làm hỏng cấu trúc HTML, bỏ qua các trường hợp ngoại lệ như:
- Tên miền, URL, Email (ví dụ: `google.com`, `user@email.com`)
- Số thập phân, cấu trúc phân cấp (ví dụ: `3.14`, `1.2.3`, `1,000`)
- Các từ viết tắt phổ biến (ví dụ: `Tp.HCM`, `PGS.TS.`, `ThS.`, `U.S.A`)

## Cài đặt thư viện yêu cầu

Trước khi sử dụng, bạn cần đảm bảo máy tính đã cài đặt Python. Sau đó, mở Terminal (hoặc Command Prompt) và chạy lệnh sau để cài các thư viện cần thiết:

```bash
pip install beautifulsoup4 lxml
```

## Hướng dẫn sử dụng

Chỉ cần copy và paste dòng lệnh sau vào Terminal, thay thế đường dẫn file tương ứng của bạn.

**Cú pháp:**
```bash
python epub_fixer.py <đường_dẫn_file_gốc> <đường_dẫn_file_mới>
```

**Ví dụ thực tế:**
```bash
python epub_fixer.py input.epub output.epub
```

*Lưu ý: Nếu tên file của bạn có khoảng trắng, hãy đặt tên file trong dấu ngoặc kép (ví dụ: `"sach cua toi.epub"`).*

## Cách công cụ hoạt động
1. Tool sẽ giải nén file EPUB gốc.
2. Trích xuất file `mimetype` và đảm bảo nó không bị nén (chế độ Store).
3. Tìm tất cả các file mã nguồn giao diện (`.html`, `.xhtml`, `.htm`) và phân tích cấu trúc DOM bằng `BeautifulSoup`.
4. Tìm đến các khối Text (bỏ qua thẻ Tag) và dùng logic thay thế thông minh (Regex) để thêm một khoảng trắng sau các dấu câu nếu sau nó là chữ/số.
5. Đóng gói lại mọi thứ thành file EPUB hoàn chỉnh.
