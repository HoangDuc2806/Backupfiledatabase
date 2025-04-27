import os
import shutil
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import schedule
import time
from datetime import datetime

# Tải các biến môi trường từ .env
load_dotenv()
sender_email = os.getenv('EMAIL_SENDER')
sender_password = os.getenv('EMAIL_PASSWORD')
receiver_email = os.getenv('EMAIL_RECEIVER')

database_dir = './database'
backup_dir = './backup'

# Gửi email thông báo
def send_email(subject, message):
    email_msg = MIMEText(message)
    email_msg['From'] = sender_email
    email_msg['To'] = receiver_email
    email_msg['Subject'] = subject
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(email_msg)
        print(" Đã gửi email.")
    except Exception as e:
        print(f" Gửi email lỗi: {e}")

# Sao lưu database
def backup_database():
    try:
        os.makedirs(backup_dir, exist_ok=True)
        backed_up_files = []

        for file in os.listdir(database_dir):
            if file.endswith(('.sql', '.sqlite3')):
                src = os.path.join(database_dir, file)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                dst = os.path.join(backup_dir, f"{os.path.splitext(file)[0]}_{timestamp}{os.path.splitext(file)[1]}")
                shutil.copy2(src, dst)
                backed_up_files.append(dst)

        if backed_up_files:
            send_email(" Backup thành công", "Các file đã sao lưu:\n" + "\n".join(backed_up_files))
        else:
            send_email(" Không có file để sao lưu", "Không tìm thấy file .sql hoặc .sqlite3.")
    except Exception as e:
        send_email(" Backup thất bại", f"Lỗi: {str(e)}")

# Lên lịch sao lưu vào mỗi sáng lúc 00:00
schedule.every().day.at("00:00").do(backup_database)

print(" Đang chạy lịch backup...")
while True:
    schedule.run_pending()
