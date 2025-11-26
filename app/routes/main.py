from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.db.connection import get_db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    db = get_db()
    cur = db.cursor()
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    
    cur.execute("""
        SELECT
        p.id,
        p.name,
        p.energy,
        p.fat,
        p.sat_fat,
        p.sodium,
        p.carbs,
        p.fiber,
        p.sugars,
        p.protein,
        p.c_vitamin,
        p.nutr_score_fr,
        p.ingredients_text,
        b.name as brand_name,
        pr.price,
        pr.weight,
        pr.date as price_date,
        s.name as store_name,
        c.country as country_name,
        curr.currency_code
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN LATERAL (
            SELECT price, weight, date, store_id, currency_id
            FROM prices
            WHERE product_id = p.id
            ORDER BY date DESC
            LIMIT 1
        ) pr ON true
        LEFT JOIN stores s ON pr.store_id = s.id
        LEFT JOIN countries c ON s.country_id = c.id
        LEFT JOIN currencies curr ON pr.currency_id = curr.id
        ORDER BY p.protein DESC
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    
    products = cur.fetchall()
    
    cur.execute("SELECT COUNT(*) as count FROM products")
    total_products = cur.fetchone()['count']
    total_pages = (total_products + per_page - 1) // per_page
    
    return render_template('main/index.html',
                        products=products,
                        page=page,
                        total_pages=total_pages)