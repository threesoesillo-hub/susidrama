# 🔧 TROUBLESHOOTING GUIDE - Susi Drama Bot

Panduan lengkap untuk mengatasi masalah yang mungkin terjadi selama development dan production.

---

## 🚨 BOT & TELEGRAM ISSUES

### Problem 1: Bot Tidak Respond

**Gejala:**
- Bot tidak balas pesan
- /start command tidak berfungsi
- Menu tidak muncul

**Penyebab:**
- Token tidak valid
- Bot tidak running
- Internet connection error
- Bot blocked/restricted

**Solusi:**

```bash
# 1. Check bot running
sudo systemctl status susidrama

# 2. Jika tidak running, start
sudo systemctl start susidrama

# 3. Check logs
sudo journalctl -u susidrama -f

# 4. Verify token
nano .env
# Pastikan TELEGRAM_BOT_TOKEN tidak empty

# 5. Test connection
python -c "
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN
bot = Bot(token=TELEGRAM_BOT_TOKEN)
info = bot.get_me()
print(f'Bot: @{info.username}')
"

# 6. Restart bot
sudo systemctl restart susidrama
```

---

### Problem 2: Bot Killed/Crash

**Gejala:**
- Bot suddenly stops
- systemctl shows inactive
- No error message

**Penyebab:**
- Out of memory
- Unhandled exception
- Connection timeout
- Database error

**Solusi:**

```bash
# 1. Check memory usage
free -h
top -b -n 1 | head -20

# 2. Check logs untuk error
sudo journalctl -u susidrama -n 50
# Lihat last 50 lines

# 3. Jika memory issue
# Increase VPS RAM atau optimize code

# 4. Restart service
sudo systemctl restart susidrama

# 5. Enable auto-restart
# Check .service file punya:
# Restart=always
# RestartSec=10

# 6. Monitor kontinyu
sudo journalctl -u susidrama -f &
```

---

### Problem 3: Slow Response

**Gejala:**
- Bot lambat respond
- Button click delay
- Video loading lama

**Penyebab:**
- Database slow query
- Too many concurrent users
- Network latency
- VPS resource bottleneck

**Solusi:**

```bash
# 1. Monitor performance
top -u bot_user
# Check CPU & memory

# 2. Check database latency
python -c "
import time
from firebase_db import get_firebase_db
db = get_firebase_db()
start = time.time()
db.get_user(123456789)
print(f'Query time: {time.time()-start}s')
"

# 3. Optimize Firebase rules
# Check untuk missing indexes

# 4. Scale VPS
# Upgrade CPU/RAM if needed

# 5. Add caching layer
# Implement local cache untuk frequently accessed data

# 6. Rate limiting
# Implement request throttling
```

---

## 🔥 FIREBASE DATABASE ISSUES

### Problem 4: Firebase Connection Error

**Gejala:**
```
Error: Failed to initialize Firebase
Error: Cannot connect to database
Error: Authentication failed
```

**Penyebab:**
- Invalid credentials
- Service account key corrupted
- Firebase rules blocking access
- Network connectivity

**Solusi:**

```bash
# 1. Verify .env file
cat .env | grep FIREBASE
# Pastikan semua fields ada

# 2. Check private key format
# Harus ada:
# FIREBASE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n

# 3. Test credentials
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('PROJECT_ID:', os.getenv('FIREBASE_PROJECT_ID'))
print('CLIENT_EMAIL:', os.getenv('FIREBASE_CLIENT_EMAIL'))
print('KEY present:', bool(os.getenv('FIREBASE_PRIVATE_KEY')))
"

# 4. Validate JSON structure
python -c "
from config import FIREBASE_CONFIG
import json
print(json.dumps(FIREBASE_CONFIG, indent=2))
"

# 5. Check Firebase console
# - Project settings → Service accounts
# - Realtime Database → Rules
# - Check if authenticated

# 6. Re-generate credentials
# Firebase console → Service accounts → Generate new key
```

---

### Problem 5: Database Read/Write Failed

**Gejala:**
- Payment tidak tersimpan
- User data tidak terupdate
- Permission denied error

**Penyebab:**
- Firebase security rules terlalu ketat
- User tidak authorized
- Database offline
- Quota exceeded

**Solusi:**

```bash
# 1. Check security rules
# Firebase console → Database → Rules
# Minimal rules untuk testing:
{
  "rules": {
    ".read": true,
    ".write": true
  }
}

# 2. Verify user permission
python -c "
from firebase_db import get_firebase_db
db = get_firebase_db()
result = db.get_user(123456789)
print('Result:', result)
"

# 3. Check database quota
# Firebase console → Usage
# Jika exceeded, upgrade plan

# 4. Verify database URL
echo $FIREBASE_DATABASE_URL
# Harus: https://your-project.firebaseio.com

# 5. Test write operation
python -c "
from firebase_db import get_firebase_db
db = get_firebase_db()
db.create_user(999999999, 'Test', 'User')
print('✅ Write success')
"

# 6. Clear cache
# Restart bot untuk clear cached connections
```

---

### Problem 6: Database Quota Exceeded

**Gejala:**
```
Error: Quota exceeded
Error: Rate limit
Error: Too many requests
```

**Penyebab:**
- Too many concurrent users
- Inefficient queries
- Loops reading database multiple times
- Firebase free tier limit

**Solusi:**

```bash
# 1. Check current usage
# Firebase console → Usage tab

# 2. Optimize queries
# BEFORE (inefficient):
for user_id in user_list:
    user = db.get_user(user_id)  # N queries

# AFTER (efficient):
users = db.get_all_users()  # 1 query

# 3. Add caching
from functools import lru_cache

@lru_cache(maxsize=100)
def get_user_cached(user_id):
    return db.get_user(user_id)

# 4. Batch operations
# Instead of 100 individual updates
users_batch = {
    'user1': data1,
    'user2': data2
}
db.update_batch(users_batch)  # 1 update

# 5. Upgrade Firebase plan
# Free tier limited, upgrade untuk production

# 6. Archive old data
# Move inactive users ke archive collection
```

---

## 💳 PAYMENT & PAKASIR ISSUES

### Problem 7: Payment Not Processing

**Gejala:**
- QRIS tidak generate
- Payment status stuck di "pending"
- VIP tidak aktif setelah bayar

**Penyebab:**
- Pakasir API error
- Invalid credentials
- Payment signature mismatch
- Webhook not configured

**Solusi:**

```bash
# 1. Verify Pakasir credentials
cat .env | grep PAKASIR

# 2. Test API connection
python -c "
from payment import get_pakasir
pakasir = get_pakasir()
invoice = pakasir.create_invoice(
    user_id=999999999,
    amount=10000,
    package_id='1_hari',
    reference_id='test_12345'
)
print('Invoice:', invoice)
"

# 3. Check Pakasir dashboard
# Verify merchant status: Active?
# Check transaction history

# 4. Test QRIS generation
python -c "
from payment import get_pakasir
pakasir = get_pakasir()
qris = pakasir.generate_qris('ref_123', 10000)
print('QRIS:', qris)
"

# 5. Verify signature
python -c "
from payment import get_pakasir
pakasir = get_pakasir()
sig = pakasir._generate_signature({'test': 'data'})
print('Signature:', sig)
"

# 6. Check webhook
# Pakasir dashboard → Settings → Webhook
# Verify URL correct
```

---

### Problem 8: QRIS Image Not Displaying

**Gejala:**
- QRIS button muncul tapi gambar blank
- "Failed to load image"
- QRIS link error

**Penyebab:**
- QRIS URL invalid
- Image not generated
- Telegram image server issue
- Link expired

**Solusi:**

```bash
# 1. Check QRIS URL
python -c "
from payment import get_pakasir
qris = get_pakasir().generate_qris('ref_123', 10000)
print('QRIS URL:', qris['qris_image'])
# Test buka di browser
"

# 2. Verify QRIS image exists
curl https://api.pakasir.id/qris/ref_123
# Should return image binary

# 3. Use static QRIS for testing
# Temporary use placeholder image:
qris_image = 'https://via.placeholder.com/300x300?text=QRIS'

# 4. Test dengan screenshot QRIS
# Manual: screenshot QRIS dari Pakasir dashboard
# Upload ke server, link di bot

# 5. Check Telegram image limit
# Max 5MB per image
# QRIS harus < 5MB

# 6. Fallback mechanism
# Jika image fail, tampilkan text code
"Manual QRIS: [copy-paste code here]"
"
```

---

### Problem 9: Commission Not Distributed

**Gejala:**
- Referrer balance tidak bertambah
- Commission calculation wrong
- L2/L3 commission missing

**Penyebab:**
- Referral chain not set properly
- Commission logic error
- Payment not confirmed
- Database transaction fail

**Solusi:**

```bash
# 1. Check referral chain
python -c "
from firebase_db import get_firebase_db
db = get_firebase_db()

user = db.get_user(123456789)
print('Referred by:', user.get('referred_by'))

referrer = db.get_user(user.get('referred_by'))
print('L1 referrer:', referrer.get('referral_code'))
print('L1 balance:', referrer.get('balance'))
"

# 2. Verify payment confirmation
python -c "
from firebase_db import get_firebase_db
db = get_firebase_db()

payment = db.get_payment('ref_123')
print('Status:', payment.get('status'))
# Harus: 'confirmed'
"

# 3. Manually trigger commission
python -c "
from payment import get_pakasir
pakasir = get_pakasir()
pakasir.confirm_payment('ref_123')
"

# 4. Check commission calculation
python -c "
amount = 20900
l1 = int(amount * 0.20)  # 4180
l2 = int(amount * 0.03)  # 627
l3 = int(amount * 0.02)  # 418
print(f'L1: {l1}, L2: {l2}, L3: {l3}')
"

# 5. Verify database update
python -c "
from firebase_db import get_firebase_db
db = get_firebase_db()
balance = db.get_balance(referrer_id)
print('Balance:', balance)
"

# 6. Reset & recalculate
# Manual process all pending payments
```

---

## 🎥 VIDEO & STREAMING ISSUES

### Problem 10: Video Won't Play

**Gejala:**
- Video loading infinite
- "Cannot load video"
- Blank video player
- Telegram error

**Penyebab:**
- Invalid file_id
- Video deleted dari Telegram
- File too large
- Telegram API error

**Solusi:**

```bash
# 1. Verify file_id di video_data.py
python -c "
from video_data import get_drama_part
part = get_drama_part('drama_001', 'part_1')
print('File ID:', part.get('video_id'))
# Should be: BAACAgIAAxkB...
"

# 2. Test video exists di Telegram
python -c "
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN
bot = Bot(TELEGRAM_BOT_TOKEN)
file_info = bot.get_file('FILE_ID_HERE')
print('File exists:', file_info)
"

# 3. Check file size
# Video should be < 50MB untuk optimal
# Max Telegram limit: 2GB

# 4. Re-upload video
# Forward fresh video ke bot
# Get new file_id
# Update video_data.py

# 5. Test send video
python -c "
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN
bot = Bot(TELEGRAM_BOT_TOKEN)
bot.send_video(
    chat_id=YOUR_USER_ID,
    video='FILE_ID',
    caption='Test'
)
"

# 6. Check Telegram API status
# Sometime Telegram API down
# Wait & retry later
```

---

### Problem 11: Video Can Be Recorded/Forwarded

**Gejala:**
- User bisa screenshot video
- Video bisa di-forward ke chat lain
- Protection tidak work

**Penyebab:**
- Telegram client capability limitation
- No server-side protection
- Protection only in UI level

**Solusi:**

```python
# NOTE: Telegram tidak provide true DRM
# Protection hanya di client-side

# Best practices:
# 1. Watermark video (video_data.py)
# 2. Limit streaming quality
# 3. Disable forwarding permission
# 4. Add timestamp watermark
# 5. Monitor abuse

# Implementasi watermark:
def send_protected_video(context, chat_id, video_id, title):
    context.bot.send_video(
        chat_id=chat_id,
        video=video_id,
        caption=f"🔒 {title}\nVideo ini property Susi Drama",
        supports_streaming=True,
        # Note: Telegram tidak support disable_forward
        # Ini hanya limitation teknis Telegram
    )
```

---

### Problem 12: Next Part Button Not Appearing

**Gejala:**
- Part selesai tapi no button untuk next part
- User stuck di satu part
- Navigation error

**Penyebab:**
- Part not defined di video_data.py
- Keyboard tidak di-generate
- Message tidak updated

**Solusi:**

```bash
# 1. Verify part exists
python -c "
from video_data import get_drama_by_id
drama = get_drama_by_id('drama_001')
print('Parts:', drama['parts'].keys())
# Should include: part_1, part_2, ...
"

# 2. Check get_next_part function
python -c "
from content import get_content_manager
cm = get_content_manager()
next_p = cm.get_next_part('drama_001', 'part_1')
print('Next part:', next_p)
"

# 3. Verify keyboard building
python -c "
from susidrama import get_next_part_keyboard
kb = get_next_part_keyboard('drama_001', 'part_1')
print('Keyboard:', kb)
"

# 4. Add missing part
# Edit video_data.py
# Add part_X entry:
'part_2': {
    'episode': 2,
    'video_id': 'NEW_FILE_ID',
    'is_free': False,
    'requires_vip': True,
    'duration': '48:00'
}

# 5. Restart bot
sudo systemctl restart susidrama
```

---

## 👤 USER & REFERRAL ISSUES

### Problem 13: VIP Status Not Updating

**Gejala:**
- User still shows "VIP: Not Active"
- But sudah bayar
- Part 2 masih locked

**Penyebab:**
- Payment not confirmed
- Database not updated
- Cache not refreshed
- User ID mismatch

**Solusi:**

```bash
# 1. Check payment status
python -c "
from firebase_db import get_firebase_db
db = get_firebase_db()
payment = db.get_payment('ref_USER_ID_TIMESTAMP')
print('Status:', payment.get('status'))
"

# 2. Check VIP status di database
python -c "
from firebase_db import get_firebase_db
db = get_firebase_db()
user = db.get_user(123456789)
print('VIP:', user.get('vip_status'))
print('Expiry:', user.get('vip_expiry'))
"

# 3. Manually activate VIP
python -c "
from firebase_db import get_firebase_db
db = get_firebase_db()
db.activate_vip(123456789, 7)  # 7 hari
print('✅ VIP activated')
"

# 4. Check user ID mismatch
# Verify user_id di payment = actual Telegram ID

# 5. Refresh cache
# User buka /start lagi
# Bot akan re-query status

# 6. Confirm payment manually
python -c "
from payment import get_pakasir
pakasir = get_pakasir()
pakasir.confirm_payment('ref_123')
"
```

---

### Problem 14: Referral Link Not Working

**Gejala:**
- Click referral link → bot error
- "User not found"
- Referral not recorded

**Penyebab:**
- Invalid referral code format
- User already registered
- Deep link not configured
- Parameter parsing error

**Solusi:**

```bash
# 1. Test referral link
# Format: https://t.me/your_bot?start=ref_USER_ID

# 2. Generate correct code
python -c "
user_id = 123456789
ref_code = f'ref_{user_id}'
link = f'https://t.me/your_bot?start={ref_code}'
print('Link:', link)
"

# 3. Verify code parsing
python -c "
ref_code = 'ref_123456789'
if ref_code.startswith('ref_'):
    referrer_id = int(ref_code.split('_')[1])
    print('Referrer ID:', referrer_id)
"

# 4. Test referral flow
# Click link → should show bot
# /start should register with referrer

# 5. Check database entry
python -c "
from firebase_db import get_firebase_db
db = get_firebase_db()
user = db.get_user(NEW_USER_ID)
print('Referred by:', user.get('referred_by'))
"

# 6. Fix referral link distribution
# Use QR code untuk mobile
# Use shortened URL untuk easy sharing
```

---

## 🌐 VPS & DEPLOYMENT ISSUES

### Problem 15: Bot Not Starting After Reboot

**Gejala:**
- VPS reboot → bot tidak start
- systemctl status = inactive
- Manual start works fine

**Penyebab:**
- systemd service not enabled
- Service file configuration error
- Dependency not met
- File path issue

**Solusi:**

```bash
# 1. Check service enabled
sudo systemctl is-enabled susidrama
# Should output: enabled

# 2. If not enabled
sudo systemctl enable susidrama

# 3. Verify service file
sudo cat /etc/systemd/system/susidrama.service
# Check:
# - WorkingDirectory correct
# - ExecStart correct
# - User correct
# - Environment PATH correct

# 4. Check permissions
ls -la /home/user/susidrama/
# Should be owned by user

# 5. Test service manually
sudo systemctl start susidrama
sudo systemctl status susidrama

# 6. Check dependencies
python3 --version
pip --version
# Verify installed

# 7. Fix and reload
sudo systemctl daemon-reload
sudo systemctl restart susidrama
sudo systemctl enable susidrama
```

---

### Problem 16: High Memory/CPU Usage

**Gejala:**
- Top shows 80%+ CPU
- Memory usage keeps increasing
- VPS slowing down

**Penyebab:**
- Memory leak di code
- Infinite loop
- Too many concurrent connections
- Database query inefficient

**Solusi:**

```bash
# 1. Monitor in real-time
top -u bot_user -p PID
# Or for bot process
ps aux | grep susidrama

# 2. Find memory leak
python -m memory_profiler susidrama.py

# 3. Check for infinite loops
sudo journalctl -u susidrama | tail -100
# Look for repeating errors

# 4. Limit concurrent connections
# Add dalam susidrama.py:
updater = Updater(
    token=TELEGRAM_BOT_TOKEN,
    workers=4,  # Limit workers
    max_queue_size=32
)

# 5. Optimize database queries
# Use caching
# Batch operations
# Add indexes

# 6. Upgrade VPS
# If optimization tidak help
# Increase RAM/CPU

# 7. Restart service
sudo systemctl restart susidrama

# 8. Monitor after fix
free -h
top
```

---

### Problem 17: 502 Bad Gateway (Webhook Error)

**Gejala:**
```
Error 502: Bad Gateway
nginx error log shows connection refused
```

**Penyebab:**
- Bot service down
- Port mismatch
- Nginx misconfigured
- Firewall blocking

**Solusi:**

```bash
# 1. Check bot running
sudo systemctl status susidrama

# 2. Verify port listening
netstat -tulpn | grep python
ss -tulpn | grep 5000

# 3. Check nginx config
sudo cat /etc/nginx/sites-enabled/default
# Should proxy_pass to bot port

# 4. Test local connection
curl http://localhost:5000

# 5. Check firewall
sudo ufw status
# Port 5000 should be open

# 6. Restart services
sudo systemctl restart nginx
sudo systemctl restart susidrama

# 7. Check logs
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u susidrama -f
```

---

## 🔐 SECURITY & PERMISSION ISSUES

### Problem 18: Permission Denied Error

**Gejala:**
```
PermissionError: [Errno 13]
Cannot write to .env file
Cannot create log file
```

**Penyebab:**
- Wrong file owner
- Wrong permissions
- Running as wrong user
- Sudo vs non-sudo mix

**Solusi:**

```bash
# 1. Check file ownership
ls -la /home/user/susidrama/
# Should be owned by 'user'

# 2. Fix ownership
sudo chown -R user:user /home/user/susidrama/

# 3. Set correct permissions
chmod 755 /home/user/susidrama/
chmod 644 /home/user/susidrama/*.py
chmod 600 /home/user/susidrama/.env  # Most restrictive for secrets

# 4. Verify systemd user
sudo cat /etc/systemd/system/susidrama.service
# Should have: User=correct_user

# 5. Fix systemd if needed
sudo nano /etc/systemd/system/susidrama.service
# Change: User=your_username
sudo systemctl daemon-reload

# 6. Create log directory if needed
mkdir -p /home/user/logs
chown user:user /home/user/logs
```

---

### Problem 19: API Key Leaked/Compromised

**Gejala:**
- Security warning from Pakasir
- Unauthorized API calls
- Quota suddenly exceeded

**Penyebab:**
- .env file committed to git
- Someone accessed VPS
- Hardcoded credentials
- Log file exposed

**Solusi:**

```bash
# 1. IMMEDIATE: Revoke old credentials
# Pakasir dashboard → Regenerate API Key
# Firebase → Delete service account key
# Create new one

# 2. Update .env
nano .env
# Paste new credentials

# 3. Clean git history
git rm --cached .env
git commit -m "Remove .env"
# Or better: already in .gitignore

# 4. Check for hardcoded credentials
grep -r "api_key" *.py
grep -r "secret_key" *.py
# Delete if found

# 5. Review logs
sudo grep -r "BEGIN PRIVATE KEY" /var/log/
# Delete exposed logs if any

# 6. Secure permissions
chmod 600 .env

# 7. Monitor for abuse
# Check Pakasir & Firebase for unauthorized activity
```

---

## 📊 MONITORING & MAINTENANCE

### Problem 20: Cannot Monitor Bot Status

**Gejala:**
- Cannot see bot logs
- No way to check status
- Unknown if bot running

**Solusi:**

```bash
# 1. Simple status check
sudo systemctl status susidrama

# 2. Real-time logs
sudo journalctl -u susidrama -f
# Or last 50 lines:
sudo journalctl -u susidrama -n 50

# 3. Specific error search
sudo journalctl -u susidrama | grep ERROR
sudo journalctl -u susidrama | grep error

# 4. Get exact error
sudo journalctl -u susidrama -n 200 > bot_logs.txt
cat bot_logs.txt

# 5. Set up monitoring
# Install monitoring tool:
sudo apt install htop

# 6. Create monitoring script
cat > check_bot.sh << 'EOF'
#!/bin/bash
echo "=== Bot Status ==="
sudo systemctl status susidrama | grep Active
echo "=== Last Errors ==="
sudo journalctl -u susidrama -n 10 | grep -i error
echo "=== Memory ==="
ps aux | grep susidrama | grep -v grep | awk '{print $6}'
EOF

chmod +x check_bot.sh
./check_bot.sh

# 7. Continuous monitoring
watch -n 5 'systemctl status susidrama'
```

---

## ✅ QUICK REFERENCE TABLE

| Problem | Quick Fix |
|---------|-----------|
| Bot not responding | `sudo systemctl restart susidrama` |
| Firebase error | Check .env, verify private key format |
| Payment issue | Verify Pakasir credentials, check Firebase payment record |
| Video won't play | Verify file_id, test with new video |
| VIP not active | Manually confirm payment with `pakasir.confirm_payment()` |
| High CPU | Check for memory leak, restart service |
| Permission denied | Fix file ownership with `chown` |
| Reference error | Check logs with `journalctl` |

---

## 🎯 Debugging Workflow

### When Something Breaks:

1. **Check if bot running:**
   ```bash
   sudo systemctl status susidrama
   ```

2. **Read error logs:**
   ```bash
   sudo journalctl -u susidrama -f
   ```

3. **Identify error type:**
   - Bot error → Check telegram connection
   - Database error → Check Firebase .env
   - Payment error → Check Pakasir API
   - Video error → Check file_id

4. **Test component:**
   ```bash
   python -c "from [module] import ..."
   ```

5. **Fix issue:** (see solutions above)

6. **Restart:**
   ```bash
   sudo systemctl restart susidrama
   ```

7. **Verify:**
   ```bash
   test bot in Telegram
   ```

---

## 📞 Still Need Help?

**Check these docs first:**
- SETUP.md → Setup issues
- FIREBASE_SETUP.md → Database issues
- PAKASIR_SETUP.md → Payment issues
- BOT_SETUP.md → Telegram issues

**Then contact:**
- Admin: @xiu039
- Telegram: @susi_drama

---

**Remember:** Most issues have simple solutions. Always check logs first!

🔧 Happy troubleshooting!
