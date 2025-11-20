from flask import Blueprint
from app.db.connection import get_db
from config import Config
from psycopg2.extras import RealDictCursor

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/test')
def test():
    return '<h2>Auth blueprint is working! ✅</h2>'

@auth_bp.route('/test-connection')
def test_connection():
    """Show what database we're connected to"""
    try:
        db = get_db()
        with db.cursor(cursor_factory=RealDictCursor) as cur:
            # Get current database name
            cur.execute("SELECT current_database();")
            db_name = cur.fetchone()
            
            # List all tables
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)
            tables = cur.fetchall()
            
            tables_list = [t['table_name'] for t in tables] if tables else []
            
            return f'''
                <h2>Connection Info:</h2>
                <p><strong>Database:</strong> {db_name['current_database']}</p>
                <p><strong>Host:</strong> {Config.DATABASE_HOST}</p>
                <p><strong>Tables found:</strong> {tables_list}</p>
            '''
    except Exception as e:
        return f'<h2>❌ Error: {str(e)}</h2>'