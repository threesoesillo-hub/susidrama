# PANDUAN SETUP TELEGRAM BOT

## 1. Create Bot di BotFather

1. Buka Telegram
2. Search: `@BotFather`
3. Chat dengan BotFather
4. Ketik: `/newbot`
5. Ikuti instruksi:
   - **Nama bot:** Susi Drama Bot
   - **Username:** susi_drama_bot (harus unique)
6. BotFather akan memberi token seperti:
   ```
   123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
   ```

## 2. Copy Token ke .env

Buka file `.env`:

```ini
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

## 3. Setup Bot Commands

Di BotFather, ketik: `/mybots`

Pilih bot kamu, kemudian:

### Command List
Ketik: `/setcommands`

Pilih bot, kemudian paste:
```
start - Buka menu utama
help - Tampilkan bantuan
cancel - Batalkan operasi
```

### Bot Description
Ketik: `/setdescription`

Pilih bot, paste:
```
🎬 Bot streaming drama dengan sistem VIP & referral
Nikmati berbagai drama dengan kualitas HD
💎 Upgrade VIP untuk akses unlimited
💰 Dapatkan passive income dari referral
```

### Bot Short Description
Ketik: `/setshortdescription`

Paste:
```
Streaming drama Indonesia - VIP & Referral
```

## 4. Setup Privacy

Ketik: `/setprivacy`

Pilih bot, pilih: **Enable** (recommended untuk production)

Ini membuat bot hanya bisa read private chat dari users.

## 5. Setup Inline Keyboard Buttons

Bot kamu akan otomatis punya buttons (sudah di code):

- 🔍 CARI DRAMA
- 📺 LIST DRAMA
- 💎 BELI VIP
- 💰 DAPATKAN UANG
- 👤 PROFIL

Buttons ini defined di `susidrama.py`

## 6. Setup Channel Forwarding (Optional)

Jika ingin channel khusus untuk drama posting:

1. Create channel: `@susi_drama` (example)
2. Di channel → Settings → Edit
3. Aktifkan Comments
4. Copy channel username

Update di `.env`:
```ini
CHANNEL_ID=-1001234567890
CHANNEL_USERNAME=@susi_drama
DRAMA_CHANNEL_LINK=https://t.me/susi_drama
```

## 7. Test Bot Locally

```bash
python susidrama.py
```

Harusnya output:
```
🚀 Starting Susi Drama Bot...
✅ Bot is running... Press Ctrl+C to stop
```

## 8. Test Commands

Di Telegram chat dengan bot kamu:

- Ketik `/start` - Harus keluar menu utama
- Klik buttons - Harus responsive
- Ketik `/help` - Harus tampil bantuan

## 9. Setup Admin Commands (Optional)

Tambah di `susidrama.py` untuk admin:

```python
def admin_only(func):
    def wrapper(update, context):
        if update.effective_user.id not in ADMIN_IDS:
            update.message.reply_text("❌ Unauthorized")
            return
        return func(update, context)
    return wrapper

@admin_only
def admin_stats(update, context):
    # Get stats
    pass
```

## 10. Security Settings

### Disable Group Membership
Di BotFather:
- Ketik: `/setjoingroups`
- Pilih bot
- Pilih: **Disable**

(Bot hanya bisa dipakai di private chat)

### Disable Comments
Ketik: `/setcommandprivacy`
- Pilih: **Enabled** (users tidak lihat commands di grup)

## Bot Features

Bot kamu support:

✅ Inline keyboards  
✅ Callback queries  
✅ File handling (video)  
✅ Photo sending  
✅ Message editing  
✅ User state management  
✅ Multi-user concurrent  

## Telegram API Limits

⚠️ Perhatian:

- **Message limit:** 30 per detik per user
- **Update limit:** 100 per detik
- **File size:** 2GB max
- **Video:** 50MB per file
- **Rate limit:** Auto-throttling jika exceed

Bot kita sudah handle ini via:
- Queue management
- Drop pending updates
- Error handling

## Testing Checklist

- [ ] Bot respond to /start
- [ ] Menu buttons kerja
- [ ] Search drama berfungsi
- [ ] VIP purchase flow complete
- [ ] Referral link generate
- [ ] Profile tampil correct
- [ ] Video bisa diplay
- [ ] All keyboard navigation smooth

## Production Deployment

Jika sudah test di local:

1. Push ke GitHub
2. Deploy ke VPS
3. Update `.env` di VPS
4. Start bot service
5. Monitor logs

```bash
# VPS
git clone your-repo
cd susidrama
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nano .env  # Setup credentials
python susidrama.py &
```

---

✅ Bot setup complete! Test di Telegram: search `@your_bot_username`
