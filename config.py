import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    SCHEMA_PATH = 'db/schema.sql'
    
    #Database config (PostgreSQL)
    DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'protein_money_time')
    DATABASE_USER = os.getenv('DATABASE_USER', 'postgres')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
    
    DATABASE_URL = os.getenv('DATABASE_URL', 
    f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?sslmode=require')
    
    #Enable CSRF for forms
    WTF_CSRF_ENABLED = True