from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.db.connection import get_db

presave_bp = Blueprint("presave", __name__)


def get_presaved(db, author_id):
    query = """
    SELECT product_name, creation_date FROM presaved_products
    WHERE author_id = %s AND completed = False
    ORDER BY presaved_products.creation_date DESC
    """
    return db.execute(query, (author_id,)).fetchall()


def set_contributions(db, author_id):
    query = """
    UPDATE users SET contributions = (
    SELECT COUNT(*) FROM presaved_products
    WHERE author_id = %s AND completed = true
    ) WHERE id = %s
    """
    return db.execute(
        query,
        (
            author_id,
            author_id,
        ),
    )


def get_contributions(db, user_id):
    set_contributions(db, user_id)
    db.commit()

    query = """
    SELECT contributions FROM users
    WHERE id = %s
    """
    return db.execute(query, (user_id,)).fetchone()


def is_completed(db, product_name):
    return db.execute(
        "SELECT completed FROM presaved_products WHERE product_name = %s",
        (product_name,),
    ).fetchone()["completed"]


def get_brands(db):
    query = """
    SELECT * FROM brands
    ORDER BY brands.name
    """
    return db.execute(query).fetchall()


def get_brand_id(db, brand_name):
    query = """
    SELECT id FROM brands
    WHERE name = %s
    """
    result = db.execute(query, (brand_name,)).fetchone()
    return result["id"] if result else None


def get_products(db):
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
    return db.execute(query).fetchall()


@presave_bp.route("/presave", methods=("GET", "POST"))
@login_required
def presave():
    db = get_db()
    author_id = current_user.id
    presaved = get_presaved(db, author_id)
    contributions = get_contributions(db, author_id)
    brands = get_brands(db)
    products = get_products(db)
    old_new_brand = "both"

    if request.method == "POST":

        def opt(name):
            val = request.form.get(name)
            val = val.strip() if val else None
            return val or None

        product_name = (request.form.get("product_name") or "").strip()
        product_url = opt("product_url")
        old_new_brand = opt("old_new_brand")
        if old_new_brand == "old":
            brand_name = opt("old_brand_name")
        elif old_new_brand == "new":
            brand_name = opt("new_brand_name")
        else:
            brand_name = opt("new_brand_name") or opt("old_brand_name")
        brand_id = get_brand_id(db, brand_name) if brand_name else None
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

        if not product_name:
            flash("Product name is required.")
            return render_template(
                "main/presave.html",
                products=products,
                brands=brands,
                presaved=presaved,
                contributions=contributions,
                old_new_brand=old_new_brand,
            )

        # Check if product with same name already presaved and update
        for row in presaved:
            if product_name == row["product_name"]:
                presaved_id = row["id"]
                db.execute(
                    """
                    UPDATE presaved_products SET
                        author_id=%s, product_name=%s, product_url=%s, brand_id=%s,
                        brand_name=%s, brand_website=%s, product_ingredients=%s,
                        product_energy=%s, product_protein=%s, product_fat=%s,
                        product_sat_fat=%s, product_carbs=%s, product_sugars=%s,
                        product_fiber=%s, product_sodium=%s, product_c_vitamin=%s
                    WHERE id = %s
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
                        presaved_id,
                    ),
                )
                db.commit()
                if is_completed(db, product_name) == False:
                    flash(
                        "Successfully updated pre-saved product data, please complete missing data ASAP"
                    )
                else:
                    flash(
                        "Successfully updated COMPLETE product data, you earned a NEW MEDAL!"
                    )
                return redirect(url_for("presave.presave"))

        # Insert new presaved product
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

        if is_completed(db, product_name) == False:
            flash(
                "Successfully inserted pre-saved product data, please complete missing data ASAP"
            )
        else:
            flash(
                "Successfully inserted COMPLETE product data, you earned a NEW MEDAL!"
            )

        return redirect(url_for("presave.presave"))

    return render_template(
        "main/presave.html",
        products=products,
        brands=brands,
        presaved=presaved,
        contributions=contributions,
        old_new_brand=old_new_brand,
    )


@presave_bp.route("/presave/delete", methods=("GET", "POST"))
@login_required
def delete():
    db = get_db()
    if request.method == "POST":
        delete_id = request.form["delete_id"]
        db.execute("DELETE FROM presaved_products WHERE id = %s", (delete_id,))
        db.commit()
    return redirect(url_for("presave.presave"))


@presave_bp.route("/presave/edit", methods=("GET", "POST"))
@login_required
def edit():
    db = get_db()
    presaved_edit = []
    if request.method == "POST":
        presaved_id = request.form["edit_id"]
        presaved_edit = db.execute(
            "SELECT * FROM presaved_products WHERE id = %s ORDER BY creation_date DESC",
            (presaved_id,),
        ).fetchall()
    brands = get_brands(db)
    products = get_products(db)
    author_id = current_user.id
    presaved = get_presaved(db, author_id)
    contributions = get_contributions(db, author_id)
    return render_template(
        "main/presave.html",
        presaved_edit=presaved_edit,
        products=products,
        brands=brands,
        presaved=presaved,
        contributions=contributions,
    )
