from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.db.connection import get_db

product_insert_bp = Blueprint("product_insert", __name__)


@product_insert_bp.route("/product_insert", methods=("GET", "POST"))
def product_insert():
    db = get_db()
    cur = db.cursor()
    products = cur.execute(get_products()).fetchall()

    return render_template("inserts/product_insert.html", products=products)


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
