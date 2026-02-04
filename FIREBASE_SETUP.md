# PANDUAN SETUP FIREBASE

## 1. Buat Firebase Project

1. Buka https://console.firebase.google.com
2. Klik "Create a project"
3. Masukkan nama: `susi-drama-bot`
4. Pilih location: Indonesia (Southeast Asia)
5. Klik "Create project"
6. Tunggu prosesnya selesai (~2 menit)

## 2. Setup Realtime Database

1. Di sidebar kiri, klik "Realtime Database"
2. Klik "Create Database"
3. Pilih region: `asia-southeast1` (Indonesia)
4. Pilih mode: **Start in locked mode** (security)
5. Klik "Enable"
6. Tunggu database terbuat

## 3. Konfigurasi Security Rules

1. Di tab "Rules", ganti dengan:

```json
{
  "rules": {
    "users": {
      "$uid": {
        ".read": "auth.uid === $uid || root.child('admin').child(auth.uid).exists()",
        ".write": "auth.uid === $uid || root.child('admin').child(auth.uid).exists()"
      }
    },
    "payments": {
      "$payment_id": {
        ".read": "root.child('admin').child(auth.uid).exists()",
        ".write": "root.child('admin').child(auth.uid).exists()"
      }
    },
    "transactions": {
      "$uid": {
        ".read": "auth.uid === $uid || root.child('admin').child(auth.uid).exists()",
        ".write": "root.child('admin').child(auth.uid).exists()"
      }
    },
    "admin": {
      ".read": false,
      ".write": false
    }
  }
}
```

2. Klik "Publish"

## 4. Generate Service Account Key

1. Di sidebar kiri, klik icon gear (⚙️) → "Project settings"
2. Klik tab "Service accounts"
3. Pilih "Python" di dropdown
4. Klik "Generate new private key"
5. File JSON akan download otomatis
6. Buka file JSON, copy isi

## 5. Copy ke .env

1. Buka file `.env`
2. Cari bagian Firebase
3. Copy value dari JSON ke .env:

```ini
FIREBASE_PROJECT_ID=susi-drama-bot
FIREBASE_PRIVATE_KEY_ID=xxxxx
FIREBASE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nxxx\n-----END PRIVATE KEY-----\n
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxx@susi-drama-bot.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=xxxxx
FIREBASE_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/...
FIREBASE_DATABASE_URL=https://susi-drama-bot.firebaseio.com
```

⚠️ **PENTING:** Untuk `FIREBASE_PRIVATE_KEY`, ganti newline dengan `\n`:
- Find: `-----BEGIN...`
- Replace: `-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n`

## 6. Test Connection

```bash
python -c "from firebase_db import get_firebase_db; db = get_firebase_db(); print('✅ Firebase connected')"
```

## 7. Initial Data Setup (Optional)

Buat struktur awal di Firebase:

```bash
python -c "
from firebase_db import get_firebase_db

firebase = get_firebase_db()

# Test buat user
firebase.create_user(
    user_id=123456789,
    first_name='Test',
    last_name='User'
)

print('✅ Test user created')
"
```

## Troubleshooting Firebase

### Error: "Failed to initialize"
- Check private key format (replace newlines)
- Verify JSON credentials correct
- Check project ID match

### Database tidak bisa di-access
- Check security rules (set to public untuk test)
- Verify API enabled di GCP console
- Check internet connection

### Slow performance
- Optimize rules complexity
- Add indexes untuk large queries
- Check Firebase quota

## Struktur Database

```
users/
├── 123456789/
│   ├── user_id: 123456789
│   ├── first_name: "Budi"
│   ├── joined_date: "2026-02-04..."
│   ├── vip_status: false
│   └── balance: 0

payments/
├── susi_123456789_1707050000/
│   ├── user_id: 123456789
│   ├── amount: 10900
│   ├── package_id: "7_hari"
│   └── status: "pending"

transactions/
└── 123456789/
    └── transaction_id/
        ├── type: "credit"
        ├── amount: 5000
        └── timestamp: "2026-02-04..."
```

---

✅ Firebase setup complete! Lanjut ke setup Pakasir.
