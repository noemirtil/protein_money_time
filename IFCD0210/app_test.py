#!/usr/bin/env python

from flask import Flask
import psycopg

app = Flask(__name__)


@app.route("/")
def index():
    with psycopg.connect("dbname=pmt") as conn:
        results = conn.execute(
            """
                               SELECT "products"."off_code", "products"."name",
                               "brands"."name", "brands"."website" FROM "products"
                                JOIN "brands" ON "brands"."id" = "products"."brand_id"
                               """
        ).fetchall()

    return f"""
    <H1>SOME RESULTS OF A QUERY:</H1>
    <p>Product: {results[0][1]}, Brand: {results[0][2]}</p>
    <p>Product: {results[1][1]}, Brand: {results[1][2]}</p>
    <p>Product: {results[2][1]}, Brand: {results[2][2]}</p>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
