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
        )

    return results


if __name__ == "__main__":
    app.run(debug=True)
