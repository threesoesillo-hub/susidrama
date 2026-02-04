# Script untuk test bot secara lokal sebelum production

import sys
from dotenv import load_dotenv
import os

load_dotenv()

def test_environment():
    """Test environment variables"""
    print("\n🔍 Testing Environment Variables...")
    
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'FIREBASE_PROJECT_ID',
        'FIREBASE_CLIENT_EMAIL',
        'PAKASIR_API_KEY'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
            print(f"❌ {var}")
        else:
            print(f"✅ {var}")
    
    if missing:
        print(f"\n⚠️  Missing: {', '.join(missing)}")
        return False
    
    print("\n✅ All environment variables OK!")
    return True

def test_imports():
    """Test all imports"""
    print("\n🔍 Testing Imports...")
    
    try:
        from config import TELEGRAM_BOT_TOKEN, VIP_PACKAGES
        print("✅ config.py")
    except Exception as e:
        print(f"❌ config.py: {e}")
        return False
    
    try:
        from video_data import get_all_dramas, search_drama
        print("✅ video_data.py")
    except Exception as e:
        print(f"❌ video_data.py: {e}")
        return False
    
    try:
        from firebase_db import get_firebase_db
        print("✅ firebase_db.py")
    except Exception as e:
        print(f"❌ firebase_db.py: {e}")
        print("   Note: Firebase error OK jika belum setup credentials")
    
    try:
        from payment import get_pakasir
        print("✅ payment.py")
    except Exception as e:
        print(f"❌ payment.py: {e}")
        return False
    
    try:
        from content import get_content_manager
        print("✅ content.py")
    except Exception as e:
        print(f"❌ content.py: {e}")
        return False
    
    print("\n✅ All imports OK!")
    return True

def test_bot_connection():
    """Test Telegram bot connection"""
    print("\n🔍 Testing Telegram Bot Connection...")
    
    try:
        import asyncio
        from telegram import Bot
        from config import TELEGRAM_BOT_TOKEN
        
        async def get_bot_info():
            bot = Bot(token=TELEGRAM_BOT_TOKEN)
            bot_info = await bot.get_me()
            return bot_info
        
        bot_info = asyncio.run(get_bot_info())
        print(f"✅ Bot connected: @{bot_info.username}")
        print(f"   Name: {bot_info.first_name}")
        print(f"   ID: {bot_info.id}")
        return True
    except Exception as e:
        print(f"❌ Bot connection failed: {e}")
        return False

def test_firebase():
    """Test Firebase connection"""
    print("\n🔍 Testing Firebase Connection...")
    
    try:
        from firebase_db import get_firebase_db
        firebase = get_firebase_db()
        print("✅ Firebase connected")
        return True
    except Exception as e:
        print(f"❌ Firebase connection failed: {e}")
        print("   Setup Firebase credentials di .env")
        return False

def test_video_data():
    """Test video data"""
    print("\n🔍 Testing Video Data...")
    
    try:
        from video_data import get_all_dramas, search_drama
        
        dramas = get_all_dramas()
        print(f"✅ Total drama: {len(dramas)}")
        
        # Test search
        results = search_drama("BALIK")
        print(f"✅ Search test: {len(results)} results")
        
        return True
    except Exception as e:
        print(f"❌ Video data error: {e}")
        return False

def run_all_tests():
    """Run semua test"""
    print("=" * 50)
    print("🧪 SUSI DRAMA BOT - TEST SUITE")
    print("=" * 50)
    
    results = {
        'Environment': test_environment(),
        'Imports': test_imports(),
        'Telegram': test_bot_connection(),
        'Firebase': test_firebase(),
        'Video Data': test_video_data(),
    }
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    total_pass = sum(1 for r in results.values() if r)
    total_tests = len(results)
    
    print(f"\nTotal: {total_pass}/{total_tests} passed")
    
    if total_pass == total_tests:
        print("\n🎉 All tests passed! Bot ready to run.")
        print("Run: python susidrama.py")
        return True
    else:
        print("\n⚠️  Some tests failed. Fix issues before running bot.")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
