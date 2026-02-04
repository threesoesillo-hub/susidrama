# Script untuk mendapatkan Telegram File ID dari Video
# Run: python get_file_id.py

from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

def get_bot():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN tidak ditemukan di .env")
        return None
    return Bot(token)

def get_file_id():
    """
    Untuk menggunakan script ini:
    1. Ambil video yang ingin di-upload
    2. Forward ke bot kamu
    3. Bot akan menampilkan file_id
    4. Copy file_id ke video_data.py
    """
    print("""
    ╔════════════════════════════════════════════════╗
    ║    Get Telegram Video File ID                 ║
    ║                                                ║
    ║  Cara menggunakan:                             ║
    ║  1. Kirim video ke bot kamu                    ║
    ║  2. Forward ke script ini                      ║
    ║  3. Ambil file_id yang muncul                  ║
    ║  4. Paste ke video_data.py                     ║
    ╚════════════════════════════════════════════════╝
    
    Contoh format file_id:
    BAACAgIAAxkBAAIBZ2Fg5rJ_2U...
    """)

if __name__ == '__main__':
    get_file_id()
    print("\n💡 Untuk mendapatkan file_id:")
    print("1. Forward video dari chat ke bot")
    print("2. Lihat message ID")
    print("3. Gunakan get_file() API untuk ambil file_id")
    print("\nAlternative: Buka debug console dan forward video")
