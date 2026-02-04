"""Payment Gateway Module - Pakasir Integration (api_key + project slug)

This module was updated to use Pakasir endpoints documented at
https://app.pakasir.com/api — using `api_key` + `project` (slug).
"""
import requests
from datetime import datetime
from config import PAKASIR_API_KEY, PAKASIR_PROJECT, PAKASIR_API_URL
from firebase_db import get_firebase_db


class PakasirPayment:
    def __init__(self):
        self.api_key = PAKASIR_API_KEY
        self.project = PAKASIR_PROJECT
        self.base_url = PAKASIR_API_URL.rstrip('/')
        self.firebase = get_firebase_db()

    def create_invoice(self, user_id, amount, package_id, reference_id, simulate=True):
        """Create invoice / request QRIS.

        For testing you can use the paymentsimulation endpoint (simulate=True).
        In production, depending on your Pakasir setup you may only need to
        persist the invoice locally and wait for webhook/transactiondetail.
        """
        try:
            payload = {
                'project': self.project,
                'order_id': reference_id,
                'amount': int(amount),
                'api_key': self.api_key
            }

            # Create payment record in Firebase as pending
            self.firebase.create_payment_record(
                reference_id,
                user_id,
                int(amount),
                package_id,
                status='pending'
            )

            if simulate:
                url = f"{self.base_url}/paymentsimulation"
                resp = requests.post(url, json=payload, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    # The simulation may not return QRIS image; create client-side URL
                    qris_url = data.get('qris_url') or f"https://app.pakasir.com/qris/{reference_id}"
                    return {
                        'reference_id': reference_id,
                        'amount': int(amount),
                        'qris_url': qris_url,
                        'raw': data
                    }
                else:
                    return {
                        'reference_id': reference_id,
                        'amount': int(amount),
                        'qris_url': f"https://app.pakasir.com/qris/{reference_id}",
                        'raw': {'status_code': resp.status_code, 'body': resp.text}
                    }

            # If not simulating, just return the invoice info and wait for webhook
            return {'reference_id': reference_id, 'amount': int(amount), 'qris_url': None}

        except Exception as e:
            print(f"Error creating invoice: {e}")
            return None

    def transaction_cancel(self, reference_id, amount):
        """Cancel a transaction via Pakasir API."""
        try:
            payload = {
                'project': self.project,
                'order_id': reference_id,
                'amount': int(amount),
                'api_key': self.api_key
            }
            url = f"{self.base_url}/transactioncancel"
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            return {'error': True, 'status_code': resp.status_code, 'body': resp.text}
        except Exception as e:
            print(f"Error cancelling transaction: {e}")
            return None

    def transaction_detail(self, reference_id, amount):
        """Query transaction detail from Pakasir (recommended verification)."""
        try:
            params = {
                'project': self.project,
                'amount': int(amount),
                'order_id': reference_id,
                'api_key': self.api_key
            }
            url = f"{self.base_url}/transactiondetail"
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            return {'error': True, 'status_code': resp.status_code, 'body': resp.text}
        except Exception as e:
            print(f"Error fetching transaction detail: {e}")
            return None

    def verify_and_confirm(self, reference_id):
        """Verify transaction with Pakasir and confirm in Firebase if completed."""
        try:
            payment = self.firebase.get_payment(reference_id)
            if not payment:
                return False

            amount = payment.get('amount')
            # Call transaction detail API for authoritative status
            detail = self.transaction_detail(reference_id, amount)
            if not detail:
                return False

            transaction = detail.get('transaction') or {}
            status = transaction.get('status') or transaction.get('state') or payment.get('status')

            if status == 'completed' or status == 'success':
                # Update firebase record
                self.firebase.update_payment_status(reference_id, 'confirmed')

                # Activate VIP and distribute commissions
                from config import VIP_PACKAGES, REFERRAL_COMMISSION
                user_id = payment.get('user_id')
                package_id = payment.get('package_id')
                amount = int(payment.get('amount', 0))

                if package_id in VIP_PACKAGES:
                    vip_days = VIP_PACKAGES[package_id]['days']
                    self.firebase.activate_vip(user_id, vip_days)

                # Distribute commissions using REFERRAL_COMMISSION config
                user = self.firebase.get_user(user_id)
                if user and user.get('referred_by'):
                    ref1 = user.get('referred_by')
                    comm1 = int(amount * REFERRAL_COMMISSION.get('L1', 20) / 100)
                    self.firebase.add_balance(ref1, comm1, f"Referral commission from {user_id}")

                    ref1_user = self.firebase.get_user(ref1)
                    if ref1_user and ref1_user.get('referred_by'):
                        ref2 = ref1_user.get('referred_by')
                        comm2 = int(amount * REFERRAL_COMMISSION.get('L2', 3) / 100)
                        self.firebase.add_balance(ref2, comm2, f"Referral commission L2 from {user_id}")

                        ref2_user = self.firebase.get_user(ref2)
                        if ref2_user and ref2_user.get('referred_by'):
                            ref3 = ref2_user.get('referred_by')
                            comm3 = int(amount * REFERRAL_COMMISSION.get('L3', 2) / 100)
                            self.firebase.add_balance(ref3, comm3, f"Referral commission L3 from {user_id}")

                return True

            return False
        except Exception as e:
            print(f"Error verifying and confirming payment: {e}")
            return False

    def get_invoice_details(self, reference_id):
        """Retrieve invoice details from Firebase."""
        try:
            payment = self.firebase.get_payment(reference_id)
            if not payment:
                return None
            from config import VIP_PACKAGES
            package_id = payment.get('package_id')
            package_info = VIP_PACKAGES.get(package_id, {})
            return {
                'reference_id': reference_id,
                'user_id': payment.get('user_id'),
                'amount': payment.get('amount'),
                'package': package_info.get('label'),
                'status': payment.get('status'),
                'created_at': payment.get('created_at'),
                'updated_at': payment.get('updated_at')
            }
        except Exception as e:
            print(f"Error getting invoice details: {e}")
            return None


# Singleton instance
pakasir_instance = PakasirPayment()


def get_pakasir():
    return pakasir_instance
