import psycopg
from psycopg.rows import dict_row
from flask import g, current_app
from config import Config
import click
import csv
from flask.cli import with_appcontext
import os

# To encode the special characters of the password:
from urllib.parse import quote
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()


def get_database_url():
    """Get database URL for Cloud SQL, local, or Neon"""
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    instance = os.getenv("CLOUD_SQL_INSTANCE")

    # Auto-encode password
    encoded_password = quote(password, safe="") if password else ""

    # Build connection string based on environment
    if instance:
        # Cloud Run/App Engine: Unix socket
        return f"postgresql://{user}:{encoded_password}@/{database}?host=/{host}/{instance}"
    else:
        # Neon connection - use Config.DATABASE_URL if available
        if hasattr(Config, "DATABASE_URL") and Config.DATABASE_URL:
            return Config.DATABASE_URL
        # Local or TCP connection
        return f"dbname=pmt"


def get_db():
    if "db" not in g:
        try:
            g.db = psycopg.connect(
                get_database_url(),  # Changed from Config.DATABASE_URL
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


def split_sql_commands(sql):
    """Split SQL by semicolons, but respect dollar-quoted strings"""
    commands = []
    current_command = []
    in_dollar_quote = False

    lines = sql.split("\n")

    for line in lines:
        # Skip comments
        if line.strip().startswith("--"):
            if "CSV_IMPORT:" in line:
                current_command.append(line)
                cmd = "\n".join(current_command).strip()
                if cmd:
                    commands.append(cmd)
                current_command = []
            continue

        # Check if line contains $$
        if "$$" in line:
            in_dollar_quote = not in_dollar_quote

        # Add line to current command
        current_command.append(line)

        # Separate lines without dollar triggers and add them to the command
        if ";" in line and not in_dollar_quote:
            cmd = "\n".join(current_command).strip()
            if cmd:
                commands.append(cmd)
            current_command = []

    # Add any remaining command (Triggers or with $$ sign)
    if current_command:
        cmd = "\n".join(current_command).strip()
        if cmd:
            commands.append(cmd)

    return commands


def init_db():
    """Initialize database with schema.sql"""

    db = get_db()

    try:
        print(f"📂 Looking for schema at: {Config.SCHEMA_PATH}")

        # Open resource relative to app folder
        with current_app.open_resource(Config.SCHEMA_PATH) as f:
            sql_script = f.read().decode("utf-8")

        print(f"📄 Schema file read ({len(sql_script)} chars)")

        # Use smart splitting that handles $$
        commands = split_sql_commands(sql_script)

        with db.cursor() as cur:
            for i, command in enumerate(commands, 1):
                print(f"\n⚙️  Ejecutando comando {i}:")
                preview = command[:80].replace("\n", " ")
                print(f"{preview}...")

                try:
                    cur.execute(command)
                    print(f"✅ ¡Éxito!")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    print(f"Comando completo:\n{command}")
                    db.rollback()
                    raise

        db.commit()
        print("\n🎉 ¡Base de datos iniciada con éxito!")

    except FileNotFoundError:
        print(f"❌ Error: schema.sql no encontrado en {Config.SCHEMA_PATH}")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise


def _handle_csv_import(cur, db, filename, table_name, columns):
    """
    Reads a CSV file and uses psycopg2's copy_expert to insert data into a table.
    """
    try:
        csv_path = os.path.join(current_app.root_path, "db", filename)

        print(f"   Reading CSV from: {csv_path}")

        with open(csv_path, "r", encoding="utf-8") as f:
            # copy_sql = f"COPY \"{table_name}\" ({', '.join(f'\"{col}\"' for col in columns)}) FROM STDIN WITH CSV HEADER DELIMITER ';'"
            # in an f-string, you cannot use a backslash (\) followed by a double quote (") as you would in a regular string.
            copy_sql = (
                f'COPY "{table_name}" ({", ".join(f"{col}" for col in columns)}) FROM STDIN WITH CSV HEADER DELIMITER '
                ';"'
            )

            # psycopg3 uses db.copy() not cur.copy()
            with cur.copy(copy_sql) as copy_op:
                data = f.read()
                copy_op.write(data)

            db.commit()
            print(f"   ✅ ¡Éxito! Copied data into {table_name}.")

    except FileNotFoundError:
        print(f" ❌ Error: CSV file not found at expected location for {filename}")
        db.rollback()
        raise
    except Exception as e:
        print(f"   ❌ Error during CSV import into {table_name}: {e}")
        db.rollback()
        raise


def seed_db():
    """
    Seed database with seed.sql
    """

    db = get_db()

    try:
        print(f"📂 Buscando seed.sql en: {Config.SEED_PATH}")

        with current_app.open_resource(Config.SEED_PATH) as f:
            sql_script = f.read().decode("utf-8")

        print(f"📄 Archivo seed.sql leído ({len(sql_script)} caracteres)")

        # Use the smart split that handles $$
        commands = split_sql_commands(sql_script)

        with db.cursor() as cur:
            for i, command in enumerate(commands, 1):
                # Check if it's a CSV import instruction
                if "CSV_IMPORT:" in command:
                    # Format: -- CSV_IMPORT: filename|table_name|column1,column2|;

                    try:
                        parts = command.split(":", 1)[1].strip().split("|")
                    except IndexError:
                        print(f"❌ Error: Invalid CSV_IMPORT format in command {i}.")
                        continue

                    if len(parts) < 3:
                        print(
                            f"Error: invalid CSV_IMPORT forma in command {i}.Expected filename|table|columns."
                        )
                        continue

                    csv_filename = parts[0].strip()
                    table_name = parts[1].strip()
                    columns_str = parts[2].strip()
                    columns = (
                        [c.strip() for c in columns_str.split(",")]
                        if columns_str
                        else []
                    )

                    print(
                        f"\n📦 CSV import found: '{csv_filename}' into '{table_name}' ({len(columns)} cols)..."
                    )

                    _handle_csv_import(cur, db, csv_filename, table_name, columns)

                    continue

                # Execute SQL command
                print(f"\n⚙️  Ejecutando comando {i}: {command[:60]}...")

                try:
                    cur.execute(command)
                    db.commit()
                    print("✅ ¡Éxito!")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    print(f"Comando completo:\n{command}")
                    db.rollback()
                    raise

        print("\n🎉 ¡Database seeded successfully!")

    except FileNotFoundError:
        print(f"❌ Error: seed.sql no encontrado en {Config.SEED_PATH}")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise


@click.command("init-db")
def init_db_command():
    """Reinicia la base de datos"""
    init_db()
    click.echo("✅ Se inició la base de datos.")


@click.command("seed-db")
@with_appcontext
def seed_db_command():
    """Seed database with sample data"""
    seed_db()
    click.echo("🌱 Database seeded.")


def init_app(app):
    """Registra la base de datos en la app de Flask"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
