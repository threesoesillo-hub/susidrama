# ✅ DEPLOYMENT CHECKLIST - Susi Drama Bot

Gunakan checklist ini untuk memastikan semua setup complete sebelum production.

---

## 🔧 PRE-DEPLOYMENT SETUP

### Local Development
- [ ] Python 3.8+ installed
- [ ] pip & venv working
- [ ] Git installed & configured
- [ ] Text editor ready (VS Code/Sublime)

### Account Requirements
- [ ] Telegram account active
- [ ] Firebase account created
- [ ] Pakasir merchant account active
- [ ] Bank account ready (untuk withdraw)

---

## 📥 INSTALLATION PHASE

### 1. Clone & Setup
- [ ] Repository cloned: `git clone ...`
- [ ] Changed to directory: `cd susidrama`
- [ ] Virtual environment created: `python3 -m venv venv`
- [ ] Venv activated: `source venv/bin/activate`
- [ ] Dependencies installed: `pip install -r requirements.txt`

### 2. Environment Configuration
- [ ] `.env.example` copied to `.env`
- [ ] `.env` file NOT committed to git
- [ ] `.gitignore` properly configured

### 3. Telegram Bot Setup
- [ ] Created bot via @BotFather
- [ ] Got bot token (format: `123456:ABC-DEF...`)
- [ ] Pasted `TELEGRAM_BOT_TOKEN` in `.env`
- [ ] Set bot commands (/start, /help, /cancel)
- [ ] Set bot description

### 4. Firebase Setup
- [ ] Firebase project created
- [ ] Realtime Database enabled
- [ ] Service account key generated
- [ ] All 6 Firebase fields copied to `.env`:
  - [ ] FIREBASE_PROJECT_ID
  - [ ] FIREBASE_PRIVATE_KEY_ID
  - [ ] FIREBASE_PRIVATE_KEY
  - [ ] FIREBASE_CLIENT_EMAIL
  - [ ] FIREBASE_CLIENT_ID
  - [ ] FIREBASE_CERT_URL
  - [ ] FIREBASE_DATABASE_URL
- [ ] Security rules configured

### 5. Pakasir Payment Setup
- [ ] Pakasir merchant account created
- [ ] Merchant verification complete
- [ ] API Key generated
- [ ] Project slug noted
- [ ] Pasted `PAKASIR_API_KEY` in `.env`
- [ ] Pasted `PAKASIR_PROJECT` in `.env`
- [ ] Webhook URL configured (production)

### 6. Additional Configuration
- [ ] `CHANNEL_ID` configured (your channel)
- [ ] `CHANNEL_USERNAME` set
- [ ] `DRAMA_CHANNEL_LINK` correct
- [ ] `ADMIN_IDS` added (your Telegram ID)
- [ ] All `.env` values properly filled

---

## 🧪 TESTING PHASE

### Unit Testing
- [ ] Run `python test_bot.py`
- [ ] All tests passed: ✅
  - [ ] Environment variables OK
  - [ ] Imports successful
  - [ ] Telegram bot connection OK
  - [ ] Firebase connection OK
  - [ ] Video data loaded OK

### Local Testing
- [ ] Bot runs: `python susidrama.py`
- [ ] Output: "✅ Bot is running..."
- [ ] No errors in console

### Functionality Testing (Telegram)
- [ ] `/start` command works → Shows menu
- [ ] 🔍 **CARI DRAMA** button works
- [ ] 📺 **LIST DRAMA** button works
- [ ] 💎 **BELI VIP** button works
  - [ ] Package selection works
  - [ ] QRIS generated
  - [ ] Payment simulation works
- [ ] 💰 **DAPATKAN UANG** button works
  - [ ] Referral link generated
  - [ ] Balance display correct
- [ ] 👤 **PROFIL** button works
  - [ ] User info displayed
  - [ ] VIP status shown

### Video Streaming Testing
- [ ] Added sample drama to `video_data.py`
- [ ] Part 1 (free) plays correctly
- [ ] Part 2 (VIP) shows lock message
- [ ] VIP activation shows QRIS
- [ ] Next button works

### Payment Testing
- [ ] Test payment flow complete
- [ ] Firebase payment record created
- [ ] VIP status activated after payment
- [ ] Referral commission calculated

---

## 🎬 CONTENT SETUP

### Drama Management
- [ ] Initial drama added to `video_data.py`
- [ ] Video file IDs obtained from Telegram
- [ ] All parts formatted correctly:
  - [ ] episode number
  - [ ] video_id correct
  - [ ] is_free true/false
  - [ ] requires_vip true/false
  - [ ] duration format correct

### Channel Setup (Optional)
- [ ] Channel created (@susi_drama or custom)
- [ ] Channel description set
- [ ] Admin permissions set
- [ ] First drama posted
- [ ] Comments enabled

---

## 🌐 VPS DEPLOYMENT

### VPS Preparation
- [ ] VPS created (Hostinger/Digital Ocean)
- [ ] Ubuntu 20.04 LTS selected
- [ ] SSH access configured
- [ ] SSH key generated (optional but recommended)
- [ ] Firewall ports opened (22, 443)

### VPS Setup
- [ ] SSH connected: `ssh user@vps_ip`
- [ ] System updated: `sudo apt update`
- [ ] Python 3.8+ installed: `sudo apt install python3`
- [ ] pip installed: `sudo apt install python3-pip`
- [ ] Git installed: `sudo apt install git`
- [ ] virtual env support: `sudo apt install python3-venv`

### Project Deployment
- [ ] Cloned repository on VPS
- [ ] Virtual environment created
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created with all credentials
- [ ] Tested locally first: `python susidrama.py`

### Systemd Service Setup
- [ ] Service file created: `/etc/systemd/system/susidrama.service`
- [ ] Service file configured with:
  - [ ] Correct user
  - [ ] Correct working directory
  - [ ] Correct python path
  - [ ] Restart=always set
- [ ] Daemon reloaded: `sudo systemctl daemon-reload`
- [ ] Service enabled: `sudo systemctl enable susidrama`
- [ ] Service started: `sudo systemctl start susidrama`
- [ ] Service status checked: `sudo systemctl status susidrama`

### Monitoring Setup
- [ ] Logs accessible: `sudo journalctl -u susidrama`
- [ ] Auto-restart verified (if crash)
- [ ] Memory usage monitored: `top` or `htop`
- [ ] Disk space checked: `df -h`

### Backup Setup
- [ ] Backup script created
- [ ] Cron job scheduled (daily backup)
- [ ] Firebase auto-backup enabled
- [ ] Test restore procedure

---

## 📊 PRODUCTION CHECKS

### Security
- [ ] All credentials in `.env` (not hardcoded)
- [ ] `.env` NOT in git repository
- [ ] SSH key secured
- [ ] Firewall properly configured
- [ ] HTTPS enabled (if webhook used)
- [ ] Admin IDs restricted
- [ ] Database rules secured in Firebase

### Performance
- [ ] Bot responds within 1 second
- [ ] Database queries optimized
- [ ] Memory usage < 100MB
- [ ] CPU usage < 20% idle
- [ ] Video streaming smooth
- [ ] No error logs

### Availability
- [ ] Bot auto-starts on VPS reboot
- [ ] Systemd service configured
- [ ] Monitoring dashboard set up
- [ ] Alert system configured
- [ ] 24/7 uptime ready

### Scalability
- [ ] Can handle 100+ concurrent users
- [ ] Database properly indexed
- [ ] API rate limits understood
- [ ] Payment queue working

---

## 🚀 GO-LIVE CHECKLIST

### 24 Hours Before Launch
- [ ] Final testing complete
- [ ] All documentation reviewed
- [ ] Admin trained on operations
- [ ] Support contact ready
- [ ] Announcement prepared

### Launch Day
- [ ] Bot announced to users
- [ ] Channel link shared
- [ ] First drama posted
- [ ] Monitoring team active
- [ ] Bug reports collected

### Post-Launch (First 24 Hours)
- [ ] Monitor logs continuously
- [ ] Check payment flow
- [ ] Verify referral system
- [ ] Monitor user feedback
- [ ] Fix critical bugs immediately

### Post-Launch (First Week)
- [ ] Optimize based on usage
- [ ] Add more drama content
- [ ] Monitor performance metrics
- [ ] Gather user feedback
- [ ] Make improvements

---

## 📈 ONGOING MAINTENANCE

### Daily
- [ ] Check logs for errors
- [ ] Monitor bot status
- [ ] Verify payments processed
- [ ] Check user feedback

### Weekly
- [ ] Review performance metrics
- [ ] Backup database
- [ ] Add new drama content
- [ ] Update video data

### Monthly
- [ ] Security audit
- [ ] Performance optimization
- [ ] Update dependencies (carefully)
- [ ] Backup verification
- [ ] Documentation update

---

## 🆘 TROUBLESHOOTING QUICK REFERENCE

### Bot Not Running
```bash
# Check status
sudo systemctl status susidrama

# View logs
sudo journalctl -u susidrama -f

# Restart
sudo systemctl restart susidrama
```

### Payment Issues
```bash
# Check Firebase payment records
# Check Pakasir API key
# Verify webhook endpoint
```

### Video Not Playing
```bash
# Verify file_id in video_data.py
# Test with another video
# Check Telegram API limits
```

### Database Issues
```bash
# Verify .env credentials
# Check Firebase console
# Test connection: python -c "from firebase_db import get_firebase_db; print('OK')"
```

---

## 📞 SUPPORT CONTACTS

- **Telegram:** @xiu039 (admin)
- **Emergency:** [backup contact]
- **Escalation:** [manager contact]

---

## ✨ LAUNCH READINESS SCORE

Count ✅ marks above:

- **90-100%:** Ready to launch 🚀
- **70-89%:** Almost ready, finish remaining items
- **< 70%:** Not ready, complete all checklist items first

---

**Remember:**
- Don't rush deployment
- Test thoroughly before launch
- Monitor continuously after launch
- Be ready to troubleshoot
- Keep documentation updated
- Regular backups mandatory
- Security is not optional

---

**Good luck! 🎬 Happy Drama Streaming! 🍿**

Last Updated: 2026-02-04
