import os
from dotenv import load_dotenv
import cloudinary

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'eric-dev-secret-key-159')
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI:
        # Ensure we use pymysql driver for Vercel
        if SQLALCHEMY_DATABASE_URI.startswith('mysql://'):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('mysql://', 'mysql+pymysql://', 1)
            
        # If using TiDB/PlanetScale, make sure the SSL cert path is absolute
        if 'isrgrootx1.pem' in SQLALCHEMY_DATABASE_URI:
            cert_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'isrgrootx1.pem')
            # Replace backslashes with forward slashes for URL compatibility
            cert_path = cert_path.replace('\\', '/')
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('ssl_ca=isrgrootx1.pem', f'ssl_ca={cert_path}')
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///eric_portfolio_fallback.db'
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

    RESEND_API_KEY = os.getenv('RESEND_API_KEY')
    RESEND_FROM_EMAIL = os.getenv('RESEND_FROM_EMAIL', 'onboarding@resend.dev')
    RESEND_TO_EMAIL = os.getenv('RESEND_TO_EMAIL')

if Config.CLOUDINARY_CLOUD_NAME and Config.CLOUDINARY_API_KEY and Config.CLOUDINARY_API_SECRET:
    cloudinary.config(
        cloud_name=Config.CLOUDINARY_CLOUD_NAME,
        api_key=Config.CLOUDINARY_API_KEY,
        api_secret=Config.CLOUDINARY_API_SECRET,
        secure=True
    )
