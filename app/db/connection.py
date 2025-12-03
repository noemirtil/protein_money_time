import psycopg
from psycopg.rows import dict_row
from flask import g, current_app

# To encode the special characters of the password:
from urllib.parse import quote
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()


def get_database_url():
    """Get database URL for Cloud SQL, local, or generic PostgreSQL."""

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    instance = os.getenv("CLOUD_SQL_INSTANCE")

    # Auto-encode password
    encoded_password = quote(password, safe="") if password else ""

    # Build connection string based on environment
    if instance:
        # Cloud Run: Unix socket
        return f"postgresql://{user}:{encoded_password}@/{database}?host=/cloudsql/{instance}"
    else:
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            return db_url
        else:
            return "dbname=pmt"


def get_db():
    if "db" not in g:
        try:
            g.db = psycopg.connect(
                get_database_url(),
                row_factory=dict_row,
            )
        except psycopg.Error as e:
            print(f"Falló la conexión a la base de datos: {e}")
            raise
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app):
    """Registers the database functions with the Flask app"""
    app.teardown_appcontext(close_db)
