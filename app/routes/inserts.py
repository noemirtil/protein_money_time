from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.db.connection import get_db

inserts_bp = Blueprint("inserts", __name__)


@inserts_bp.route("/inserts", methods=("GET", "POST"))
@login_required
def inserts():

    db = get_db()
    cur = db.cursor()
    brands = cur.execute(get_brands()).fetchall()
    products = cur.execute(get_products()).fetchall()

    author_id = current_user.id
    if request.method == "POST":
        # Required field
        product_name = (request.form.get("product_name") or "").strip()

        # Optional fields: normalize empty to None
        def opt(name):
            val = request.form.get(name)
            val = val.strip() if val is not None else None
            return val or None

        product_url = opt("product_url")
        brand_id = "1"
        brand_name = "temp"
        brand_website = opt("brand_website")
        product_ingredients = opt("product_ingredients")
        product_energy = opt("product_energy")
        product_protein = opt("product_protein")
        product_fat = opt("product_fat")
        product_sat_fat = opt("product_sat_fat")
        product_carbs = opt("product_carbs")
        product_sugars = opt("product_sugars")
        product_fiber = opt("product_fiber")
        product_sodium = opt("product_sodium")
        product_c_vitamin = opt("product_c_vitamin")

        message = None
        if not product_name:
            message = "Product name is required."

        if message is not None:
            flash(message)
        else:
            db.execute(
                """
                INSERT INTO presaved_products (
                    author_id, product_name, product_url, brand_id, brand_name,
                    brand_website, product_ingredients, product_energy, product_protein,
                    product_fat, product_sat_fat, product_carbs, product_sugars,
                    product_fiber, product_sodium, product_c_vitamin
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    author_id,
                    product_name,
                    product_url,
                    brand_id,
                    brand_name,
                    brand_website,
                    product_ingredients,
                    product_energy,
                    product_protein,
                    product_fat,
                    product_sat_fat,
                    product_carbs,
                    product_sugars,
                    product_fiber,
                    product_sodium,
                    product_c_vitamin,
                ),
            )

            db.commit()
            message = (
                "Successfully pre-saved product data, please complete missing data ASAP"
            )
            flash(message)

            return redirect(url_for("presaved.presaved"))

    return render_template("main/inserts.html", products=products, brands=brands)


def get_brands():
    query = """
    SELECT * FROM brands
    ORDER BY brands.name
"""
    return query


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
