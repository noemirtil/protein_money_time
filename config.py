import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    SCHEMA_PATH = 'db/schema.sql'
    SEED_PATH = 'db/seed.sql'
    
    # Simple: Just read DATABASE_URL
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # WTF Forms
    WTF_CSRF_ENABLED = True