# 🚀 Panduan Deployment Webhook Pakasir

Dokumen ini menjelaskan cara setup dan deploy webhook Pakasir untuk auto-activation VIP setelah pembayaran.

## 📋 Prerequisite

- ✅ VPS sudah setup dengan Python, Nginx, dll (lihat DEPLOYMENT_CHECKLIST.md)
- ✅ Pakasir merchant account sudah active
- ✅ Domain atau IP address untuk webhook URL
- ✅ HTTPS/SSL certificate (recommended untuk production)

## 🔧 Quick Setup (Development)

### Jalankan Webhook Lokal

```bash
cd /home/youruser/susidrama
source venv/bin/activate
python pakasir_webhook.py
```

Server akan start di `http://0.0.0.0:5000`

Test endpoint:
```bash
curl http://localhost:5000/health
# Output: {"status":"ok"}
```

## 🌐 Production Deployment dengan Systemd + Nginx

### Step 1: Siapkan Service File

Edit `/home/youruser/susidrama/deploy/susidrama_webhook.service`:

```ini
[Unit]
Description=SusiDrama Pakasir Webhook (gunicorn)
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/youruser/susidrama
Environment="PATH=/home/youruser/susidrama/venv/bin"
Environment="WEBHOOK_HOST=127.0.0.1"
Environment="WEBHOOK_PORT=5000"
ExecStart=/home/youruser/susidrama/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 pakasir_webhook:app

Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**⚠️ Ganti `/home/youruser/` dengan path actual VPS Anda!**

### Step 2: Install Systemd Service

```bash
sudo cp deploy/susidrama_webhook.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable susidrama_webhook
sudo systemctl start susidrama_webhook
```

Verify status:
```bash
sudo systemctl status susidrama_webhook
```

View logs:
```bash
sudo journalctl -u susidrama_webhook -f
```

### Step 3: Configure Nginx Reverse Proxy

Edit `/home/youruser/susidrama/deploy/nginx_pakasir.conf`:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com; # GANTI dengan domain Anda!

    # Redirect HTTP ke HTTPS (uncomment jika sudah ada cert)
    # return 301 https://$host$request_uri;

    location /webhook/pakasir {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_pass http://127.0.0.1:5000;
        proxy_read_timeout 60s;
    }

    location /health {
        proxy_pass http://127.0.0.1:5000/health;
    }

    client_max_body_size 10M;
}
```

**⚠️ Ganti `yourdomain.com` dengan domain Anda!**

Symlink ke enabled sites:
```bash
sudo cp deploy/nginx_pakasir.conf /etc/nginx/sites-available/susidrama_webhook
sudo ln -s /etc/nginx/sites-available/susidrama_webhook /etc/nginx/sites-enabled/
sudo nginx -t  # Test config
sudo systemctl restart nginx
```

### Step 4: Setup SSL/HTTPS (Optional tapi Recommended)

Gunakan Let's Encrypt + Certbot:

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot certonly --nginx -d yourdomain.com
```

Update nginx config untuk HTTPS:
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # ... rest of config
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}
```

Reload Nginx:
```bash
sudo systemctl reload nginx
```

### Step 5: Configure Pakasir Webhook

1. Login ke Pakasir Dashboard
2. Masuk ke **Pengaturan Proyek** atau **Project Settings**
3. Cari **Webhook URL**
4. Paste URL:
   ```
   https://yourdomain.com/webhook/pakasir
   ```
   atau
   ```
   http://yourdomain.com/webhook/pakasir
   ```
   (jika belum setup SSL)

5. Pilih events yang ingin diterima:
   - Payment Success / Pembayaran Berhasil
   - Payment Failed / Pembayaran Gagal (optional)

6. **Save**

### Step 6: Test Webhook

#### 1. Test endpoint health:
```bash
curl https://yourdomain.com/health
# Expected response: {"status":"ok"}
```

#### 2. Test dengan manual simulation:
```bash
curl -X POST https://yourdomain.com/webhook/pakasir \
  -H 'Content-Type: application/json' \
  -d '{
    "amount": 10900,
    "order_id": "TEST_12345",
    "project": "your-project-slug",
    "status": "completed",
    "payment_method": "qris",
    "completed_at": "2024-09-10T08:07:02.819+07:00"
  }'
```

Expected response:
```json
{
  "status": "ok"
}
```

#### 3. Check logs:
```bash
sudo journalctl -u susidrama_webhook -n 50
```

## 📊 Monitoring & Troubleshooting

### Check Service Status
```bash
sudo systemctl status susidrama_webhook
```

### View Live Logs
```bash
sudo journalctl -u susidrama_webhook -f
```

### Restart Service
```bash
sudo systemctl restart susidrama_webhook
```

### Check Nginx Logs
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Common Issues

**❌ Error: Connection refused**
- Check gunicorn running: `sudo systemctl status susidrama_webhook`
- Check port 5000 listening: `sudo lsof -i :5000`
- Restart: `sudo systemctl restart susidrama_webhook`

**❌ Error: 502 Bad Gateway**
- Nginx tidak bisa connect ke gunicorn
- Check gunicorn logs: `sudo journalctl -u susidrama_webhook`
- Verify config: `sudo nginx -t`

**❌ Webhook tidak dipanggil Pakasir**
- Verify webhook URL di Pakasir dashboard
- Check firewall: `sudo ufw allow 443`
- Test manual webhook (lihat step 6.2)

**❌ Payment tidak auto-activated**
- Check Firebase credentials di .env
- Check Pakasir API key di .env
- View logs: `sudo journalctl -u susidrama_webhook`

## 🔄 API Integration Flow

```
User klik "Bayar Sekarang"
    ↓
Bot create invoice → susidrama.py
    ↓
Bot show QRIS → User scan & bayar
    ↓
Pakasir terima pembayaran
    ↓
Pakasir POST ke webhook
    ↓
pakasir_webhook.py receive
    ↓
Verify via transactiondetail API
    ↓
Firebase update + activate VIP + distribute commission
    ↓
User auto-unlock akses VIP ✅
```

## 🚀 Deployment Checklist Webhook

- [ ] Webhook code reviewed (`pakasir_webhook.py`)
- [ ] Service file prepared (`deploy/susidrama_webhook.service`)
- [ ] Nginx config prepared (`deploy/nginx_pakasir.conf`)
- [ ] Domain/IP ready
- [ ] SSL certificate configured (recommended)
- [ ] Environment variables set (PAKASIR_API_KEY, PAKASIR_PROJECT)
- [ ] Service started: `sudo systemctl start susidrama_webhook`
- [ ] Nginx reloaded: `sudo systemctl reload nginx`
- [ ] Webhook URL registered di Pakasir dashboard
- [ ] Test health endpoint
- [ ] Test with manual simulation webhook
- [ ] Monitor logs during live test payment
- [ ] Verify VIP auto-activated after payment
- [ ] Setup monitoring/alerting (optional)

## 💡 Monitoring Best Practice

Setup monitoring alerts untuk webhook service:

```bash
# Simple cron job to monitor service
(crontab -l 2>/dev/null; echo "*/5 * * * * systemctl is-active --quiet susidrama_webhook || systemctl restart susidrama_webhook") | crontab -
```

## 📞 Support

Jika ada masalah:
1. Check logs: `sudo journalctl -u susidrama_webhook`
2. Test manual: curl test endpoint
3. Verify config: `sudo nginx -t`
4. Restart service: `sudo systemctl restart susidrama_webhook`

---

**✅ Webhook setup complete! Payment auto-activation sekarang ready.** 🎉

