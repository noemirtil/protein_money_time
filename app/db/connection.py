import psycopg2
from psycopg2.extras import RealDictCursor
from flask import g, current_app
from config import Config
import click

def get_db():
    if 'db' not in g:
        try:
            g.db = psycopg2.connect(
                Config.DATABASE_URL,
                cursor_factory=RealDictCursor
            )
        except psycopg2.Error as e:
            print(f"Falló la conexión a la base de datos: {e}")
            raise
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    """Initialize database with schema.sql"""
    db = get_db()

    try:
        print(f"📂 Looking for schema at: {Config.SCHEMA_PATH}")
        with current_app.open_resource(Config.SCHEMA_PATH) as f:
            sql_script = f.read().decode('utf-8')
        
        print(f"📄 Schema file read ({len(sql_script)} chars)")
        
        # Split by semicolon and clean up
        commands = sql_script.split(';')
        
        with db.cursor() as cur:
            for i, command in enumerate(commands, 1):
                # Remove comment lines and clean whitespace
                lines = []
                for line in command.split('\n'):
                    stripped = line.strip()
                    # Skip empty lines and full-line comments
                    if stripped and not stripped.startswith('--'):
                        lines.append(line)
                
                # Rebuild command without comment-only lines
                clean_command = '\n'.join(lines).strip()
                
                if not clean_command:
                    continue
                
                print(f"\n⚙️  Ejecutando comando {i}:")
                print(f"{clean_command[:100]}...")
                
                try:
                    cur.execute(clean_command)
                    print(f"✅ ¡Éxito!")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    print(f"Comand completo:\n{clean_command}")
                    db.rollback()
                    raise
        
        db.commit()
        print("\n🎉 ¡Base de datos iniciada con éxito!")
        
    except FileNotFoundError:
        print("❌ Error: schema.sql no encontrado.")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise


@click.command('init-db')
def init_db_command():
    """Reinicia la base de datos"""
    init_db()
    click.echo('✅ Se inició la base de datos.')

def init_app(app):
    """Registra la base de datos en la app de Flask"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)