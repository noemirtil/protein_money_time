from flask import Flask
import psycopg
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
# Now you can access the DATABASE_URL environment variable

app = Flask(__name__)


@app.route("/")
def index():
    try:
        conn_string = os.getenv("DATABASE_URL")
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

            return f"""
            <H1>THIS IS NOT A WEIGHT-LOSS APP</H1>
            <H2>Some results of a test query:</H2>
            <p>Product: {results[0][1]}, Brand: {results[0][2]}</p>
            <p>Product: {results[1][1]}, Brand: {results[1][2]}</p>
            <p>Product: {results[2][1]}, Brand: {results[2][2]}</p>
            """
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
    app.run(host="0.0.0.0", port=8080, debug=True)
