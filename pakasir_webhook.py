"""Flask webhook receiver for Pakasir payments.

Usage (production): run behind a process manager (gunicorn) and reverse-proxy via Nginx.

Endpoints:
- POST /webhook/pakasir  : receive Pakasir webhook and verify via transactiondetail
- GET  /health           : health check

This handler calls `payment.get_pakasir().verify_and_confirm(order_id)`
after confirming the transaction detail with Pakasir.
"""
import os
import logging
from flask import Flask, request, jsonify

from payment import get_pakasir

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pakasir_webhook")

pakasir = get_pakasir()


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/webhook/pakasir', methods=['POST'])
def pakasir_webhook():
    data = request.get_json(force=True, silent=True)
    logger.info('Received webhook: %s', data)

    if not data:
        return jsonify({'status': 'ignored', 'reason': 'no_json'}), 400

    # Pakasir body example: {"amount":22000, "order_id":"240910HDE7C9", "project":"depodomain", "status":"completed"}
    order_id = data.get('order_id') or data.get('orderId') or data.get('ref_id')
    amount = data.get('amount')
    status = data.get('status')

    if not order_id or amount is None:
        logger.warning('Webhook missing order_id or amount')
        return jsonify({'status': 'ignored', 'reason': 'missing_fields'}), 400

    try:
        # Prefer authoritative check via transactiondetail API
        detail = pakasir.transaction_detail(order_id, amount)
        logger.info('transaction_detail response: %s', detail)

        txn = None
        if isinstance(detail, dict):
            txn = detail.get('transaction') or detail.get('data')

        # If transaction detail shows completed -> confirm and process
        if txn and txn.get('status') == 'completed':
            ok = pakasir.verify_and_confirm(order_id)
            if ok:
                logger.info('Payment confirmed for %s', order_id)
                return jsonify({'status': 'ok'}), 200
            else:
                logger.error('verify_and_confirm failed for %s', order_id)
                return jsonify({'status': 'error'}), 500

        # As fallback, if webhook status indicates completed, attempt verify_and_confirm
        if status and status.lower() == 'completed':
            ok = pakasir.verify_and_confirm(order_id)
            if ok:
                logger.info('Payment confirmed (fallback) for %s', order_id)
                return jsonify({'status': 'ok'}), 200

        logger.info('Payment not completed or not verified yet for %s', order_id)
        return jsonify({'status': 'ignored'}), 202

    except Exception as e:
        logger.exception('Error handling webhook: %s', e)
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    # For quick local testing only. In production use gunicorn + systemd + nginx.
    port = int(os.getenv('WEBHOOK_PORT', 5000))
    host = os.getenv('WEBHOOK_HOST', '0.0.0.0')
    app.run(host=host, port=port)
