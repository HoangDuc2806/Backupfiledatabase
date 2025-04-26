Backup Database tự động mỗi ngày
📌 Mô tả
Dự án Python này thực hiện:

Tự động sao lưu các file database .sql và .sqlite3 từ thư mục database/ sang thư mục backup/ mỗi ngày lúc 00:00 (nửa đêm).
Gửi email thông báo kết quả backup (thành công hoặc thất bại) cho người quản lý.
Cấu hình thông tin email (gửi, nhận) trong file .env để bảo mật.
🛠️ Công nghệ sử dụng
Python 3
Các thư viện:
smtplib
schedule
dotenv
email.mime
shutil
os
📂 Cấu trúc thư mục
├── backup/ # Folder lưu các file backup ├── database/ # Folder chứa các file database gốc (.sql, .sqlite3) ├── backup_db.py # File script chính thực hiện backup và gửi email ├── .env # File cấu hình biến môi trường (KHÔNG PUSH LÊN GITHUB) ├── README.md # File mô tả dự án ├── requirements.txt # Danh sách các thư viện cần cài

⚙️ Hướng dẫn chạy
Tạo file .env với nội dung:
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=receiver_email@gmail.com

2. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

3. Chạy chương trình backup
python backup_db.py
