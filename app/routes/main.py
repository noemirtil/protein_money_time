from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.db.connection import get_db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    db = get_db()
    cur = db.cursor()

    page = request.args.get("page", 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    cur.execute(
        # To look for the highest Protein Score cost-effective products
        """
SELECT
    products.id,
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
    prices.price * 0.01 AS price,
    prices.weight,
    ROUND((prices.price * 0.01) / (prices.weight * 0.001), 2) AS price_per_kg,
    prices."date" AS price_date,
    stores."name" AS store_name,
    countries.country,
    currencies.currency_code,
    CAST((products.protein / GREATEST(SUM(prices.weight * prices.price), 0.01))
    / GREATEST(products.fat, 0.001) * 10000000 AS INT) AS protein_score
FROM products
LEFT JOIN prices ON prices.product_id = products.id
LEFT JOIN brands ON products.brand_id = brands.id
LEFT JOIN stores ON prices.store_id = stores.id
LEFT JOIN countries ON stores.country_id = countries.id
LEFT JOIN currencies ON prices.currency_id = currencies.id
GROUP BY
    products.id,
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
    brands."name",
    prices.price,
    prices.weight,
    prices."date",
    stores."name",
    countries.country,
    currencies.currency_code
ORDER BY protein_score DESC NULLS LAST
LIMIT %s OFFSET %s
    """,
        (per_page, offset),
    )

    products = cur.fetchall()

    cur.execute("SELECT COUNT(*) as count FROM products")
    total_products = cur.fetchone()["count"]
    total_pages = (total_products + per_page - 1) // per_page

    return render_template(
        "main/index.html", products=products, page=page, total_pages=total_pages
    )
