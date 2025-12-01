from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.db.connection import get_db

presaved_bp = Blueprint("presaved", __name__)


@presaved_bp.route("/presaved", methods=("GET", "POST"))
@login_required
def presaved():

    db = get_db()
    cur = db.cursor()
    brands = cur.execute(get_brands()).fetchall()
    products = cur.execute(get_products()).fetchall()
    author_id = current_user.id
    presaved = cur.execute(get_presaved(), (author_id,)).fetchall()

    if request.method == "POST":
        presaved_id = request.form["presaved_id"]
        product_name = request.form["product_name"]
        product_url = request.form["product_url"]
        brand_name = request.form["new_brand_name"] or request.form["old_brand_name"]
        brand_website = request.form["brand_website"]
        if brand_name:
            result = cur.execute(
                "SELECT id FROM brands WHERE name = %s", (brand_name,)
            ).fetchone()
            if result:
                brand_id = result["id"]
            else:
                # Create new brand if old_brand_name doesn't have an ID
                cur.execute(
                    "INSERT INTO brands (name, website) VALUES (%s, %s) RETURNING id",
                    (brand_name, brand_website),
                )
                brand_id = cur.fetchone()["id"]
                db.commit()

        product_ingredients = request.form["product_ingredients"]
        product_energy = request.form["product_energy"]
        product_protein = request.form["product_protein"]
        product_fat = request.form["product_fat"]
        product_sat_fat = request.form["product_sat_fat"]
        product_carbs = request.form["product_carbs"]
        product_sugars = request.form["product_sugars"]
        product_fiber = request.form["product_fiber"]
        product_sodium = request.form["product_sodium"]
        product_c_vitamin = request.form["product_c_vitamin"]

        message = None
        if not presaved_id:
            message = "PRESAVED ID IS MISSING"
        if message is not None:
            flash(message)

        else:
            db.execute(
                "UPDATE presaved_products SET (author_id, product_name, product_url, brand_id, brand_name, brand_website, product_ingredients, product_energy, product_protein, product_fat, product_sat_fat, product_carbs, product_sugars, product_fiber, product_sodium, product_c_vitamin) = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) WHERE id = %s",
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
                    presaved_id,
                ),
            )

            db.commit()
            message = (
                "Successfully pre-saved product data, please complete missing data ASAP"
            )
            flash(message)

            return redirect(url_for("presaved.presaved"))

    return render_template(
        "main/presaved.html", products=products, brands=brands, presaved=presaved
    )


@presaved_bp.route("/presaved/delete", methods=("GET", "POST"))
@login_required
def delete():
    db = get_db()
    if request.method == "POST":
        delete_id = request.form["delete_id"]
        db.execute("DELETE FROM presaved_products WHERE id = %s", (delete_id,))
        db.commit()

    cur = db.cursor()
    author_id = current_user.id
    last_presaved = cur.execute(get_presaved(), (author_id,)).fetchall()
    if last_presaved:
        return redirect(url_for("presaved.presaved"))
    return redirect(url_for("inserts.inserts"))


def get_presaved():
    query = """
    SELECT * FROM presaved_products
    WHERE author_id = %s
    ORDER BY presaved_products.creation_date DESC
"""
    return query


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
