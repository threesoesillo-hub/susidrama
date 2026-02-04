# Susi Drama Bot - Main Script
# Telegram Bot untuk streaming drama dengan sistem VIP & Referral

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, ChatAction
from telegram.ext import (
    Updater, 
    CommandHandler, 
    MessageHandler, 
    Filters, 
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext
)
from datetime import datetime, timedelta
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules
from config import (
    TELEGRAM_BOT_TOKEN,
    VIP_PACKAGES,
    CHANNEL_ID,
    DRAMA_CHANNEL_LINK,
    ADMIN_IDS,
    MIN_WITHDRAWAL
)
from firebase_db import get_firebase_db
from payment import get_pakasir
from content import get_content_manager

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize managers
firebase = get_firebase_db()
pakasir = get_pakasir()
content_manager = get_content_manager()

# States for conversation
CHOOSING_VIP_PACKAGE = 1
CONFIRMING_VIP = 2
SEARCHING_DRAMA = 3
WATCHING_DRAMA = 4
WITHDRAWAL = 5

# ==================== KEYBOARD BUILDERS ====================

def get_main_menu_keyboard():
    """Build main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔍 CARI DRAMA", callback_data='search_drama')],
        [InlineKeyboardButton("📺 LIST DRAMA", callback_data='list_drama'),
         InlineKeyboardButton("💎 BELI VIP", callback_data='buy_vip')],
        [InlineKeyboardButton("💰 DAPATKAN UANG", callback_data='get_money'),
         InlineKeyboardButton("👤 PROFIL", callback_data='profile')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_vip_packages_keyboard():
    """Build VIP packages keyboard"""
    keyboard = []
    for package_id, package_info in VIP_PACKAGES.items():
        keyboard.append([
            InlineKeyboardButton(
                package_info['label'],
                callback_data=f'vip_{package_id}'
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data='back_to_menu')])
    return InlineKeyboardMarkup(keyboard)

def get_referral_keyboard():
    """Build referral menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔗 AMBIL LINK REFERRAL (SHARE)", callback_data='get_referral_link')],
        [InlineKeyboardButton("💵 Saldo & Komisi", callback_data='show_balance')],
        [InlineKeyboardButton("🏧 Tarik Dana", callback_data='withdraw_balance')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_button():
    """Build back button"""
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='back_to_menu')]]
    return InlineKeyboardMarkup(keyboard)

# ==================== START & MENU HANDLERS ====================

def start(update: Update, context: CallbackContext) -> None:
    """Handle /start command"""
    user = update.effective_user
    user_id = user.id
    
    # Create user jika belum ada
    if not firebase.user_exists(user_id):
        firebase.create_user(user_id, user.first_name, user.last_name, user.username)
        
        # Check if ada referral link
        if context.args and len(context.args) > 0:
            ref_code = context.args[0]
            # Extract user_id dari referral code
            if ref_code.startswith('ref_'):
                referrer_id = int(ref_code.split('_')[1])
                firebase.set_referrer(user_id, referrer_id)
    
    # Welcome message
    welcome_text = f"""
👋 Selamat malam, {user.first_name}!
Selamat datang di Susi Drama 📺

Kami menyediakan koleksi drama terbaik dengan berbagai genre. 
Nikmati pengalaman menonton yang menyenangkan bersama kami!

✨ Fitur:
🔍 Cari drama favorit kamu
📺 Nonton drama gratis dan premium
💎 Upgrade ke VIP untuk akses unlimited
💰 Dapatkan komisi referral

Pilih menu di bawah untuk memulai:
"""
    
    update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode=ParseMode.HTML
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Handle /help command"""
    help_text = """
<b>📖 PANDUAN SUSI DRAMA BOT</b>

<b>🔍 CARI DRAMA</b>
Cari drama favorit kamu berdasarkan judul. 
Ketik judul drama yang ingin dicari.

<b>📺 LIST DRAMA</b>
Lihat daftar semua drama yang tersedia.
Klik untuk menonton drama pilihan kamu.

<b>💎 BELI VIP</b>
Upgrade ke member VIP untuk akses unlimited:
• Nonton semua episode tanpa batas
• Kualitas video HD
• Bebas gangguan iklan

<b>💰 DAPATKAN UANG</b>
Dapatkan passive income dengan referral:
• Bagikan link referral ke teman
• Dapatkan komisi setiap kali mereka membeli VIP
• System 3 level untuk earning maksimal

<b>👤 PROFIL</b>
Lihat status VIP dan data profile kamu

<b>❓ PERTANYAAN?</b>
Hubungi admin: @xiu039

Nikmati! 🎬
"""
    
    update.message.reply_text(
        help_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_back_button()
    )

# ==================== MAIN MENU HANDLERS ====================

def button_callback(update: Update, context: CallbackContext) -> int:
    """Handle button clicks"""
    query = update.callback_query
    query.answer()
    user_id = update.effective_user.id
    
    # Search Drama
    if query.data == 'search_drama':
        query.edit_message_text(
            text="🔍 <b>CARI DRAMA</b>\n\nKetik judul drama yang ingin kamu cari:",
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_button()
        )
        return SEARCHING_DRAMA
    
    # List Drama
    elif query.data == 'list_drama':
        query.edit_message_text(
            text=f"📺 <b>DAFTAR DRAMA</b>\n\n"
                 f"Buka channel kami untuk melihat semua drama:\n"
                 f"<a href='{DRAMA_CHANNEL_LINK}'>Klik di sini</a>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_button()
        )
    
    # Buy VIP
    elif query.data == 'buy_vip':
        query.edit_message_text(
            text="💎 <b>BELI VIP</b>\n\n"
                 "Pilih paket VIP yang sesuai dengan kebutuhan kamu:\n\n"
                 "<b>Keuntungan VIP:</b>\n"
                 "✅ Akses unlimited semua drama\n"
                 "✅ Bebas iklan\n"
                 "✅ Video quality HD\n"
                 "✅ Akses instant ke episode baru\n\n"
                 "<b>Harga lebih murah dengan paket lebih lama!</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_vip_packages_keyboard()
        )
    
    # Get Money (Referral)
    elif query.data == 'get_money':
        query.edit_message_text(
            text="💰 <b>DAPATKAN UANG!</b>\n\n"
                 "Ajak teman kamu untuk bergabung dan dapatkan komisi!\n\n"
                 "<b>Sistem 3 Level:</b>\n"
                 "🔸 Level 1: 20% (dari teman kamu)\n"
                 "🔸 Level 2: 3% (dari teman teman kamu)\n"
                 "🔸 Level 3: 2% (dari teman teman teman kamu)\n\n"
                 "<b>Contoh:</b>\n"
                 "Jika teman kamu beli VIP Rp20.900:\n"
                 "→ Kamu dapat Rp4.180\n"
                 "→ Minimal penarikan Rp10.000",
            parse_mode=ParseMode.HTML,
            reply_markup=get_referral_keyboard()
        )
    
    # Profile
    elif query.data == 'profile':
        stats = firebase.get_user_statistics(user_id)
        if stats:
            vip_status_text = "✅ Aktif" if stats['vip_status'] else "❌ Tidak Aktif"
            vip_expiry_text = f"\nBerlaku sampai: {stats['vip_expiry']}" if stats['vip_expiry'] else ""
            
            profile_text = f"""
👤 <b>STATUS AKUN KAMU</b>

🆔 User ID: <code>{stats['user_id']}</code>
👤 Nama: <b>{stats['name']}</b>
{'👑' if stats['vip_status'] else '⭐'} VIP: <b>{vip_status_text}</b>{vip_expiry_text}
💰 Saldo: <b>Rp{stats['balance']:,.0f}</b>
📊 Limit Harian: 8/10

<b>Jaringan Referral:</b>
🌳 Level 1: {stats['downlines'].get('L1', 0)} orang
🌳 Level 2: {stats['downlines'].get('L2', 0)} orang
🌳 Level 3: {stats['downlines'].get('L3', 0)} orang
"""
            
            query.edit_message_text(
                text=profile_text,
                parse_mode=ParseMode.HTML,
                reply_markup=get_back_button()
            )
    
    # VIP Package Selection
    elif query.data.startswith('vip_'):
        package_id = query.data.replace('vip_', '')
        if package_id in VIP_PACKAGES:
            package = VIP_PACKAGES[package_id]
            
            confirmation_text = f"""
💎 <b>KONFIRMASI PEMBELIAN VIP</b>

<b>Paket:</b> {package['label']}
<b>Durasi:</b> {package['days']} hari
<b>Harga:</b> Rp{package['price']:,.0f}

<b>Proses Pembayaran:</b>
1. Klik tombol "Bayar Sekarang"
2. Scan QRIS yang muncul
3. Pembayaran otomatis terverifikasi
4. VIP kamu aktif seketika! ✨

<b>Fitur VIP:</b>
✅ Akses semua episode
✅ Video HD quality
✅ Bebas gangguan iklan
✅ Download episode (optional)
"""
            
            keyboard = [
                [InlineKeyboardButton("✅ BAYAR SEKARANG", callback_data=f'pay_{package_id}')],
                [InlineKeyboardButton("🔙 Kembali", callback_data='buy_vip')]
            ]
            
            query.edit_message_text(
                text=confirmation_text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    # Process Payment
    elif query.data.startswith('pay_'):
        package_id = query.data.replace('pay_', '')
        if package_id in VIP_PACKAGES:
            package = VIP_PACKAGES[package_id]
            
            # Generate unique reference ID
            reference_id = f"susi_{user_id}_{int(datetime.now().timestamp())}"
            
            # Create invoice
            invoice = pakasir.create_invoice(
                user_id,
                package['price'],
                package_id,
                reference_id
            )
            
            if invoice:
                # Generate QRIS
                qris_response = pakasir.generate_qris(
                    reference_id,
                    package['price']
                )
                
                if qris_response:
                    qris_text = f"""
💳 <b>VIP PEMBAYARAN VIA QRIS</b>

📋 Paket: {package['label']}
💰 Harga: Rp{package['price']:,.0f}
🔔 Ref ID: <code>{reference_id}</code>

<b>Instruksi:</b>
1️⃣ Pilih paket di bawah
2️⃣ Nanti bot kirim kode QRIS yang bisa kamu scan
3️⃣ Setelah pembayaran terdeteksi, VIP kamu akan aktif otomatis

⏰ Pembayaran berlaku 1 jam
Silakan lakukan pembayaran sekarang 👇

<b>Metode Pembayaran:</b>
• Transfer Bank
• E-Wallet (Dana, OVO, GoPay, LinkAja)
• QRIS Universal
"""
                    
                    keyboard = [
                        [InlineKeyboardButton("💳 Lihat QRIS", callback_data=f'show_qris_{reference_id}')],
                        [InlineKeyboardButton("✅ Sudah Bayar", callback_data=f'confirm_pay_{reference_id}')],
                        [InlineKeyboardButton("❌ Batal", callback_data='buy_vip')]
                    ]
                    
                    query.edit_message_text(
                        text=qris_text,
                        parse_mode=ParseMode.HTML,
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
    
    # Show QRIS
    elif query.data.startswith('show_qris_'):
        reference_id = query.data.replace('show_qris_', '')
        payment = firebase.get_payment(reference_id)
        
        if payment:
            # Send QRIS image
            qris_image_url = f'https://api.pakasir.id/qris/{reference_id}'
            
            qris_info_text = f"""
📸 <b>QRIS CODE</b>

<b>Referensi:</b> <code>{reference_id}</code>
<b>Nominal:</b> Rp{payment['amount']:,.0f}

<b>Cara Pembayaran:</b>
1. Buka aplikasi perbankan kamu
2. Pilih fitur QRIS/Scan QR
3. Arahkan ke gambar QRIS di bawah
4. Ikuti instruksi pembayaran
5. Konfirmasi pembayaran

⏱️ Waktu berlaku: 1 jam
Pembayaran akan terdeteksi otomatis ✅
"""
            
            try:
                query.edit_message_text(
                    text=qris_info_text,
                    parse_mode=ParseMode.HTML,
                )
                # Send QRIS image
                context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=qris_image_url,
                    caption="Silakan scan QRIS ini",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("✅ Sudah Bayar", callback_data=f'confirm_pay_{reference_id}')],
                        [InlineKeyboardButton("❌ Batal", callback_data='buy_vip')]
                    ])
                )
            except Exception as e:
                logger.error(f"Error sending QRIS: {e}")
                query.edit_message_text(
                    text=f"{qris_info_text}\n\n⚠️ QRIS: {qris_image_url}",
                    parse_mode=ParseMode.HTML,
                )
    
    # Confirm Payment
    elif query.data.startswith('confirm_pay_'):
        reference_id = query.data.replace('confirm_pay_', '')
        
        # Check payment status
        payment = firebase.get_payment(reference_id)
        if payment and payment['status'] == 'pending':
            # Simulate payment confirmation
            pakasir.confirm_payment(reference_id)
            
            success_text = """
✅ <b>PEMBAYARAN BERHASIL!</b>

VIP kamu sudah <b>AKTIF</b> sekarang! 🎉

✨ Nikmati semua keuntungan:
✅ Akses unlimited semua drama
✅ Video HD quality
✅ Bebas gangguan iklan
✅ Priority upload episode baru

Selamat menonton! 🍿
Klik "CARI DRAMA" untuk memulai.
"""
            
            keyboard = [
                [InlineKeyboardButton("🔍 CARI DRAMA", callback_data='search_drama')],
                [InlineKeyboardButton("🔙 Kembali ke Menu", callback_data='back_to_menu')]
            ]
            
            query.edit_message_text(
                text=success_text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            query.edit_message_text(
                text="⏳ Pembayaran masih diproses. Silakan tunggu beberapa saat...",
                parse_mode=ParseMode.HTML,
            )
    
    # Get Referral Link
    elif query.data == 'get_referral_link':
        ref_code = firebase.get_referral_code(user_id)
        referral_link = f"https://t.me/susi_drama_bot?start={ref_code}"
        
        referral_text = f"""
🔗 <b>LINK REFERRAL KAMU</b>

Salin link ini dan bagikan ke teman/grup:

<code>{referral_link}</code>

<b>Cara share biar cepat dapat komisi:</b>
• WhatsApp / Telegram: kirim ke grup + status/story
• Facebook: post di timeline + share ke grup (iyual beli/komunitas)
• TikTok / Reels / Shorts: bikin video singkat 10-20 detik, taruh link di bio / komentar tersemat
• YouTube: taruh link di deskripsi + pinned comment
• Instagram: story + highlight (kalau ada link sticker, pakai itu)

✅ Tips: pakai 1 kalimat ajakan + link.
Jangan kepanjangan biar orang klik.

<b>Setiap orang yang klik link kamu & beli VIP:</b>
→ Kamu dapat komisi otomatis ke saldo
→ Langsung bisa dicairkan/dipakai belanja

💪 Happy sharing!
"""
        
        keyboard = [
            [InlineKeyboardButton("📋 Saldo & Komisi", callback_data='show_balance')],
            [InlineKeyboardButton("🔙 Kembali", callback_data='get_money')]
        ]
        
        query.edit_message_text(
            text=referral_text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    # Show Balance
    elif query.data == 'show_balance':
        stats = firebase.get_user_statistics(user_id)
        balance = stats['balance'] if stats else 0
        
        balance_text = f"""
💵 <b>SALDO & KOMISI</b>

💰 Saldo komisi (bisa ditarik): <b>Rp{balance:,.0f}</b>
✅ Sudah dicairkan: Rp0
⏳ Terpakai: Rp0
💎 Terpakai beli VIP: Rp0

<b>Minimal tarik dana:</b> Rp{MIN_WITHDRAWAL:,.0f}

Klik "Tarik Dana" untuk ajukan pencairan.
"""
        
        keyboard = [
            [InlineKeyboardButton("🏧 Tarik Dana", callback_data='withdraw_balance')],
            [InlineKeyboardButton("🔙 Kembali", callback_data='get_money')]
        ]
        
        query.edit_message_text(
            text=balance_text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    # Withdraw Balance
    elif query.data == 'withdraw_balance':
        stats = firebase.get_user_statistics(user_id)
        balance = stats['balance'] if stats else 0
        
        if balance < MIN_WITHDRAWAL:
            withdraw_text = f"""
❌ <b>SALDO BELUM CUKUP</b>

💰 Saldo kamu sekarang: Rp{balance:,.0f}
❌ Minimal penarikan: Rp{MIN_WITHDRAWAL:,.0f}

Kamu butuh Rp{MIN_WITHDRAWAL - balance:,.0f} lagi.

💡 Tip: 
Ajak lebih banyak teman untuk mendapat komisi lebih besar!
Berbagi link referral kamu di berbagai platform.
"""
        else:
            withdraw_text = f"""
✅ <b>TARIK DANA</b>

💰 Saldo kamu: Rp{balance:,.0f}
✅ Bisa ditarik: Rp{balance:,.0f}

<b>Pilih metode pencairan:</b>
"""
        
        keyboard = [
            [InlineKeyboardButton("🔙 Kembali", callback_data='show_balance')]
        ]
        
        query.edit_message_text(
            text=withdraw_text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    # Back to Menu
    elif query.data == 'back_to_menu':
        query.edit_message_text(
            text="👋 Selamat datang di Susi Drama! 🎬\n\nPilih menu di bawah:",
            reply_markup=get_main_menu_keyboard()
        )
    
    return -1

# ==================== SEARCH HANDLER ====================

def search_handler(update: Update, context: CallbackContext) -> int:
    """Handle search text input"""
    user_id = update.effective_user.id
    query_text = update.message.text
    
    if query_text.lower() == 'cancel' or query_text == '/cancel':
        update.message.reply_text(
            "❌ Pencarian dibatalkan",
            reply_markup=get_main_menu_keyboard()
        )
        return ConversationHandler.END
    
    # Search dramas
    search_results = content_manager.search_dramas(query_text)
    
    if not search_results:
        update.message.reply_text(
            f"❌ Drama dengan judul '{query_text}' tidak ditemukan.\n\n"
            f"Silakan coba judul lain atau lihat di LIST DRAMA 📺",
            reply_markup=get_back_button()
        )
        return SEARCHING_DRAMA
    
    # Format results
    search_text = f"🔍 <b>HASIL PENCARIAN: '{query_text}'</b>\n\n"
    keyboard = []
    
    for drama_id, drama in search_results.items():
        search_text += f"📺 <b>{drama['title']}</b>\n"
        search_text += f"   📂 {len(drama['parts'])} episode\n\n"
        
        keyboard.append([
            InlineKeyboardButton(
                f"▶️ {drama['title'][:30]}...",
                callback_data=f'watch_drama_{drama_id}_part_1'
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data='back_to_menu')])
    
    update.message.reply_text(
        search_text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return ConversationHandler.END

# ==================== WATCH DRAMA HANDLER ====================

def watch_drama(update: Update, context: CallbackContext) -> None:
    """Handle drama watching"""
    query = update.callback_query
    query.answer()
    user_id = update.effective_user.id
    
    if query.data.startswith('watch_drama_'):
        parts = query.data.replace('watch_drama_', '').split('_')
        drama_id = parts[0]
        part_key = '_'.join(parts[1:])  # handle part_1, part_2, etc
        
        drama = content_manager.get_drama(drama_id)
        if not drama:
            query.edit_message_text(
                text="❌ Drama tidak ditemukan",
                reply_markup=get_back_button()
            )
            return
        
        # Get video part
        video_data = content_manager.get_drama_part_video(drama_id, part_key, user_id)
        
        if video_data.get('requires_vip'):
            is_vip = video_data.get('is_vip', False)
            if not is_vip:
                # VIP required but not active
                part_info = drama['parts'][part_key]
                
                vip_text = f"""
🔒 <b>PART INI HANYA UNTUK MEMBER VIP</b>

📺 <b>{drama['title']}</b>
📍 Episode {part_info.get('episode')}

💎 Upgrade ke VIP sekarang untuk akses unlimited:

<b>Keuntungan VIP:</b>
✅ Akses semua episode tanpa batas
✅ Video HD quality
✅ Bebas gangguan iklan
✅ Prioritas episode baru

Paket VIP paling murah cuma Rp2.000 aja! 💰
"""
                
                keyboard = [
                    [InlineKeyboardButton("💎 Beli VIP Sekarang", callback_data='buy_vip')],
                    [InlineKeyboardButton("✅ Saya Sudah VIP", callback_data=f'watch_drama_{drama_id}_{part_key}')],
                    [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_menu')]
                ]
                
                query.edit_message_text(
                    text=vip_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                return
        
        # Send video
        if video_data.get('video_id'):
            watch_text = f"""
▶️ <b>{drama['title']}</b>
📍 Episode {video_data.get('episode')}
⏱️ Durasi: {video_data.get('duration')}

🔒 Video ini tidak dapat direkam atau di-forward
Nikmati menonton dengan nyaman! 🍿
"""
            
            try:
                query.edit_message_text(text="⏳ Memuat video...", parse_mode=ParseMode.HTML)
                
                context.bot.send_video(
                    chat_id=query.message.chat_id,
                    video=video_data['video_id'],
                    caption=watch_text,
                    parse_mode=ParseMode.HTML,
                    supports_streaming=True,
                    reply_markup=get_next_part_keyboard(drama_id, part_key)
                )
            except Exception as e:
                logger.error(f"Error sending video: {e}")
                query.edit_message_text(
                    text=f"❌ Error: Gagal memuat video\n\nError: {str(e)}",
                    parse_mode=ParseMode.HTML,
                    reply_markup=get_back_button()
                )

def get_next_part_keyboard(drama_id, current_part):
    """Build next part keyboard"""
    next_part = content_manager.get_next_part(drama_id, current_part)
    
    keyboard = []
    if next_part:
        keyboard.append([
            InlineKeyboardButton(
                f"▶️ Part Berikutnya",
                callback_data=f'watch_drama_{drama_id}_{next_part}'
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data='back_to_menu')])
    
    return InlineKeyboardMarkup(keyboard)

# ==================== ERROR HANDLER ====================

def error_handler(update: Update, context: CallbackContext) -> None:
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}")

# ==================== MAIN ====================

def main():
    """Start the bot"""
    print("🚀 Starting Susi Drama Bot...")
    
    # Create Updater
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start, pass_args=True))
    dispatcher.add_handler(CommandHandler("help", help_command))
    
    # Button callback handler
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    
    # Search drama handler
    search_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern='^search_drama$')],
        states={
            SEARCHING_DRAMA: [MessageHandler(Filters.text & ~Filters.command, search_handler)]
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)]
    )
    dispatcher.add_handler(search_conv_handler)
    
    # Watch drama handler
    dispatcher.add_handler(CallbackQueryHandler(watch_drama, pattern='^watch_drama_'))
    
    # Error handler
    dispatcher.add_error_handler(error_handler)
    
    # Start polling
    print("✅ Bot is running... Press Ctrl+C to stop")
    updater.start_polling(drop_pending_updates=True)
    updater.idle()

if __name__ == '__main__':
    main()
