import os
import shutil
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import schedule
import time
from datetime import datetime

# Tải các biến môi trường từ tệp .env
load_dotenv()
email_gui = os.getenv('EMAIL_SENDER')
mat_khau_gui = os.getenv('EMAIL_PASSWORD')
email_nhan = os.getenv('EMAIL_RECEIVER')

thu_muc_csdld = './database'
thu_muc_sao_luu = './backup'

# Hàm gửi email thông báo
def gui_email(tieu_de, noi_dung):
    thong_diep = MIMEText(noi_dung)
    thong_diep['From'] = email_gui
    thong_diep['To'] = email_nhan
    thong_diep['Subject'] = tieu_de
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_gui, mat_khau_gui)
            server.send_message(thong_diep)
        print("✅ Đã gửi email thành công.")
    except Exception as loi:
        print(f"❌ Gửi email thất bại: {loi}")

# Hàm sao lưu cơ sở dữ liệu
def sao_luu_csdld():
    try:
        os.makedirs(thu_muc_sao_luu, exist_ok=True)
        danh_sach_file_sao_luu = []

        for tep in os.listdir(thu_muc_csdld):
            if tep.endswith(('.sql', '.sqlite3')):
                duong_dan_goc = os.path.join(thu_muc_csdld, tep)
                thoi_gian = datetime.now().strftime('%Y%m%d_%H%M%S')
                duong_dan_dich = os.path.join(thu_muc_sao_luu, f"{os.path.splitext(tep)[0]}_{thoi_gian}{os.path.splitext(tep)[1]}")
                shutil.copy2(duong_dan_goc, duong_dan_dich)
                danh_sach_file_sao_luu.append(duong_dan_dich)

        if danh_sach_file_sao_luu:
            gui_email("✅ Sao lưu thành công", "Các tệp đã sao lưu:\n" + "\n".join(danh_sach_file_sao_luu))
        else:
            gui_email("⚠️ Không có tệp để sao lưu", "Không tìm thấy tệp .sql hoặc .sqlite3 trong thư mục database.")
    except Exception as loi:
        gui_email("❌ Sao lưu thất bại", f"Lỗi chi tiết: {str(loi)}")

# Lên lịch sao lưu hàng ngày vào 00:00
schedule.every().day.at("00:00").do(sao_luu_csdld)

print("🕛 Đang chạy lịch sao lưu tự động...")

while True:
    schedule.run_pending()
    time.sleep(1)  # Thêm sleep nhẹ để tránh CPU load cao
