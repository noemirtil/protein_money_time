from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.db.connection import get_db

main_bp = Blueprint('main', __name__)

def _assign_nutriscore_data(score):
    """Calculate Nutri-Score letter and color from score"""
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

def _get_products(cur, limit, offset, **kwargs):
    """
    Flexible product query with optional filters
    
    Args:
        cur: Database cursor
        limit: Number of results
        offset: Pagination offset
        **kwargs: Optional filters
            - keyword: Search term for name/brand/store
            - min_protein: Minimum protein amount
            - max_fat: Maximum fat amount
            - nutri_score_max: Maximum nutri-score
    """
    # Base query parts
    base_query = """
        SELECT
            p.id, p.name, p.energy, p.fat, p.sat_fat, p.sodium,
            p.carbs, p.fiber, p.sugars, p.protein, p.c_vitamin,
            p.nutr_score_fr, p.ingredients_text,
            b.name as brand_name,
            pr.price, pr.weight, pr.date as price_date,
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
    """
    
    conditions = []
    params = []
    
    # Add search keyword filter
    if 'keyword' in kwargs and kwargs['keyword']:
        keyword = kwargs['keyword']
        conditions.append("""
            (p.name ILIKE %s OR b.name ILIKE %s OR s.name ILIKE %s)
        """)
        params.extend([f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
    
    # Add protein filter
    if 'min_protein' in kwargs and kwargs['min_protein'] is not None:
        conditions.append("p.protein >= %s")
        params.append(kwargs['min_protein'])
    
    # Add fat filter
    if 'max_fat' in kwargs and kwargs['max_fat'] is not None:
        conditions.append("p.fat <= %s")
        params.append(kwargs['max_fat'])
    
    # Add nutri-score filter
    if 'nutri_score_max' in kwargs and kwargs['nutri_score_max'] is not None:
        conditions.append("p.nutr_score_fr <= %s")
        params.append(kwargs['nutri_score_max'])
    
    # Build WHERE clause
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)
    
    # Add ordering and pagination
    base_query += " ORDER BY p.protein DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    
    cur.execute(base_query, params)
    return cur.fetchall()

def _process_products(products):
    """Process products: add nutri-score letter/color"""
    processed = []
    for product_row in products:
        product = dict(product_row)
        letter, color = _assign_nutriscore_data(product['nutr_score_fr'])
        product['nutri_letter'] = letter
        product['nutri_color'] = color
        processed.append(product)
    return processed

@main_bp.route('/')
def index():
    db = get_db()
    cur = db.cursor()
    
    page = request.args.get('page', 1, type=int)
    per_page = 18
    offset = (page - 1) * per_page
    
    products = _get_products(cur, per_page, offset)
    processed_products = _process_products(products)
    
    cur.execute("SELECT COUNT(*) as count FROM products")
    total_products = cur.fetchone()['count']
    total_pages = (total_products + per_page - 1) // per_page
    
    return render_template('main/index.html',
                        products=processed_products,
                        page=page,
                        total_pages=total_pages)

                        
@main_bp.route('/api/search')
def api_search():
    """API endpoint for dynamic search - returns JSON"""
    db = get_db()
    cur = db.cursor()
    
    keyword = request.args.get('keyword', '').strip()
    
    if not keyword:
        return jsonify({'products': []})
    
    products = _get_products(cur, 100, 0, keyword=keyword)  # Max 100 results
    processed_products = _process_products(products)
    
    return jsonify({
        'products': processed_products,
        'count': len(processed_products)
    })
    
    