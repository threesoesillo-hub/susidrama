# QUICK START GUIDE - Susi Drama Bot

## ⚡ 5-Minute Setup

### 1. Prerequisites
- Python 3.8+
- Telegram account
- Firebase account
- Pakasir account

### 2. Clone & Install
```bash
git clone https://github.com/yourusername/susidrama.git
cd susidrama
pip install -r requirements.txt
```

### 3. Setup Credentials

**Create `.env` file:**
```bash
cp .env.example .env
```

**Get credentials:**

1. **Telegram Bot Token** (@BotFather)
2. **Firebase JSON** (console.firebase.google.com)
3. **Pakasir API Key** (pakasir.id)

**Edit `.env`:**
```
TELEGRAM_BOT_TOKEN=your_token
FIREBASE_PROJECT_ID=your_project
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_email
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_CERT_URL=your_cert_url
FIREBASE_DATABASE_URL=your_database_url
PAKASIR_API_KEY=your_api_key
PAKASIR_PROJECT=your_project_slug
PAKASIR_API_URL=https://app.pakasir.com/api
```

### 4. Test Bot
```bash
python test_bot.py
```

Should show: ✅ All tests passed

### 5. Run Bot
```bash
python susidrama.py
```

Bot running locally! 🎉

### 6. Add Drama

Edit `video_data.py`:

```python
'drama_new': {
    'title': 'Drama Name',
    'parts': {
        'part_1': {
            'video_id': 'TELEGRAM_FILE_ID',
            'is_free': True
        }
    }
}
```

### 7. Deploy to VPS (Optional)

```bash
# SSH ke VPS
ssh user@vps_ip

# Clone & setup
git clone https://github.com/yourusername/susidrama.git
cd susidrama
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
nano .env  # Paste credentials

# Start service
sudo nano /etc/systemd/system/susidrama.service
# Copy systemd config dari SETUP.md
sudo systemctl start susidrama
```

## 📝 File Quick Reference

| File | Edit untuk... |
|------|---|
| `config.py` | Harga VIP, komisi, settings |
| `video_data.py` | Tambah/edit drama |
| `.env` | Credentials & API keys |
| `susidrama.py` | Logic bot (jangan kecuali pro) |

## 🎬 Add Video Steps

1. Record video
2. Forward ke Telegram bot
3. Get file_id (debug/console)
4. Edit `video_data.py`
5. Add entry:
```python
'part_X': {
    'episode': X,
    'video_id': 'xxx',
    'is_free': False,
    'requires_vip': True,
    'duration': 'xx:xx'
}
```
6. Save & restart bot

## 💰 Commission Formula

```
Referral payment → Firebase payment record
    ↓
confirm_payment() triggered
    ↓
Check referrer (L1)
→ Add 20% to referrer balance
    ↓
Check referrer's referrer (L2)
→ Add 3% to L2 balance
    ↓
Check L2's referrer (L3)
→ Add 2% to L3 balance
```

## 🆘 Quick Troubleshooting

| Error | Fix |
|-------|-----|
| Bot not responding | Check token, restart |
| "No module" error | `pip install -r requirements.txt` |
| Firebase error | Verify .env credentials, check newlines |
| Payment fails | Check Pakasir API key, test callback |
| Video won't play | Verify file_id correct, test with different video |

## 📊 Monitoring

**Check bot status:**
```bash
sudo systemctl status susidrama
```

**View logs:**
```bash
sudo journalctl -u susidrama -f
```

**Restart:**
```bash
sudo systemctl restart susidrama
```

## 🔗 Useful Links

- 📚 Full Docs: `SETUP.md`
- 🔥 Firebase: `FIREBASE_SETUP.md`
- 💳 Payment: `PAKASIR_SETUP.md`
- 🤖 Bot: `BOT_SETUP.md`
- 🧪 Testing: `python test_bot.py`

## 🎯 Next Steps

1. ✅ Run bot locally
2. ✅ Test all features
3. ✅ Add your drama videos
4. ✅ Deploy to VPS
5. ✅ Setup auto-start
6. ✅ Monitor & maintain

## 💬 Need Help?

- Admin: @xiu039
- Channel: @susi_drama
- Docs: README.md

---

**Good luck! 🚀 Happy drama streaming!**
