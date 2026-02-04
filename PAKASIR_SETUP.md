# PANDUAN SETUP PAKASIR PAYMENT GATEWAY

## 1. Daftar Pakasir

1. Buka https://pakasir.id
2. Klik "Daftar"
3. Isi form:
   - Email
   - Password
   - Nama bisnis: "Susi Drama"
   - Tipe bisnis: "Media/Entertainment"
4. Verifikasi email
5. Login

## 2. Setup Merchant Account

1. Masuk ke dashboard Pakasir
2. Lengkapi profil:
   - Nama merchant
   - Alamat
   - Nomor identitas
   - Bank account (untuk withdraw)
3. Verifikasi data (tunggu ~1-2 jam)

## 3. Generate API Key & Project Slug

1. Di dashboard, klik "Pengaturan" atau halaman proyek
2. Salin **API Key** untuk proyek Anda
3. Catat juga **Project Slug** (biasanya nama proyek/slug seperti `depodomain`)

⚠️ Simpan `API Key` dengan aman, jangan share!

## 4. Setup Webhook (Optional)

Untuk auto-confirm payment:

1. Di Pengaturan → "Webhook"
2. URL: `https://yourbot.com/webhook/pakasir`
3. Pilih events: "Payment Success"
4. Save

## 5. Copy ke .env

```ini
PAKASIR_API_KEY=pak_xxxxx_xxxxxx
PAKASIR_PROJECT=your-project-slug
PAKASIR_API_URL=https://app.pakasir.com/api
```

## 6. Test Payment

```bash
python -c "
from payment import get_pakasir

pakasir = get_pakasir()

# Test create invoice (uses paymentsimulation endpoint)
invoice = pakasir.create_invoice(
    user_id=123456789,
    amount=10900,
    package_id='7_hari',
    reference_id='test_12345',
    simulate=True
)

if invoice:
    print('✅ Invoice created:', invoice)
else:
    print('❌ Failed to create invoice')
"
```

## 7. Setup QRIS (Manual)

Jika Pakasir belum support QRIS auto, gunakan manual:

1. Login ke Pakasir Dashboard
2. Masuk ke "Pembayaran"
3. Buat invoice manual
4. Pakasir akan generate QRIS
5. Screenshot QRIS
6. Upload ke server

Kemudian di bot, update file_id gambar QRIS.

## Payment Flow

```
User klik "Bayar Sekarang"
    ↓
Bot create invoice di Pakasir
    ↓
Bot generate QRIS code
    ↓
User scan QRIS & bayar
    ↓
Payment gateway confirm
    ↓
Bot auto-activate VIP
    ↓
User mendapat akses
```

## Webhook Integration

```python
# payment_webhook.py
from flask import Flask, request, jsonify
from payment import get_pakasir

app = Flask(__name__)
pakasir = get_pakasir()

@app.route('/webhook/pakasir', methods=['POST'])
def pakasir_webhook():
    data = request.json

    # Pakasir will POST fields like: amount, order_id, project, status, payment_method, completed_at
    order_id = data.get('order_id')
    amount = data.get('amount')
    status = data.get('status')

    # Basic sanity check
    if not order_id or not amount:
        return jsonify({'status': 'ignored', 'reason': 'missing_fields'}), 400

    # Recommended: Verify with transactiondetail API for authoritative status
    verified = pakasir.transaction_detail(order_id, amount)
    txn = verified.get('transaction') if isinstance(verified, dict) else None
    if txn and txn.get('status') == 'completed':
        # mark as confirmed and process VIP + commissions
        pakasir.verify_and_confirm(order_id)
        return jsonify({'status': 'ok'})

    # If transactiondetail not available or not completed, ignore
    return jsonify({'status': 'ignored'})

if __name__ == '__main__':
    app.run(port=5000)
```

## Troubleshooting

### Error: "Invalid API Key"
- Check API key di .env
- Verify di Pakasir dashboard
- Re-generate jika perlu

### QRIS tidak muncul
- Check account status (aktif?)
- Verify merchant onboarding complete
- Contact Pakasir support

### Payment tidak terdeteksi
- Check webhook URL correct
- Verify signature validation
- Check Firebase payment record

## Payment Methods Supported by Pakasir

- 💰 Bank Transfer (semua bank)
- 📱 E-Wallet:
  - Dana
  - OVO
  - GoPay
  - LinkAja
  - DOKU
- 🔳 QRIS (semua bank)
- 💳 Virtual Account

---

✅ Pakasir setup complete! Lanjut ke setup Telegram Bot.
