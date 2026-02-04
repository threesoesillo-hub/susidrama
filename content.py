# Content & Video Management Module
from video_data import (
    get_all_dramas, 
    get_drama_by_id, 
    search_drama, 
    get_drama_part,
    DRAMAS
)
from firebase_db import get_firebase_db

class ContentManager:
    def __init__(self):
        self.firebase = get_firebase_db()
    
    def get_all_dramas(self):
        """Dapatkan semua drama"""
        return get_all_dramas()
    
    def get_drama(self, drama_id):
        """Dapatkan drama berdasarkan ID"""
        return get_drama_by_id(drama_id)
    
    def search_dramas(self, query):
        """Search drama berdasarkan judul"""
        return search_drama(query)
    
    def get_drama_list_formatted(self):
        """Dapatkan list drama dalam format untuk ditampilkan"""
        dramas = get_all_dramas()
        formatted = []
        
        for drama_id, drama in dramas.items():
            formatted.append({
                'drama_id': drama_id,
                'title': drama['title'],
                'parts_count': len(drama['parts'])
            })
        
        return formatted
    
    def get_drama_parts(self, drama_id):
        """Dapatkan semua part dari sebuah drama"""
        drama = get_drama_by_id(drama_id)
        if drama:
            return drama['parts']
        return None
    
    def get_drama_part_video(self, drama_id, part_key, user_id=None):
        """Dapatkan video part dengan check VIP status"""
        part = get_drama_part(drama_id, part_key)
        
        if not part:
            return None
        
        # Check if part requires VIP
        if part.get('requires_vip') and user_id:
            is_vip, _ = self.firebase.check_vip_status(user_id)
            if not is_vip:
                return {
                    'requires_vip': True,
                    'is_vip': False,
                    'message': 'Part ini hanya bisa diakses oleh member VIP'
                }
        
        return {
            'video_id': part.get('video_id'),
            'episode': part.get('episode'),
            'duration': part.get('duration'),
            'is_free': part.get('is_free', False),
            'requires_vip': part.get('requires_vip', False)
        }
    
    def get_next_part(self, drama_id, current_part):
        """Get part berikutnya"""
        drama = get_drama_by_id(drama_id)
        if not drama:
            return None
        
        parts = drama['parts']
        part_keys = sorted(parts.keys(), key=lambda x: int(x.split('_')[1]))
        
        current_index = part_keys.index(current_part) if current_part in part_keys else -1
        
        if current_index >= 0 and current_index + 1 < len(part_keys):
            return part_keys[current_index + 1]
        
        return None
    
    def get_drama_free_parts(self, drama_id):
        """Dapatkan part gratis dari drama"""
        drama = get_drama_by_id(drama_id)
        if not drama:
            return []
        
        free_parts = []
        for part_key, part_data in drama['parts'].items():
            if part_data.get('is_free', False):
                free_parts.append({
                    'part_key': part_key,
                    'episode': part_data.get('episode'),
                    'duration': part_data.get('duration')
                })
        
        return free_parts
    
    def get_drama_vip_parts(self, drama_id):
        """Dapatkan part VIP dari drama"""
        drama = get_drama_by_id(drama_id)
        if not drama:
            return []
        
        vip_parts = []
        for part_key, part_data in drama['parts'].items():
            if part_data.get('requires_vip', False):
                vip_parts.append({
                    'part_key': part_key,
                    'episode': part_data.get('episode'),
                    'duration': part_data.get('duration')
                })
        
        return vip_parts
    
    def count_dramas(self):
        """Hitung total drama"""
        return len(get_all_dramas())
    
    def count_total_parts(self):
        """Hitung total part dari semua drama"""
        dramas = get_all_dramas()
        total = 0
        for drama in dramas.values():
            total += len(drama['parts'])
        return total
    
    def add_drama(self, drama_data):
        """Tambah drama baru (untuk admin)"""
        try:
            drama_id = f"drama_{len(DRAMAS) + 1:03d}"
            drama_data['id'] = drama_id
            DRAMAS[drama_id] = drama_data
            return True, drama_id
        except Exception as e:
            print(f"Error adding drama: {e}")
            return False, None
    
    def add_part_to_drama(self, drama_id, part_key, part_data):
        """Tambah part ke drama (untuk admin)"""
        try:
            if drama_id in DRAMAS:
                DRAMAS[drama_id]['parts'][part_key] = part_data
                return True
            return False
        except Exception as e:
            print(f"Error adding part: {e}")
            return False

# Singleton instance
content_manager = ContentManager()

def get_content_manager():
    """Get Content Manager instance"""
    return content_manager
