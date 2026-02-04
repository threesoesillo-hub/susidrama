# Firebase Database Module
import firebase_admin
from firebase_admin import credentials, db, auth
from datetime import datetime, timedelta
import json
from config import FIREBASE_CONFIG, FIREBASE_DATABASE_URL

class FirebaseDB:
    def __init__(self):
        """Inisialisasi Firebase connection"""
        try:
            # Jika belum diinit, init sekarang
            if not firebase_admin._apps:
                cred = credentials.Certificate(FIREBASE_CONFIG)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': FIREBASE_DATABASE_URL
                })
            self.db = db
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
    
    # ==================== USER MANAGEMENT ====================
    
    def create_user(self, user_id, first_name, last_name=None, username=None):
        """Buat user baru di Firebase"""
        try:
            user_data = {
                'user_id': user_id,
                'first_name': first_name,
                'last_name': last_name or '',
                'username': username or '',
                'joined_date': datetime.now().isoformat(),
                'vip_status': False,
                'vip_expiry': None,
                'balance': 0,
                'referral_code': self._generate_referral_code(user_id),
                'referred_by': None,
                'downlines': {
                    'L1': 0,
                    'L2': 0,
                    'L3': 0
                }
            }
            self.db.reference(f'users/{user_id}').set(user_data)
            return user_data
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user(self, user_id):
        """Ambil data user"""
        try:
            return self.db.reference(f'users/{user_id}').get().val()
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def user_exists(self, user_id):
        """Check apakah user sudah ada"""
        user = self.get_user(user_id)
        return user is not None
    
    def update_user(self, user_id, data):
        """Update data user"""
        try:
            self.db.reference(f'users/{user_id}').update(data)
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    # ==================== VIP MANAGEMENT ====================
    
    def activate_vip(self, user_id, days):
        """Aktivasi VIP untuk user"""
        try:
            expiry_date = (datetime.now() + timedelta(days=days)).isoformat()
            self.db.reference(f'users/{user_id}').update({
                'vip_status': True,
                'vip_expiry': expiry_date
            })
            return True
        except Exception as e:
            print(f"Error activating VIP: {e}")
            return False
    
    def check_vip_status(self, user_id):
        """Check status VIP user"""
        try:
            user = self.get_user(user_id)
            if not user:
                return False, None
            
            if not user.get('vip_status'):
                return False, None
            
            expiry_date = datetime.fromisoformat(user.get('vip_expiry', ''))
            if datetime.now() > expiry_date:
                # VIP sudah expired
                self.db.reference(f'users/{user_id}').update({
                    'vip_status': False
                })
                return False, None
            
            return True, user.get('vip_expiry')
        except Exception as e:
            print(f"Error checking VIP status: {e}")
            return False, None
    
    def get_vip_expiry(self, user_id):
        """Dapatkan tanggal expiry VIP"""
        try:
            user = self.get_user(user_id)
            if user and user.get('vip_status'):
                return user.get('vip_expiry')
            return None
        except Exception as e:
            print(f"Error getting VIP expiry: {e}")
            return None
    
    # ==================== REFERRAL SYSTEM ====================
    
    def _generate_referral_code(self, user_id):
        """Generate kode referral unik"""
        return f"ref_{user_id}"
    
    def set_referrer(self, user_id, referrer_id):
        """Set referrer untuk user"""
        try:
            # Update user
            self.db.reference(f'users/{user_id}').update({
                'referred_by': referrer_id
            })
            
            # Update referrer downline
            referrer = self.get_user(referrer_id)
            if referrer:
                current_l1 = referrer.get('downlines', {}).get('L1', 0)
                self.db.reference(f'users/{referrer_id}/downlines/L1').set(current_l1 + 1)
            
            return True
        except Exception as e:
            print(f"Error setting referrer: {e}")
            return False
    
    def get_referral_code(self, user_id):
        """Dapatkan kode referral user"""
        try:
            user = self.get_user(user_id)
            if user:
                return user.get('referral_code')
            return None
        except Exception as e:
            print(f"Error getting referral code: {e}")
            return None
    
    def add_balance(self, user_id, amount, reason=""):
        """Tambah balance user"""
        try:
            user = self.get_user(user_id)
            if user:
                current_balance = user.get('balance', 0)
                new_balance = current_balance + amount
                
                self.db.reference(f'users/{user_id}').update({
                    'balance': new_balance
                })
                
                # Log transaction
                self._log_transaction(user_id, 'credit', amount, reason)
                
                return True
        except Exception as e:
            print(f"Error adding balance: {e}")
            return False
    
    def subtract_balance(self, user_id, amount, reason=""):
        """Kurangi balance user"""
        try:
            user = self.get_user(user_id)
            if user:
                current_balance = user.get('balance', 0)
                if current_balance >= amount:
                    new_balance = current_balance - amount
                    
                    self.db.reference(f'users/{user_id}').update({
                        'balance': new_balance
                    })
                    
                    # Log transaction
                    self._log_transaction(user_id, 'debit', amount, reason)
                    
                    return True
            return False
        except Exception as e:
            print(f"Error subtracting balance: {e}")
            return False
    
    def get_balance(self, user_id):
        """Dapatkan balance user"""
        try:
            user = self.get_user(user_id)
            if user:
                return user.get('balance', 0)
            return 0
        except Exception as e:
            print(f"Error getting balance: {e}")
            return 0
    
    # ==================== PAYMENT MANAGEMENT ====================
    
    def create_payment_record(self, payment_id, user_id, amount, package_id, status='pending'):
        """Buat record pembayaran"""
        try:
            payment_data = {
                'payment_id': payment_id,
                'user_id': user_id,
                'amount': amount,
                'package_id': package_id,
                'status': status,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            self.db.reference(f'payments/{payment_id}').set(payment_data)
            return True
        except Exception as e:
            print(f"Error creating payment record: {e}")
            return False
    
    def update_payment_status(self, payment_id, status):
        """Update status pembayaran"""
        try:
            self.db.reference(f'payments/{payment_id}').update({
                'status': status,
                'updated_at': datetime.now().isoformat()
            })
            return True
        except Exception as e:
            print(f"Error updating payment status: {e}")
            return False
    
    def get_payment(self, payment_id):
        """Dapatkan data pembayaran"""
        try:
            return self.db.reference(f'payments/{payment_id}').get().val()
        except Exception as e:
            print(f"Error getting payment: {e}")
            return None
    
    # ==================== TRANSACTION LOGGING ====================
    
    def _log_transaction(self, user_id, trans_type, amount, reason=""):
        """Log transaksi user"""
        try:
            trans_id = f"{user_id}_{datetime.now().timestamp()}"
            transaction_data = {
                'type': trans_type,
                'amount': amount,
                'reason': reason,
                'timestamp': datetime.now().isoformat()
            }
            self.db.reference(f'transactions/{user_id}/{trans_id}').set(transaction_data)
        except Exception as e:
            print(f"Error logging transaction: {e}")
    
    # ==================== STATISTICS ====================
    
    def get_user_statistics(self, user_id):
        """Dapatkan statistik user"""
        try:
            user = self.get_user(user_id)
            vip_status, vip_expiry = self.check_vip_status(user_id)
            
            stats = {
                'user_id': user_id,
                'name': f"{user.get('first_name')} {user.get('last_name')}".strip(),
                'vip_status': vip_status,
                'vip_expiry': vip_expiry,
                'balance': user.get('balance', 0),
                'referral_code': user.get('referral_code'),
                'joined_date': user.get('joined_date'),
                'downlines': user.get('downlines', {})
            }
            return stats
        except Exception as e:
            print(f"Error getting user statistics: {e}")
            return None

# Singleton instance
firebase_instance = FirebaseDB()

def get_firebase_db():
    """Get Firebase DB instance"""
    return firebase_instance
