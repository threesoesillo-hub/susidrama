# Configuration file untuk Susi Drama Bot
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8582643985:AAHkBsWy7KnVwFYME1bfa2x2p0r0BliEiJY')

# Firebase Configuration
FIREBASE_CONFIG = {
    "type": "service_account",
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n') if os.getenv('FIREBASE_PRIVATE_KEY') else "",
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv('FIREBASE_CERT_URL')
}

# Pakasir Payment Gateway (uses api_key + project slug)
PAKASIR_API_KEY = os.getenv('PAKASIR_API_KEY', 'YOUR_PAKASIR_API_KEY')
PAKASIR_PROJECT = os.getenv('PAKASIR_PROJECT', 'your-project-slug')
PAKASIR_API_URL = 'https://app.pakasir.com/api'

# Channel Settings
CHANNEL_ID = os.getenv('CHANNEL_ID', '-1003410391228')  # Channel untuk posting drama
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', '@susidrama')

# Admin Settings
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '').split(','))) if os.getenv('ADMIN_IDS') else []

# Database Settings
FIREBASE_DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL', 'https://your-project.firebaseio.com')

# VIP Packages (dalam Rupiah)
VIP_PACKAGES = {
    '1_hari': {'days': 1, 'price': 2000, 'label': '⭐ VIP 1 hari — Rp2.000'},
    '3_hari': {'days': 3, 'price': 5500, 'label': '⭐ VIP 3 hari — Rp5.500'},
    '7_hari': {'days': 7, 'price': 10900, 'label': '⭐ VIP 7 hari — Rp10.900'},
    '15_hari': {'days': 15, 'price': 20900, 'label': '⭐ VIP 15 hari — Rp20.900'},
    '30_hari': {'days': 30, 'price': 34900, 'label': '⭐ VIP 30 hari — Rp34.900'},
    '90_hari': {'days': 90, 'price': 99000, 'label': '⭐ VIP 90 hari — Rp99.000'},
}

# Referral Commission (dalam persen)
REFERRAL_COMMISSION = {
    'L1': 20,  # Level 1: 20%
    'L2': 3,   # Level 2: 3%
    'L3': 2,   # Level 3: 2%
}

# Minimum withdrawal
MIN_WITHDRAWAL = 10000  # Minimal penarikan Rp10.000

# Drama Channel Link untuk redirect
DRAMA_CHANNEL_LINK = os.getenv('DRAMA_CHANNEL_LINK', 'https://t.me/susidrama')

print("✅ Configuration loaded successfully")
