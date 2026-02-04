# 🎬 Susi Drama Bot - Complete Documentation

**Telegram Bot untuk streaming drama dengan sistem VIP, referral, dan payment gateway Pakasir**

## ✨ Fitur Utama

### 1. 🔍 CARI DRAMA
- Search drama berdasarkan judul
- Hasil real-time
- Tampil jumlah episode

### 2. 📺 LIST DRAMA
- Link ke channel publik
- Daftar semua drama tersedia

### 3. 💎 BELI VIP
**Paket:**
- 1 hari: Rp2.000
- 3 hari: Rp5.500
- 7 hari: Rp10.900
- 15 hari: Rp20.900
- 30 hari: Rp34.900
- 90 hari: Rp99.000

**Keuntungan:**
✅ Akses unlimited  
✅ HD quality  
✅ Bebas iklan  

### 4. 💰 DAPATKAN UANG
**Referral System 3 Level:**
- L1: 20%
- L2: 3%
- L3: 2%

### 5. 👤 PROFIL
- Status VIP
- User info
- Balance & komisi
- Network referral

### 6. 🎥 VIDEO STREAMING
- Part 1: Gratis
- Part 2+: VIP only
- Protected (no record/forward)

### 7. 💳 PAYMENT GATEWAY
- QRIS otomatis
- Multi-method (Bank, E-Wallet)
- Auto-confirmation
- VIP instant active

## 💻 Requirements

**System:**
- Python 3.8+
- 2GB RAM
- 500MB storage
- Internet connection

**Accounts:**
1. Telegram Bot Token (@BotFather)
2. Firebase Project
3. Pakasir Account
4. VPS (optional - Hostinger)

## 🚀 Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/susidrama.git
cd susidrama
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Environment
```bash
cp .env.example .env
# Edit .env dengan credentials kamu
```

### Step 4: Configure Services

**Firebase:**
1. https://console.firebase.google.com
2. Create project → Realtime Database
3. Download service account JSON
4. Copy ke `.env`

**Pakasir:**
1. https://pakasir.id
2. Daftar & login
3. Dapatkan API Key & Secret
4. Copy ke `.env`

**Telegram:**
1. Chat @BotFather
2. `/newbot` → ikuti instruksi
3. Copy token ke `.env`

### Step 5: Run Bot
```bash
python susidrama.py
```

Success: `✅ Bot is running...`

## ⚙️ Configuration

### File: `config.py`

Edit untuk customize:

```python
# VIP Packages
VIP_PACKAGES = {
    '1_hari': {'days': 1, 'price': 2000},
    '3_hari': {'days': 3, 'price': 5500},
    # Add more...
}

# Referral Commission
REFERRAL_COMMISSION = {
    'L1': 20,  # 20%
    'L2': 3,   # 3%
    'L3': 2,   # 2%
}

# Minimal Withdrawal
MIN_WITHDRAWAL = 10000  # Rp10.000
```

## 📁 Project Structure

```
susidrama/
├── susidrama.py          # Main bot script
├── config.py             # Configuration
├── video_data.py         # Drama/video database
├── firebase_db.py        # Firebase integration
├── payment.py            # Pakasir payment
├── content.py            # Content manager
├── requirements.txt      # Dependencies
├── .env.example          # Config template
└── README.md             # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `susidrama.py` | Bot main dengan handlers |
| `config.py` | Semua setting & konfigurasi |
| `video_data.py` | Database drama (mudah di-edit) |
| `firebase_db.py` | Firebase functions |
| `payment.py` | Pakasir integration |
| `content.py` | Content management |

## 🎬 Add Drama

### Edit `video_data.py`

```python
DRAMAS = {
    'drama_XXX': {
        'id': 'drama_XXX',
        'title': 'JUDUL DRAMA',
        'thumbnail': 'https://url.jpg',
        'description': 'Description',
        'parts': {
            'part_1': {
                'episode': 1,
                'video_id': 'FILE_ID_TELEGRAM',
                'is_free': True,
                'duration': '45:30'
            },
            'part_2': {
                'episode': 2,
                'video_id': 'FILE_ID_TELEGRAM',
                'is_free': False,
                'requires_vip': True,
                'duration': '48:15'
            }
        }
    }
}
```

### Get Telegram File ID

**Option 1: Forward video**
- Forward video ke bot
- Ambil file_id dari response
- Paste ke video_data.py

**Option 2: Debug script**
```python
from telegram import Bot
bot = Bot('YOUR_TOKEN')
# Upload video, ambil file_id
```

## 🌐 VPS Deployment (Hostinger)

### 1. SSH Connect
```bash
ssh user@your_vps_ip
```

### 2. Install System
```bash
sudo apt update
sudo apt install python3 python3-pip git
```

### 3. Setup Project
```bash
git clone https://github.com/yourusername/susidrama.git
cd susidrama
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure
```bash
nano .env
# Paste semua credentials kamu
```

### 5. Test Bot
```bash
python susidrama.py
```

### 6. Setup Auto-Start (Systemd)

```bash
sudo nano /etc/systemd/system/susidrama.service
```

Paste:
```ini
[Unit]
Description=Susi Drama Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/home/your_user/susidrama
Environment="PATH=/home/your_user/susidrama/venv/bin"
ExecStart=/home/your_user/susidrama/venv/bin/python /home/your_user/susidrama/susidrama.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable susidrama
sudo systemctl start susidrama
sudo systemctl status susidrama
```

### 7. Monitor Bot
```bash
sudo journalctl -u susidrama -f  # View logs
sudo systemctl status susidrama  # Check status
```

## 📊 Firebase Database Structure

```
users/
  ├── {user_id}/
  │   ├── user_id
  │   ├── first_name
  │   ├── username
  │   ├── joined_date
  │   ├── vip_status
  │   ├── vip_expiry
  │   ├── balance
  │   ├── referral_code
  │   ├── referred_by
  │   └── downlines

payments/
  ├── {payment_id}/
  │   ├── user_id
  │   ├── amount
  │   ├── package_id
  │   ├── status
  │   └── created_at

transactions/
  └── {user_id}/
      └── {trans_id}/
          ├── type
          ├── amount
          ├── reason
          └── timestamp
```

## 🔧 Troubleshooting

### Bot tidak respond
```bash
# Check token
nano .env
# Verify TELEGRAM_BOT_TOKEN

# Test run
python susidrama.py
```

### Error: "No module named 'telegram'"
```bash
pip install python-telegram-bot==13.15
```

### Firebase connection error
- Verify `.env` credentials
- Check newlines: `\n` → correct
- Test: `python -c "from firebase_db import get_firebase_db; print('OK')"`

### Payment tidak terdeteksi
- Check Pakasir API key
- Verify di Pakasir dashboard
- Check Firebase payment record
- Test callback

### Video tidak bisa diplay
- Verify file_id di video_data.py
- Check video still in Telegram
- Try different video
- Bot punya permission forward

## 🛠️ Advanced

### Batch Upload Videos
```python
# upload_videos.py
import json
from video_data import DRAMAS

with open('videos.json') as f:
    new_videos = json.load(f)
    
for video in new_videos:
    drama_id = video['drama_id']
    for idx, part in enumerate(video['parts'], 1):
        DRAMAS[drama_id]['parts'][f'part_{idx}'] = part
```

### GitHub Auto-Update
```bash
# Create update script
cat > /home/user/update.sh << 'EOF'
#!/bin/bash
cd /home/user/susidrama
git pull origin main
sudo systemctl restart susidrama
EOF

chmod +x /home/user/update.sh
```

## 📞 Support

- **Admin:** @xiu039
- **Channel:** @susi_drama
- **Help:** `/help` command in bot

## 📝 License

MIT License - Feel free to use & modify

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-04  
**Created with ❤️ for Susi Drama Bot**

🎬 Happy Drama Streaming! 🍿
