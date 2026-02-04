# 📋 PROJECT STRUCTURE & FILE INDEX

## 🎯 Complete Project Overview

```
susidrama/
├── 📄 susidrama.py                    (2000+ lines) - Main bot script
├── ⚙️  config.py                       - Configuration & settings
├── 🎬 video_data.py                    - Drama/video database
├── 🔥 firebase_db.py                   - Firebase integration
├── 💳 payment.py                       - Pakasir payment gateway
├── 📺 content.py                       - Content management
│
├── 📦 requirements.txt                 - Python dependencies
├── 🔐 .env.example                     - Environment template
├── .gitignore                          - Git ignore rules
│
├── 📖 Documentation Files:
│   ├── README.md                       - Main documentation
│   ├── SETUP.md                        - Complete setup guide
│   ├── QUICKSTART.md                   - 5-minute quick start
│   ├── FIREBASE_SETUP.md               - Firebase configuration
│   ├── PAKASIR_SETUP.md                - Pakasir payment setup
│   └── BOT_SETUP.md                    - Telegram bot setup
│
├── 🛠️ Utility Scripts:
│   ├── test_bot.py                     - Bot testing suite
│   └── get_file_id.py                  - Get video file IDs
│
└── 📚 This File:
    └── FILE_STRUCTURE.md               - Project structure
```

## 📄 File Descriptions

### Core Files (Production Code)

#### `susidrama.py` (Main Bot - 2000+ lines)
- **Purpose:** Main bot script dengan semua command & button handlers
- **Key Functions:**
  - `start()` - /start command handler
  - `button_callback()` - Button & menu handlers
  - `search_handler()` - Search drama functionality
  - `watch_drama()` - Video streaming logic
  - `main()` - Bot initialization & polling
- **Dependencies:** telegram, firebase_db, payment, content, config
- **Usage:** `python susidrama.py`

#### `config.py` (Configuration - 80 lines)
- **Purpose:** Centralized configuration & settings
- **Key Elements:**
  - Telegram & Firebase credentials (from .env)
  - VIP packages definition
  - Referral commission rates
  - Admin IDs & channel settings
  - Min withdrawal amount
- **Edit For:** Harga VIP, komisi, setting lainnya
- **Import:** `from config import TELEGRAM_BOT_TOKEN, VIP_PACKAGES`

#### `video_data.py` (Drama Database - 150+ lines)
- **Purpose:** Drama & video data storage (terpisah untuk mudah di-edit)
- **Structure:** Dictionary dengan format:
  ```python
  DRAMAS = {
      'drama_id': {
          'id', 'title', 'thumbnail', 'description',
          'parts': {'part_1': {video_id, is_free, duration}}
      }
  }
  ```
- **Key Functions:**
  - `get_all_dramas()` - Get semua drama
  - `search_drama(query)` - Search by title
  - `get_drama_by_id(id)` - Get specific drama
  - `get_drama_part(id, part_key)` - Get video part
- **Edit For:** Tambah drama, edit video IDs, update titles
- **No dependencies:** Pure Python data file

#### `firebase_db.py` (Firebase Integration - 300+ lines)
- **Purpose:** Handle all Firebase Realtime Database operations
- **Key Classes:** `FirebaseDB` singleton
- **Key Methods:**
  - User management: `create_user()`, `get_user()`, `update_user()`
  - VIP system: `activate_vip()`, `check_vip_status()`
  - Referral: `set_referrer()`, `get_referral_code()`
  - Balance: `add_balance()`, `subtract_balance()`, `get_balance()`
  - Payments: `create_payment_record()`, `update_payment_status()`
  - Statistics: `get_user_statistics()`
- **Database:** Firebase Realtime DB
- **Error Handling:** Try-except untuk semua operations
- **Usage:** `firebase = get_firebase_db()`

#### `payment.py` (Pakasir Payment - 200+ lines)
- **Purpose:** Payment gateway integration & QRIS generation
- **Key Classes:** `PakasirPayment` singleton
- **Key Methods:**
  - `create_invoice()` - Create payment invoice
  - `generate_qris()` - Generate QRIS code
  - `check_payment_status()` - Check payment status
  - `confirm_payment()` - Confirm & activate VIP
  - `_generate_signature()` - Sign requests
- **API:** Pakasir API integration
- **Commission:** Auto-process referral commission
- **Usage:** `pakasir = get_pakasir()`

#### `content.py` (Content Management - 200+ lines)
- **Purpose:** Drama & video content management
- **Key Classes:** `ContentManager` singleton
- **Key Methods:**
  - `get_all_dramas()`, `get_drama()`, `search_dramas()`
  - `get_drama_parts()`, `get_drama_part_video()`
  - `get_next_part()`, `get_drama_free_parts()`, `get_drama_vip_parts()`
  - `count_dramas()`, `count_total_parts()`
  - `add_drama()`, `add_part_to_drama()`
- **Data Source:** video_data.py
- **VIP Check:** Verify user VIP status sebelum streaming
- **Usage:** `content = get_content_manager()`

### Configuration Files

#### `.env.example` (Environment Template)
- **Purpose:** Template untuk environment variables
- **Usage:** `cp .env.example .env` kemudian edit
- **Contains:**
  - TELEGRAM_BOT_TOKEN
  - FIREBASE credentials (5 fields)
  - PAKASIR credentials
  - Channel settings
  - Admin IDs

#### `.env` (Actual Environment - NOT IN GIT)
- **Purpose:** Menyimpan credentials sensitif
- **Security:** Jangan commit ke git, sudah di .gitignore
- **Edit:** `nano .env` kemudian paste credentials

#### `.gitignore` (Git Ignore Rules)
- **Purpose:** Specify files to ignore dari git
- **Contains:** .env, __pycache__, venv/, logs, backups
- **Usage:** Automatic via git, tidak perlu di-edit

#### `requirements.txt` (Dependencies)
- **Purpose:** Menyimpan semua Python package dependencies
- **Usage:** `pip install -r requirements.txt`
- **Current Packages:**
  - python-telegram-bot==13.15
  - python-dotenv==0.19.0
  - firebase-admin==5.3.0
  - requests==2.28.0

### Utility Scripts

#### `test_bot.py` (Testing Suite - 150+ lines)
- **Purpose:** Comprehensive testing sebelum production
- **Tests:**
  - Environment variables check
  - Module imports
  - Telegram bot connection
  - Firebase connection
  - Video data loading
- **Usage:** `python test_bot.py`
- **Output:** ✅/❌ status untuk setiap test

#### `get_file_id.py` (Video File ID Helper - 50 lines)
- **Purpose:** Helper untuk mendapatkan Telegram video file IDs
- **How to:**
  1. Forward video ke bot
  2. Ambil file_id dari response
  3. Copy ke video_data.py
- **Usage:** `python get_file_id.py`
- **Note:** Dokumentasi & examples included

### Documentation Files

#### `SETUP.md` (Complete Setup Guide - 500+ lines)
- **Sections:**
  1. Features overview
  2. System requirements
  3. Installation steps
  4. Firebase setup
  5. Pakasir setup
  6. Telegram bot setup
  7. Configuration guide
  8. Project structure
  9. Add drama guide
  10. VPS deployment
  11. Troubleshooting
  12. Support info
- **Read First:** Jika baru first-time setup

#### `QUICKSTART.md` (5-Minute Quick Start)
- **Purpose:** Fast-track untuk yang sudah familiar
- **Contains:** Condensed version dari full SETUP.md
- **Usage:** `cat QUICKSTART.md` untuk quick reference

#### `FIREBASE_SETUP.md` (Firebase Configuration)
- **Sections:**
  1. Create Firebase project
  2. Setup Realtime Database
  3. Security rules configuration
  4. Generate service account key
  5. Copy to .env
  6. Test connection
  7. Troubleshooting
  8. Database structure overview
- **Target:** Beginner Firebase users

#### `PAKASIR_SETUP.md` (Payment Gateway Setup)
- **Sections:**
  1. Daftar & setup merchant
  2. Generate API keys
  3. Webhook configuration
  4. Copy to .env
  5. Test payment
  6. QRIS setup
  7. Payment flow
  8. Webhook integration
  9. Troubleshooting
- **Target:** Payment integration setup

#### `BOT_SETUP.md` (Telegram Bot Configuration)
- **Sections:**
  1. Create bot di BotFather
  2. Copy token
  3. Setup commands
  4. Setup description
  5. Privacy settings
  6. Channel forwarding
  7. Test bot
  8. Admin commands
  9. Security settings
  10. Testing checklist
- **Target:** Telegram bot configuration

#### `README.md` (Main Documentation)
- **Purpose:** Markdown version dari file ini (lebih detailed)
- **Usage:** Check untuk full explanation

#### `FILE_STRUCTURE.md` (This File)
- **Purpose:** Dokumentasi lengkap struktur & index file
- **Usage:** Reference untuk understand project layout

## 🔄 Data Flow Architecture

```
User Input (Telegram)
    ↓
susidrama.py (handlers)
    ├→ config.py (get settings)
    ├→ firebase_db.py (get/update user)
    ├→ video_data.py (get drama list)
    ├→ content.py (manage content)
    └→ payment.py (process payment)
    ↓
Firebase (store data)
Pakasir (process payment)
    ↓
Response to User (via Telegram)
```

## 📊 File Dependencies Map

```
susidrama.py
├── config.py
├── firebase_db.py
│   └── (Firebase Admin SDK)
├── payment.py
│   └── firebase_db.py
├── content.py
│   └── video_data.py
└── video_data.py

config.py
└── (python-dotenv for .env)

firebase_db.py
├── config.py
└── (firebase_admin)

payment.py
├── config.py
├── firebase_db.py
└── (requests, hashlib)

content.py
└── video_data.py
```

## 🎯 Edit Guide by Use Case

### Menambah Drama Baru
1. Edit: `video_data.py`
2. Copy format `drama_XXX` entry
3. Add entry ke `DRAMAS` dictionary
4. Restart bot

### Mengubah Harga VIP
1. Edit: `config.py`
2. Section: `VIP_PACKAGES`
3. Change `'price'` values
4. Restart bot

### Mengubah Komisi Referral
1. Edit: `config.py`
2. Section: `REFERRAL_COMMISSION`
3. Change percentage values
4. Restart bot

### Menambah Admin Commands
1. Edit: `susidrama.py`
2. Add function after existing handlers
3. Add handler di main()
4. Restart bot

### Debugging Issues
1. Run: `python test_bot.py`
2. Check logs: `python susidrama.py`
3. Check .env credentials
4. Check Firebase database

## 📈 Lines of Code Summary

| File | Lines | Purpose |
|------|-------|---------|
| susidrama.py | ~2000 | Main bot |
| firebase_db.py | ~300 | Firebase ops |
| payment.py | ~200 | Payment gateway |
| content.py | ~200 | Content mgmt |
| config.py | ~80 | Configuration |
| video_data.py | ~150 | Drama database |
| test_bot.py | ~150 | Testing |
| **TOTAL** | **~3100** | **Production code** |

## 🔐 Security Considerations

### Sensitive Files (Never Commit)
- `.env` - Contains API keys & credentials
- `*.log` - Logs bisa contain sensitive data
- `backup_*.json` - Database backups

### Protected by .gitignore
```
.env
__pycache__/
*.log
backup_*.json
```

### Production Security
- Use environment variables untuk credentials
- Implement HTTPS untuk webhook
- Validate payment signatures
- Rate limiting untuk API calls
- Error handling tanpa expose sensitive data

## 🚀 Deployment Checklist

- [ ] Clone repository
- [ ] Create .env from .env.example
- [ ] Fill all credentials
- [ ] Run `python test_bot.py`
- [ ] Test bot locally: `python susidrama.py`
- [ ] Add sample drama ke video_data.py
- [ ] Deploy ke VPS
- [ ] Setup systemd service
- [ ] Monitor logs
- [ ] Setup backup

---

**Version:** 1.0.0  
**Updated:** 2026-02-04  
**Maintained by:** Susi Drama Team  

🎬 Happy Development!
