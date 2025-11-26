from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.db.connection import get_db

main_bp = Blueprint('main', __name__)

def _assign_nutriscore_data(score):
    if score is None:
        return None, None
    
    try:
        score = float(score)
    except (ValueError, TypeError):
        return None, None

    # E: 19 to 40+
    if score >= 19:
        return 'E', 'red'
    # D: 11 to 18
    elif score >= 11:
        return 'D', 'orange'
    # C: 3 to 10
    elif score >= 3:
        return 'C', 'yellow'
    # B: 0 to 2
    elif score >= 0:
        return 'B', 'lime'
    # A: -15 to -1
    elif score >= -15: 
        return 'A', 'green'
    # Fallback for unexpected scores below -15
    return 'A', 'green'

@main_bp.route('/')
def index():
    db = get_db()
    cur = db.cursor()
    
    page = request.args.get('page', 1, type=int)
    per_page = 18
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
    
    processed_products = []
    for product_row in products:
        product = dict(product_row) # Convert row to dictionary if needed
        
        letter, color = _assign_nutriscore_data(product['nutr_score_fr'])
        
        product['nutri_letter'] = letter
        product['nutri_color'] = color
        
        processed_products.append(product)
    
    cur.execute("SELECT COUNT(*) as count FROM products")
    total_products = cur.fetchone()['count']
    total_pages = (total_products + per_page - 1) // per_page
    
    return render_template('main/index.html',
                        products=processed_products,
                        page=page,
                        total_pages=total_pages)