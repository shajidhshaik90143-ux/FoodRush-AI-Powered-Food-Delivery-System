import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / 'instance'
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-secret-key')
    _raw_db_url = os.getenv('DATABASE_URL', '')
    if not _raw_db_url or _raw_db_url.strip() in ('sqlite:///instance/foodrush.db', 'sqlite:///foodrush.db'):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{(INSTANCE_DIR / 'foodrush.db').as_posix()}"
    else:
        SQLALCHEMY_DATABASE_URI = _raw_db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
