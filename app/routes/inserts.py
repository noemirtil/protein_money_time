from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.db.connection import get_db

inserts_bp = Blueprint("inserts", __name__)


@inserts_bp.route("/inserts", methods=("GET", "POST"))
# @login_required
def inserts():
    username = request.args.get("username", "").strip().lower()

    db = get_db()
    cur = db.cursor()

    user_id = cur.execute(
        "SELECT id FROM users WHERE username=%s", (username,)
    ).fetchone()
    author_id = user_id["id"] if user_id else None
    if author_id is None:
        flash("User not found.")
        return redirect(url_for("auth.login"))

    products = cur.execute(get_products()).fetchall()

    if request.method == "POST":
        product_name = request.form["product_name"]
        brand_name = request.form["brand_name"]
        message = None

        if not product_name:
            message = "Product name is required."

        if not brand_name:
            message = "Brand name is required."

        if message is not None:
            flash(message)

        else:
            db.execute(
                "INSERT INTO incomplete_products (author_id, product_name, brand_name) VALUES (%s, %s, %s)",
                (author_id, product_name, brand_name),
            )
            db.commit()
            message = "Product registered successfully!"
            flash(message)

            return redirect(url_for("inserts.inserts"))

    return render_template("main/inserts.html", products=products)


def get_products():
    query = """
    SELECT
        products.id,
        products.url,
        products.name,
        products.energy,
        products.fat,
        products.sat_fat,
        products.sodium,
        products.carbs,
        products.fiber,
        products.sugars,
        products.protein,
        products.c_vitamin,
        products.nutr_score_fr,
        products.ingredients_text,
        brands."name" AS brand_name,
        brands.website,
        prices.price * 0.01 AS price,
        prices.weight,
        ROUND((prices.price * 0.01) / (prices.weight * 0.001), 2) AS price_per_kg,
        prices."date" AS price_date,
        stores."name" AS store_name,
        countries.country,
        currencies.currency_code
    FROM products
    LEFT JOIN prices ON prices.product_id = products.id
    LEFT JOIN brands ON products.brand_id = brands.id
    LEFT JOIN stores ON prices.store_id = stores.id
    LEFT JOIN countries ON stores.country_id = countries.id
    LEFT JOIN currencies ON prices.currency_id = currencies.id
    ORDER BY products.name
        """
    return query
