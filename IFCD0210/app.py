#!/usr/bin/env python

from flask import Flask, render_template
import psycopg
import os
from dotenv import load_dotenv

# To encode the special characters of the password:
from urllib.parse import quote

# Load the environment variables from the .env file
load_dotenv()
# Now you can access the DATABASE_URL environment variable

app = Flask(__name__)


def get_database_url():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")  # Raw password, no encoding needed
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    instance = os.getenv(
        "CLOUD_SQL_INSTANCE"
    )  # For production mode, leave it empty in .env for local dev mode and it'll use DB_HOST instead

    # Auto-encode password
    encoded_password = quote(password, safe="") if password else ""

    # Build connection string based on environment
    if instance:
        # Cloud Run/App Engine: Unix socket
        return f"postgresql://{user}:{encoded_password}@/{database}?host=/{host}/{instance}"
    else:
        # Local or TCP connection
        return f"dbname=pmt"


@app.route("/")
def index():
    try:
        conn_string = get_database_url()
        with psycopg.connect(conn_string) as conn:
            results = conn.execute(
                """
                SELECT products.off_code, products.name, brands.name, brands.website
                FROM products
                JOIN brands ON brands.id = products.brand_id
            """
            ).fetchall()

            # Safely build output, check if results exist
            if len(results) < 3:
                return "<p>Not enough products found.</p>"

            return render_template("index.html", results=results)

    except Exception as e:
        # Log the exception, and return an error message
        return (
            f"""
        <p>Database error:</p>
        <p>{str(e)}</p>
        """,
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
