import os
import shutil
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import schedule
import time
from datetime import datetime

# Load biến môi trường từ file .env
load_dotenv()
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')

DATABASE_FOLDER = './database'
BACKUP_FOLDER = './backup'

def send_email(subject, message):
    try:
        email = MIMEText(message, 'plain')
        email['From'] = EMAIL_SENDER
        email['To'] = EMAIL_RECEIVER
        email['Subject'] = subject

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(email)

        print("✅ Đã gửi email thông báo.")
    except Exception as e:
        print(f"❌ Lỗi gửi email: {e}")

def backup_database():
    try:
        os.makedirs(BACKUP_FOLDER, exist_ok=True)

        backup_files = []
        for file in os.listdir(DATABASE_FOLDER):
            if file.endswith(('.sql', '.sqlite3')):
                src = os.path.join(DATABASE_FOLDER, file)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                dst = os.path.join(BACKUP_FOLDER, f"{os.path.splitext(file)[0]}_{timestamp}{os.path.splitext(file)[1]}")
                shutil.copy2(src, dst)
                backup_files.append(dst)

        if backup_files:
            send_email("✅ Backup thành công", "Các file đã backup:\n" + "\n".join(backup_files))
        else:
            send_email("⚠️ Không có file để backup", "Không tìm thấy file .sql hoặc .sqlite3 trong thư mục database.")

    except Exception as e:
        send_email("❌ Backup thất bại", f"Lỗi: {str(e)}")

# Đặt lịch chạy mỗi ngày lúc 00:00
schedule.every().day.at("00:00").do(backup_database)

print("🛠️ Đang chạy lịch backup database...")

while True:
    schedule.run_pending()
    time.sleep(1)
