#!/usr/bin/env python

from flask import Flask, render_template
import psycopg
import os
from dotenv import load_dotenv

# To encode the special characters of the password:
from urllib.parse import quote

# Load the environment variables from the .env file
load_dotenv()

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
@app.route("/index.html")
@app.route("/protein.html")
def protein():
    try:
        conn_string = get_database_url()
        with psycopg.connect(conn_string) as conn:
            results_protein = conn.execute(
                """
SELECT "products"."name" AS "Product name", "prices"."price" * 0.01 AS "Price", "prices"."weight" AS "Grams",
ROUND(("prices"."price" * 0.01) / ("prices"."weight" * 0.001), 2) AS "Price per kg",
"products"."protein" AS "Protein",
"products"."fat" AS "Fat",
CAST(("products"."protein" / GREATEST(SUM("prices"."weight" * "prices"."price"), 0.01))
/ GREATEST("products"."fat", 0.001) * 10000000 AS INT) AS "Protein Score"
FROM "products"
JOIN "prices" ON "prices"."product_id" = "products"."id"
GROUP BY "products"."name", "products"."protein", "products"."fat", "prices"."price", "prices"."weight"
ORDER BY "Protein Score" DESC NULLS LAST;
            """
            ).fetchall()

            if len(results_protein) < 3:
                return "<p>Not enough products found.</p>"

            return render_template("protein.html", results_protein=results_protein)

    except Exception as e:
        return (
            f"""
        <p>Database error:</p>
        <p>{str(e)}</p>
        """,
            500,
        )


@app.route("/vitamin.html")
def vitamin():
    try:
        conn_string = get_database_url()
        with psycopg.connect(conn_string) as conn:
            results_vitamin = conn.execute(
                """
SELECT "products"."name" AS "Product name", "prices"."price" * 0.01 AS "Price", "prices"."weight" AS "Grams",
ROUND(("prices"."price" * 0.01) / ("prices"."weight" * 0.001), 2) AS "Price per kg",
"products"."c_vitamin" AS "C Vitamin",
"products"."sodium" AS "Sodium",
CAST(("products"."c_vitamin" / GREATEST(SUM("prices"."weight" * "prices"."price"), 0.01))
/ GREATEST("products"."sodium", 0.001) * 1000000000 AS INT) AS "C Vitamin Score"
FROM "products"
JOIN "prices" ON "prices"."product_id" = "products"."id"
GROUP BY "products"."name", "products"."c_vitamin", "products"."sodium", "prices"."price", "prices"."weight"
ORDER BY "C Vitamin Score" DESC NULLS LAST;
            """
            ).fetchall()

            if len(results_vitamin) < 3:
                return "<p>Not enough products found.</p>"

            return render_template("vitamin.html", results_vitamin=results_vitamin)

    except Exception as e:
        return (
            f"""
        <p>Database error:</p>
        <p>{str(e)}</p>
        """,
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
