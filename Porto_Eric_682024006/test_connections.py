import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_db():
    print("\n1. Menguji Koneksi Database (TiDB)...")
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("   [WARNING] DATABASE_URL tidak ditemukan di .env.")
        return False
    try:
        from sqlalchemy import create_engine
        engine = create_engine(db_url)
        with engine.connect() as conn:
            print("   [SUCCESS] Berhasil terhubung ke database TiDB!")
            return True
    except Exception as e:
        print(f"   [FAILED] Gagal terhubung ke database: {str(e)}")
        return False

def test_cloudinary():
    print("\n2. Menguji Konfigurasi Cloudinary...")
    name = os.getenv('CLOUDINARY_CLOUD_NAME')
    key = os.getenv('CLOUDINARY_API_KEY')
    secret = os.getenv('CLOUDINARY_API_SECRET')
    if not (name and key and secret):
        print("   [WARNING] Kredensial Cloudinary belum lengkap di .env.")
        return False
    try:
        import cloudinary
        import cloudinary.api
        cloudinary.config(
            cloud_name=name,
            api_key=key,
            api_secret=secret,
            secure=True
        )
        cloudinary.api.ping()
        print("   [SUCCESS] Berhasil otentikasi API Cloudinary!")
        return True
    except Exception as e:
        print(f"   [FAILED] Gagal terhubung ke Cloudinary: {str(e)}")
        return False

def test_resend():
    print("\n3. Menguji Konfigurasi Resend...")
    resend_key = os.getenv('RESEND_API_KEY')
    if not resend_key:
        print("   [WARNING] RESEND_API_KEY belum diisi di .env.")
        return False
    try:
        import resend
        resend.api_key = resend_key
        print("   [SUCCESS] Resend API Key terdeteksi dan terkonfigurasi!")
        return True
    except Exception as e:
        print(f"   [FAILED] Resend gagal dikonfigurasi: {str(e)}")
        return False

if __name__ == '__main__':
    print("====================================================")
    print("    DIAGNOSTIK INSTALASI & API PORTFOLIO ERIC   ")
    print("====================================================")
    
    if not os.path.exists('.env'):
        print("\n[WARNING] File .env tidak ditemukan!")
        try:
            import shutil
            shutil.copy('.env.example', '.env')
            print("[INFO] File .env berhasil dibuat dari .env.example.")
        except Exception as copy_err:
            print(f"[ERROR] Gagal membuat file .env: {str(copy_err)}")
            sys.exit(1)
            
    test_db()
    test_cloudinary()
    test_resend()
    
    print("\n====================================================")
    print("           DIAGNOSTIK SELESAI                       ")
    print("====================================================")
