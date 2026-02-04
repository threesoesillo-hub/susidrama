# File untuk menyimpan data video/drama
# Format: Setiap drama adalah dict dengan structure berikut
# Pisahkan file ini agar mudah di-edit dan di-update

DRAMAS = {
    'drama_001': {
        'id': 'drama_001',
        'title': 'DI BALIK HUJAN DAN DINGIN, AKU TETAP MENUNGGU',
        'thumbnail': 'https://via.placeholder.com/300x400?text=Drama+001',
        'description': 'Drama tentang cinta yang berliku-liku',
        'parts': {
            'part_1': {
                'episode': 1,
                'video_id': 'BAACAgIAAxkBAAI...',  # File ID dari Telegram
                'is_free': True,
                'duration': '45:30'
            },
            'part_2': {
                'episode': 2,
                'video_id': 'BAACAgIAAxkBAAI...',
                'is_free': False,
                'requires_vip': True,
                'duration': '48:15'
            },
            'part_3': {
                'episode': 3,
                'video_id': 'BAACAgIAAxkBAAI...',
                'is_free': False,
                'requires_vip': True,
                'duration': '50:00'
            },
            'part_4': {
                'episode': 4,
                'video_id': 'BAACAgIAAxkBAAI...',
                'is_free': False,
                'requires_vip': True,
                'duration': '46:45'
            },
            'part_5': {
                'episode': 5,
                'video_id': 'BAACAgIAAxkBAAI...',
                'is_free': False,
                'requires_vip': True,
                'duration': '49:30'
            },
            'part_6': {
                'episode': 6,
                'video_id': 'BAACAgIAAxkBAAI...',
                'is_free': False,
                'requires_vip': True,
                'duration': '51:20'
            }
        }
    },
    'drama_002': {
        'id': 'drama_002',
        'title': 'SKANDAL YANG MENGGEMPARKA : IBU TIRI MEMPEREBUTKAN WARISAN',
        'thumbnail': 'https://via.placeholder.com/300x400?text=Drama+002',
        'description': 'Drama penuh intrik keluarga',
        'parts': {
            'part_1': {
                'episode': 1,
                'video_id': 'BAACAgIAAxkBAAI...',
                'is_free': True,
                'duration': '44:00'
            },
            'part_2': {
                'episode': 2,
                'video_id': 'BAACAgIAAxkBAAI...',
                'is_free': False,
                'requires_vip': True,
                'duration': '45:30'
            }
        }
    },
    'drama_003': {
        'id': 'drama_003',
        'title': 'AYAH ANAKKU MUSUH DUNIA | BARAT',
        'thumbnail': 'https://via.placeholder.com/300x400?text=Drama+003',
        'description': 'Drama action thriller',
        'parts': {
            'part_1': {
                'episode': 1,
                'video_id': 'BAACAgIAAxkBAAI...',
                'is_free': True,
                'duration': '52:15'
            },
            'part_2': {
                'episode': 2,
                'video_id': 'BAACAgIAAxkBAAI...',
                'is_free': False,
                'requires_vip': True,
                'duration': '55:45'
            }
        }
    },
    'drama_004': {
        'id': 'drama_004',
        'title': 'SULIT DIGODA',
        'thumbnail': 'https://via.placeholder.com/300x400?text=Drama+004',
        'description': 'Drama comedy romance',
        'parts': {
            'part_1': {
                'episode': 1,
                'video_id': 'BAACAgIAAxkBAAI...',
                'is_free': True,
                'duration': '41:00'
            },
            'part_2': {
                'episode': 2,
                'video_id': 'BAACAgIAAxkBAAI...',
                'is_free': False,
                'requires_vip': True,
                'duration': '42:30'
            }
        }
    },
    'drama_005': {
        'id': 'drama_005',
        'title': 'SUAMI TAKUT ISTRI | DYLB',
        'thumbnail': 'https://via.placeholder.com/300x400?text=Drama+005',
        'description': 'Drama keluarga yang menghibur',
        'parts': {
            'part_1': {
                'episode': 1,
                'video_id': 'BAACAgIAAxkBAAI...',
                'is_free': True,
                'duration': '38:00'
            },
            'part_2': {
                'episode': 2,
                'video_id': 'BAACAgIAAxkBAAI...',
                'is_free': False,
                'requires_vip': True,
                'duration': '39:45'
            }
        }
    }
}

# Panduan cara menambah drama:
# 1. Buat entry baru dengan format: 'drama_XXX': {...}
# 2. Isi title, thumbnail, description, dan parts
# 3. Untuk setiap part, gunakan file_id dari video yang sudah di-upload ke Telegram
# 4. part_1 biasanya free (is_free: True)
# 5. Part selanjutnya memerlukan VIP (is_free: False, requires_vip: True)
# 
# Cara mendapatkan file_id dari Telegram:
# - Forward video ke bot
# - Ambil message.video.file_id dari response
# - Copy-paste ke file ini
#
# Format video_id Telegram contoh:
# 'BAACAgIAAxkBAAIBZ2Fg5rJ_...'

def get_all_dramas():
    """Get semua drama"""
    return DRAMAS

def get_drama_by_id(drama_id):
    """Get drama berdasarkan ID"""
    return DRAMAS.get(drama_id)

def search_drama(query):
    """Search drama berdasarkan judul"""
    query = query.lower()
    results = {}
    for drama_id, drama_data in DRAMAS.items():
        if query in drama_data['title'].lower():
            results[drama_id] = drama_data
    return results

def get_drama_part(drama_id, part_key):
    """Get bagian spesifik dari drama"""
    drama = DRAMAS.get(drama_id)
    if drama:
        return drama['parts'].get(part_key)
    return None
