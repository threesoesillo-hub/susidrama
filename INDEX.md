# 📚 SUSI DRAMA BOT - COMPLETE PROJECT GUIDE

**Version:** 1.0.0  
**Created:** 2026-02-04  
**Status:** ✅ Production Ready

---

## 🎬 What is This?

**Susi Drama Bot** adalah Telegram bot lengkap untuk:
- 📺 Streaming drama dengan sistem VIP
- 💎 Multiple VIP packages (1-90 hari)
- 💰 Referral earning system (3 level)
- 💳 Integrated payment gateway (Pakasir QRIS)
- 🔐 Secure user & video management
- 🚀 Production-ready dengan Firebase database

---

## 📂 What's Included?

### Production Code (~3100 lines)
```
susidrama.py        (Main bot script - 2000+ lines)
config.py           (Configuration)
video_data.py       (Drama database)
firebase_db.py      (Database operations)
payment.py          (Payment gateway)
content.py          (Content management)
```

### Utilities & Tools
```
test_bot.py         (Testing suite)
get_file_id.py      (Video file ID helper)
```

### Complete Documentation
```
README.md           (Overview)
QUICKSTART.md       (5-minute setup)
SETUP.md            (Complete guide)
FIREBASE_SETUP.md   (Firebase config)
PAKASIR_SETUP.md    (Payment config)
BOT_SETUP.md        (Telegram bot config)
FILE_STRUCTURE.md   (File reference)
DEPLOYMENT_CHECKLIST.md (Launch checklist)
```

### Configuration Files
```
.env.example        (Template for environment)
requirements.txt    (Python dependencies)
.gitignore          (Git ignore rules)
```

---

## 🚀 Quick Start (5 Minutes)

### 1. Prerequisites
```bash
# Check Python version
python3 --version    # Must be 3.8+

# Create accounts at:
# - Telegram: Get token from @BotFather
# - Firebase: console.firebase.google.com
# - Pakasir: pakasir.id
```

### 2. Clone & Install
```bash
git clone https://github.com/yourusername/susidrama.git
cd susidrama
pip install -r requirements.txt
```

### 3. Configure
```bash
cp .env.example .env
nano .env  # Paste credentials
```

### 4. Test
```bash
python test_bot.py
```

### 5. Run
```bash
python susidrama.py
```

**Bot sekarang running!** 🎉 Find at: `@your_bot_username`

---

## 📖 Full Documentation Index

### Getting Started
1. **[QUICKSTART.md](QUICKSTART.md)** - 5-minute guide
2. **[README.md](README.md)** - Feature overview

### Setup Guides (Pick All 3)
1. **[FIREBASE_SETUP.md](FIREBASE_SETUP.md)** - Database setup
2. **[PAKASIR_SETUP.md](PAKASIR_SETUP.md)** - Payment setup
3. **[BOT_SETUP.md](BOT_SETUP.md)** - Telegram bot setup

### Reference & Maintenance
1. **[FILE_STRUCTURE.md](FILE_STRUCTURE.md)** - File reference guide
2. **[SETUP.md](SETUP.md)** - Complete setup manual
3. **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Launch checklist

---

## 🎯 Key Features

### User Features
- ✅ **Search Drama** - Find drama by title
- ✅ **Watch Free** - Part 1 gratis setiap drama
- ✅ **Buy VIP** - Unlock dengan QRIS Pakasir
- ✅ **Earn Money** - Referral 3-level system
- ✅ **Profile** - Check status & balance

### Admin Features
- ✅ **Add Drama** - Easy video_data.py editing
- ✅ **Manage VIP** - Auto activation after payment
- ✅ **Monitor Payments** - Firebase dashboard
- ✅ **Track Referrals** - See network & commissions
- ✅ **User Analytics** - Track user stats

### Technical Features
- ✅ **Real-time Database** - Firebase Realtime DB
- ✅ **Payment Integration** - Pakasir QRIS
- ✅ **User Authentication** - Via Telegram ID
- ✅ **VIP Auto-Activation** - After payment confirmed
- ✅ **Video Protection** - Can't record/forward
- ✅ **Commission Auto-Distribution** - 3-level referral

---

## 💻 System Requirements

```
Minimum:
- Python 3.8+
- 512MB RAM
- 100MB disk space
- Stable internet

Recommended:
- Python 3.9+
- 2GB RAM
- 1GB disk space
- VPS with 99.9% uptime
```

---

## 🏗️ Project Structure

```
susidrama/
│
├── 🔴 PRODUCTION CODE (edit only if pro)
│   ├── susidrama.py          (Main bot)
│   ├── config.py             (Settings)
│   ├── firebase_db.py        (Database)
│   ├── payment.py            (Payments)
│   ├── content.py            (Content)
│   └── video_data.py         (Drama database - EDIT THIS!)
│
├── 🟡 UTILITIES
│   ├── test_bot.py           (Testing)
│   └── get_file_id.py        (Video ID helper)
│
├── 🟢 CONFIGURATION
│   ├── .env.example          (Config template)
│   ├── .env                  (Your credentials)
│   ├── .gitignore            (Git rules)
│   └── requirements.txt      (Dependencies)
│
└── 🔵 DOCUMENTATION
    ├── README.md             (Main overview)
    ├── QUICKSTART.md         (Quick guide)
    ├── SETUP.md              (Complete guide)
    ├── FIREBASE_SETUP.md     (Firebase)
    ├── PAKASIR_SETUP.md      (Payment)
    ├── BOT_SETUP.md          (Telegram)
    ├── FILE_STRUCTURE.md     (File reference)
    └── DEPLOYMENT_CHECKLIST.md (Launch)
```

---

## ⚡ Common Tasks

### Add Drama
```
1. Open: video_data.py
2. Copy drama_XXX entry
3. Change title, video_id, parts
4. Save & restart bot
```

### Change VIP Price
```
1. Open: config.py
2. Find: VIP_PACKAGES
3. Change: 'price' value
4. Restart bot
```

### Deploy to VPS
```
1. SSH: ssh user@vps_ip
2. Setup: git clone & install
3. Config: nano .env
4. Service: systemctl start susidrama
```

### Monitor Bot
```
# Check status
sudo systemctl status susidrama

# View logs (real-time)
sudo journalctl -u susidrama -f

# Restart
sudo systemctl restart susidrama
```

---

## 🔐 Security Notes

### Don't Commit These
```
.env                 (Contains API keys)
__pycache__/        (Python cache)
*.log               (Logs)
backup_*.json       (Database backups)
```

### Already Protected
```
.gitignore configured ✅
API keys in .env ✅
Database rules set ✅
Admin IDs restricted ✅
```

---

## 📊 Database Schema

### Users Collection
```
users/
├── user_id (Telegram ID)
├── first_name
├── joined_date
├── vip_status (true/false)
├── vip_expiry (date)
├── balance (Rp)
├── referral_code
└── downlines (L1/L2/L3 count)
```

### Payments Collection
```
payments/
├── payment_id
├── user_id
├── amount
├── package_id
├── status (pending/confirmed)
└── created_at
```

### Transactions Collection
```
transactions/
├── user_id
  ├── transaction_id
  ├── type (credit/debit)
  ├── amount
  ├── reason
  └── timestamp
```

---

## 💳 Payment Flow

```
User clicks "Bayar Sekarang"
    ↓
Bot creates invoice in Pakasir
    ↓
Bot generates QRIS code
    ↓
User scans & pays
    ↓
Payment confirmed by Pakasir
    ↓
Firebase payment updated
    ↓
VIP auto-activated
    ↓
Referral commission calculated
    ↓
User gets access
```

---

## 💰 Referral System

```
Commission Structure:
- L1 (Direct): 20%     → Rp4,180 per Rp20,900
- L2 (Sub):   3%       → Rp627 per Rp20,900
- L3 (Sub²):  2%       → Rp418 per Rp20,900

Total Earning Potential:
- Per successful referral: 25% dari harga
- Unlimited network depth
- Instant commission credit
- Min withdrawal: Rp10,000
```

---

## 🧪 Testing

### Before Production
```bash
python test_bot.py        # Run tests
python susidrama.py       # Test locally
# Then test all features in Telegram
```

### Production Monitoring
```bash
# Check status
sudo systemctl status susidrama

# Real-time logs
sudo journalctl -u susidrama -f

# Performance
top
df -h
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Bot not responding | Check token, restart bot |
| Firebase error | Verify .env credentials |
| Payment fails | Check Pakasir API key |
| Video won't play | Verify file_id in video_data.py |
| VPS high CPU | Check logs, optimize queries |

**Full troubleshooting:** See [SETUP.md](SETUP.md#troubleshooting)

---

## 📞 Support & Contact

- **Creator:** [Your Name]
- **Admin:** @xiu039
- **Channel:** @susi_drama
- **Support:** Email / Telegram

---

## 🎓 Learning Resources

### Related Technologies
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **Firebase:** https://firebase.google.com
- **Python:** https://python.org
- **Pakasir:** https://pakasir.id

### Other Bots Using Same Tech
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

---

## 📝 License & Credits

```
Project: Susi Drama Bot
Version: 1.0.0
License: MIT
Created: 2026-02-04

Built with:
- python-telegram-bot
- firebase-admin
- requests
- python-dotenv
```

---

## ✅ Pre-Launch Checklist

Essential items before going live:

- [ ] All tests passed ✅
- [ ] Firebase database ready
- [ ] Pakasir merchant verified
- [ ] Telegram bot created
- [ ] .env properly configured
- [ ] Sample drama added
- [ ] VPS setup complete
- [ ] Systemd service configured
- [ ] Monitoring enabled
- [ ] Backup scheduled

**See:** [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for complete list

---

## 🚀 Next Steps

1. **Read:** [QUICKSTART.md](QUICKSTART.md) (5 min)
2. **Setup:** [FIREBASE_SETUP.md](FIREBASE_SETUP.md) (15 min)
3. **Config:** [PAKASIR_SETUP.md](PAKASIR_SETUP.md) (15 min)
4. **Deploy:** [BOT_SETUP.md](BOT_SETUP.md) (10 min)
5. **Test:** `python test_bot.py` (2 min)
6. **Run:** `python susidrama.py` (1 min)
7. **Launch:** [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

---

## 📞 Questions?

**Common Questions answered in:**
- Feature details → [README.md](README.md)
- Setup issues → [SETUP.md](SETUP.md)
- File reference → [FILE_STRUCTURE.md](FILE_STRUCTURE.md)
- Deployment → [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

---

## 🎉 Ready to Launch?

You have everything you need! 

1. ✅ Complete source code
2. ✅ Full documentation
3. ✅ Setup guides for all services
4. ✅ Testing tools
5. ✅ Deployment instructions

**Start with:** [QUICKSTART.md](QUICKSTART.md)

---

**Happy Drama Streaming! 🎬🍿**

---

*Last Updated: 2026-02-04*
*Documentation Version: 1.0.0*
*All systems ready for production deployment*
